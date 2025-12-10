"""Vector memory using ChromaDB for semantic search."""

from typing import Any
from uuid import uuid4

import chromadb
from chromadb.config import Settings as ChromaSettings

from src.config import get_settings


class VectorMemory:
    """ChromaDB-backed vector memory for semantic search."""

    def __init__(
        self,
        collection_name: str = "agent_memory",
    ) -> None:
        """Initialize vector memory.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        self.collection_name = collection_name
        self.settings = get_settings()
        self._client: chromadb.ClientAPI | None = None
        self._collection: chromadb.Collection | None = None

    def _get_client(self) -> chromadb.ClientAPI:
        """Get or create ChromaDB client."""
        if self._client is None:
            self._client = chromadb.Client(
                ChromaSettings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=self.settings.chroma_persist_directory,
                    anonymized_telemetry=False,
                )
            )
        return self._client

    def _get_collection(self) -> chromadb.Collection:
        """Get or create the collection."""
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def add(
        self,
        text: str,
        metadata: dict[str, Any] | None = None,
        doc_id: str | None = None,
    ) -> str:
        """Add a document to vector memory.

        Args:
            text: Text content to store
            metadata: Additional metadata
            doc_id: Optional document ID

        Returns:
            Document ID
        """
        collection = self._get_collection()
        doc_id = doc_id or str(uuid4())

        collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id],
        )

        return doc_id

    def add_batch(
        self,
        texts: list[str],
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
    ) -> list[str]:
        """Add multiple documents to vector memory.

        Args:
            texts: List of text content
            metadatas: List of metadata dicts
            ids: List of document IDs

        Returns:
            List of document IDs
        """
        collection = self._get_collection()
        ids = ids or [str(uuid4()) for _ in texts]
        metadatas = metadatas or [{} for _ in texts]

        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )

        return ids

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for similar documents.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional filter conditions

        Returns:
            List of matching documents with scores
        """
        collection = self._get_collection()

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
        )

        # Format results
        documents = []
        for i in range(len(results["ids"][0])):
            doc = {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i] if results["documents"] else None,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else None,
            }
            documents.append(doc)

        return documents

    def get(self, doc_id: str) -> dict[str, Any] | None:
        """Get a document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document data or None
        """
        collection = self._get_collection()

        result = collection.get(ids=[doc_id])

        if not result["ids"]:
            return None

        return {
            "id": result["ids"][0],
            "text": result["documents"][0] if result["documents"] else None,
            "metadata": result["metadatas"][0] if result["metadatas"] else {},
        }

    def delete(self, doc_id: str) -> None:
        """Delete a document by ID."""
        collection = self._get_collection()
        collection.delete(ids=[doc_id])

    def clear(self) -> None:
        """Clear all documents in the collection."""
        client = self._get_client()
        client.delete_collection(self.collection_name)
        self._collection = None

    def count(self) -> int:
        """Get the number of documents in the collection."""
        collection = self._get_collection()
        return collection.count()

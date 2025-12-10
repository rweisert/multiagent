"""Conversation memory using Redis for persistence."""

import json
from datetime import datetime
from typing import Any

import redis.asyncio as redis
from pydantic import BaseModel

from src.config import get_settings


class Message(BaseModel):
    """A message in the conversation."""

    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = {}


class ConversationMemory:
    """Redis-backed conversation memory for agents."""

    def __init__(
        self,
        conversation_id: str,
        max_messages: int = 100,
    ) -> None:
        """Initialize conversation memory.

        Args:
            conversation_id: Unique identifier for this conversation
            max_messages: Maximum messages to retain
        """
        self.conversation_id = conversation_id
        self.max_messages = max_messages
        self.settings = get_settings()
        self._client: redis.Redis | None = None
        self._key = f"conversation:{conversation_id}"

    async def _get_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._client is None:
            self._client = redis.from_url(self.settings.redis_url)
        return self._client

    async def add_message(
        self,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Add a message to the conversation."""
        client = await self._get_client()

        message = Message(
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            metadata=metadata or {},
        )

        # Add to Redis list
        await client.rpush(self._key, message.model_dump_json())

        # Trim to max messages
        await client.ltrim(self._key, -self.max_messages, -1)

        return message

    async def get_messages(
        self,
        limit: int | None = None,
    ) -> list[Message]:
        """Get messages from the conversation.

        Args:
            limit: Maximum number of recent messages to return
        """
        client = await self._get_client()

        # Get all messages or last N
        if limit:
            messages_json = await client.lrange(self._key, -limit, -1)
        else:
            messages_json = await client.lrange(self._key, 0, -1)

        return [
            Message.model_validate_json(msg)
            for msg in messages_json
        ]

    async def get_context(
        self,
        limit: int = 10,
        format_as_string: bool = True,
    ) -> str | list[Message]:
        """Get conversation context for the agent.

        Args:
            limit: Number of recent messages to include
            format_as_string: Return as formatted string if True
        """
        messages = await self.get_messages(limit=limit)

        if not format_as_string:
            return messages

        # Format as conversation string
        lines = []
        for msg in messages:
            role = msg.role.capitalize()
            lines.append(f"{role}: {msg.content}")

        return "\n".join(lines)

    async def clear(self) -> None:
        """Clear all messages in the conversation."""
        client = await self._get_client()
        await client.delete(self._key)

    async def get_summary(self) -> dict[str, Any]:
        """Get a summary of the conversation."""
        client = await self._get_client()
        length = await client.llen(self._key)

        messages = await self.get_messages()
        roles_count = {}
        for msg in messages:
            roles_count[msg.role] = roles_count.get(msg.role, 0) + 1

        return {
            "conversation_id": self.conversation_id,
            "total_messages": length,
            "messages_by_role": roles_count,
            "first_message": messages[0].timestamp.isoformat() if messages else None,
            "last_message": messages[-1].timestamp.isoformat() if messages else None,
        }

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None

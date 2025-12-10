"""Azure Blob Storage I/O service for patent pipeline."""

import structlog
from urllib.parse import urlparse, parse_qs
from azure.storage.blob import BlobClient, BlobServiceClient, ContentSettings
from azure.core.exceptions import AzureError

from src.config import get_settings

logger = structlog.get_logger(__name__)


class AzureBlobService:
    """Service for Azure Blob Storage operations."""

    def __init__(self) -> None:
        """Initialize Azure Blob service."""
        self.settings = get_settings()
        self._service_client: BlobServiceClient | None = None

    @property
    def service_client(self) -> BlobServiceClient | None:
        """Get or create the blob service client."""
        if self._service_client is None and self.settings.azure_storage_connection_string:
            self._service_client = BlobServiceClient.from_connection_string(
                self.settings.azure_storage_connection_string
            )
        return self._service_client

    def download_from_url(self, blob_url: str) -> bytes:
        """Download blob content from a URL.

        Args:
            blob_url: Full Azure Blob URL (may include SAS token)

        Returns:
            Blob content as bytes
        """
        return download_blob(blob_url)

    def upload_to_container(
        self,
        container_url: str,
        blob_name: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload content to a blob in a container.

        Args:
            container_url: Container URL (may include SAS token)
            blob_name: Name for the blob
            content: Content to upload
            content_type: MIME type of the content

        Returns:
            URL of the uploaded blob
        """
        return upload_blob(container_url, blob_name, content, content_type)


def download_blob(url: str) -> bytes:
    """Download blob content from an Azure Blob URL.

    Args:
        url: Full Azure Blob URL (may include SAS token)

    Returns:
        Blob content as bytes

    Raises:
        AzureError: If download fails
    """
    logger.info("Downloading blob", url=_sanitize_url(url))

    try:
        blob_client = BlobClient.from_blob_url(url)
        data = blob_client.download_blob().readall()
        logger.info("Blob downloaded successfully", size_bytes=len(data))
        return data
    except AzureError as e:
        logger.error("Failed to download blob", error=str(e), url=_sanitize_url(url))
        raise


def upload_blob(
    container_url: str,
    blob_name: str,
    content: bytes,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload content to Azure Blob Storage.

    Args:
        container_url: Container URL (with or without SAS token)
        blob_name: Name for the blob
        content: Content to upload
        content_type: MIME type of the content

    Returns:
        URL of the uploaded blob (without SAS token)

    Raises:
        AzureError: If upload fails
    """
    # Construct blob URL from container URL
    parsed = urlparse(container_url)

    # Extract SAS token if present
    sas_token = ""
    if parsed.query:
        sas_token = f"?{parsed.query}"

    # Build blob URL
    base_container = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
    blob_url = f"{base_container}/{blob_name}{sas_token}"

    logger.info("Uploading blob", blob_name=blob_name, content_type=content_type)

    try:
        blob_client = BlobClient.from_blob_url(blob_url)

        content_settings = ContentSettings(content_type=content_type)

        blob_client.upload_blob(
            content,
            overwrite=True,
            content_settings=content_settings,
        )

        # Return URL without SAS token
        result_url = f"{base_container}/{blob_name}"
        logger.info("Blob uploaded successfully", url=result_url)
        return result_url

    except AzureError as e:
        logger.error("Failed to upload blob", error=str(e), blob_name=blob_name)
        raise


def split_container_and_name(blob_url: str) -> tuple[str, str]:
    """Split a blob URL into container URL and blob name.

    Args:
        blob_url: Full Azure Blob URL

    Returns:
        Tuple of (container_url, blob_name)

    Example:
        >>> split_container_and_name("https://account.blob.core.windows.net/container/path/file.pdf")
        ("https://account.blob.core.windows.net/container", "path/file.pdf")
    """
    parsed = urlparse(blob_url)

    # Path format: /container/blob/path/name.ext
    path_parts = parsed.path.lstrip("/").split("/", 1)

    if len(path_parts) < 2:
        raise ValueError(f"Invalid blob URL format: {blob_url}")

    container = path_parts[0]
    blob_name = path_parts[1]

    # Reconstruct container URL with SAS token if present
    container_url = f"{parsed.scheme}://{parsed.netloc}/{container}"
    if parsed.query:
        container_url = f"{container_url}?{parsed.query}"

    return container_url, blob_name


def get_base_name(blob_url: str) -> str:
    """Extract base name from blob URL (filename without extension).

    Args:
        blob_url: Full Azure Blob URL

    Returns:
        Base name of the file (without extension)

    Example:
        >>> get_base_name("https://account.blob.core.windows.net/container/US12345678.pdf")
        "US12345678"
    """
    _, blob_name = split_container_and_name(blob_url)

    # Get just the filename
    filename = blob_name.rsplit("/", 1)[-1]

    # Remove extension
    base_name = filename.rsplit(".", 1)[0]

    return base_name


def _sanitize_url(url: str) -> str:
    """Remove SAS token from URL for logging."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

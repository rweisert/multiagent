"""File handling tool for agents."""

from pathlib import Path
from typing import Any

import aiofiles
from langchain_core.tools import BaseTool as LangChainBaseTool, tool

from src.tools.base import BaseTool, ToolConfig


class FileHandlerTool(BaseTool):
    """Tool for reading and writing files."""

    def __init__(
        self,
        config: ToolConfig | None = None,
        allowed_directories: list[str] | None = None,
    ) -> None:
        """Initialize the file handler tool."""
        if config is None:
            config = ToolConfig(
                name="file_handler",
                description="Read and write text files in allowed directories",
            )
        super().__init__(config)
        # Default to a safe data directory
        self.allowed_directories = allowed_directories or ["./data", "./output"]

    def _is_path_allowed(self, file_path: str) -> bool:
        """Check if the file path is in allowed directories."""
        path = Path(file_path).resolve()
        for allowed_dir in self.allowed_directories:
            allowed_path = Path(allowed_dir).resolve()
            try:
                path.relative_to(allowed_path)
                return True
            except ValueError:
                continue
        return False

    async def execute(
        self,
        action: str,
        file_path: str,
        content: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute file operations.

        Args:
            action: 'read' or 'write'
            file_path: Path to the file
            content: Content to write (required for write action)
        """
        if not self._is_path_allowed(file_path):
            return {
                "tool": self.name,
                "action": action,
                "file_path": file_path,
                "error": f"Path not in allowed directories: {self.allowed_directories}",
                "status": "error",
            }

        path = Path(file_path)

        try:
            if action == "read":
                if not path.exists():
                    return {
                        "tool": self.name,
                        "action": action,
                        "file_path": file_path,
                        "error": "File not found",
                        "status": "error",
                    }

                async with aiofiles.open(path, mode="r") as f:
                    file_content = await f.read()

                return {
                    "tool": self.name,
                    "action": action,
                    "file_path": file_path,
                    "content": file_content,
                    "status": "success",
                }

            elif action == "write":
                if content is None:
                    return {
                        "tool": self.name,
                        "action": action,
                        "file_path": file_path,
                        "error": "Content required for write action",
                        "status": "error",
                    }

                # Ensure directory exists
                path.parent.mkdir(parents=True, exist_ok=True)

                async with aiofiles.open(path, mode="w") as f:
                    await f.write(content)

                return {
                    "tool": self.name,
                    "action": action,
                    "file_path": file_path,
                    "bytes_written": len(content),
                    "status": "success",
                }

            else:
                return {
                    "tool": self.name,
                    "action": action,
                    "error": f"Unknown action: {action}. Use 'read' or 'write'",
                    "status": "error",
                }

        except Exception as e:
            return {
                "tool": self.name,
                "action": action,
                "file_path": file_path,
                "error": str(e),
                "status": "error",
            }

    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to a LangChain compatible tool."""

        @tool(name=self.name, description=self.description)
        async def file_handler(
            action: str,
            file_path: str,
            content: str | None = None,
        ) -> dict[str, Any]:
            """Handle file operations (read/write)."""
            return await self.execute(action=action, file_path=file_path, content=content)

        return file_handler  # type: ignore

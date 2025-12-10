"""Base tool class for agent capabilities."""

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.tools import BaseTool as LangChainBaseTool
from pydantic import BaseModel, Field


class ToolConfig(BaseModel):
    """Configuration for a tool."""

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description for the agent")
    enabled: bool = Field(default=True, description="Whether the tool is enabled")


class BaseTool(ABC):
    """Base class for all tools in the system."""

    def __init__(self, config: ToolConfig) -> None:
        """Initialize the tool with configuration."""
        self.config = config

    @property
    def name(self) -> str:
        """Return the tool name."""
        return self.config.name

    @property
    def description(self) -> str:
        """Return the tool description."""
        return self.config.description

    @property
    def is_enabled(self) -> bool:
        """Check if the tool is enabled."""
        return self.config.enabled

    @abstractmethod
    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the tool with given parameters."""
        pass

    @abstractmethod
    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to a LangChain compatible tool."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"

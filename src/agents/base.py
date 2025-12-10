"""Base agent class and configuration."""

from abc import ABC, abstractmethod
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.config import get_settings


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent role description")
    model: str = Field(default="claude-sonnet-4-20250514", description="LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, gt=0)


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent with configuration."""
        self.config = config
        self.settings = get_settings()
        self._llm: ChatAnthropic | None = None
        self._conversation_history: list[BaseMessage] = []

    @property
    def llm(self) -> ChatAnthropic:
        """Get or create the LLM instance."""
        if self._llm is None:
            self._llm = ChatAnthropic(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                api_key=self.settings.anthropic_api_key,
            )
        return self._llm

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process input and return output."""
        pass

    async def invoke(self, message: str) -> str:
        """Send a message to the agent and get a response."""
        messages = [
            SystemMessage(content=self.system_prompt),
            *self._conversation_history,
            HumanMessage(content=message),
        ]

        response = await self.llm.ainvoke(messages)
        response_text = str(response.content)

        # Update conversation history
        self._conversation_history.append(HumanMessage(content=message))
        self._conversation_history.append(response)

        return response_text

    def reset_history(self) -> None:
        """Clear conversation history."""
        self._conversation_history = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.config.name!r}, role={self.config.role!r})"

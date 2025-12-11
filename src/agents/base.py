"""Base agent class with multi-LLM support."""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any

import google.generativeai as genai
import structlog
from anthropic import Anthropic
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pydantic import BaseModel, Field

from src.config import get_settings

logger = structlog.get_logger(__name__)

# Base paths for prompts and techpacks
PROMPTS_DIR = Path(__file__).parent.parent / "patent_pipeline" / "prompts"
TECHPACKS_DIR = Path(__file__).parent.parent / "patent_pipeline" / "techpacks"


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    GEMINI = "gemini"
    CLAUDE = "claude"


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent role description")
    provider: LLMProvider = Field(default=LLMProvider.GEMINI, description="LLM provider")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=8192, gt=0)


class BaseAgent(ABC):
    """Base class for all agents in the patent pipeline.

    Supports both Gemini and Claude as LLM backends.
    Loads prompts from external markdown files.
    """

    # Subclasses should override this with their prompt file name
    prompt_file: str | None = None

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent with configuration."""
        self.config = config
        self.settings = get_settings()
        self._system_prompt: str | None = None
        self._gemini_model: genai.GenerativeModel | None = None
        self._claude_client: Anthropic | None = None

        # Configure LLM clients
        self._configure_clients()

        # Load prompt from file if specified
        if self.prompt_file:
            self._load_prompt()

        logger.info(
            "Agent initialized",
            name=config.name,
            provider=config.provider.value,
        )

    def _configure_clients(self) -> None:
        """Configure LLM clients based on provider."""
        if self.config.provider == LLMProvider.GEMINI:
            if self.settings.google_api_key:
                genai.configure(api_key=self.settings.google_api_key)
        elif self.config.provider == LLMProvider.CLAUDE:
            if self.settings.anthropic_api_key:
                self._claude_client = Anthropic(api_key=self.settings.anthropic_api_key)

    def _load_prompt(self) -> None:
        """Load system prompt from markdown file."""
        if not self.prompt_file:
            return

        path = PROMPTS_DIR / self.prompt_file
        if path.exists():
            self._system_prompt = path.read_text(encoding="utf-8")
            logger.debug("Loaded prompt", agent=self.config.name, path=str(path))
        else:
            logger.warning("Prompt file not found", agent=self.config.name, path=str(path))

    @property
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        if self._system_prompt:
            return self._system_prompt
        return self._default_system_prompt()

    @abstractmethod
    def _default_system_prompt(self) -> str:
        """Return the default system prompt if no file is loaded."""
        pass

    @property
    def gemini_model(self) -> genai.GenerativeModel:
        """Get or create the Gemini model instance."""
        if self._gemini_model is None:
            self._gemini_model = genai.GenerativeModel(
                model_name=self.settings.gemini_model,
                generation_config=genai.GenerationConfig(
                    temperature=self.config.temperature,
                    max_output_tokens=self.config.max_tokens,
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
                system_instruction=self.system_prompt,
            )
        return self._gemini_model

    @property
    def claude_client(self) -> Anthropic:
        """Get the Claude client."""
        if self._claude_client is None:
            self._claude_client = Anthropic(api_key=self.settings.anthropic_api_key)
        return self._claude_client

    async def invoke(self, message: str, **kwargs) -> str:
        """Send a message to the agent and get a response.

        Args:
            message: The input message/prompt
            **kwargs: Additional arguments (e.g., files for Gemini)

        Returns:
            The agent's response as a string
        """
        if self.config.provider == LLMProvider.GEMINI:
            return await self._invoke_gemini(message, **kwargs)
        else:
            return await self._invoke_claude(message, **kwargs)

    async def _invoke_gemini(self, message: str, **kwargs) -> str:
        """Invoke Gemini model."""
        parts = [message]

        # Add any uploaded files
        if "files" in kwargs:
            parts = kwargs["files"] + parts

        response = self.gemini_model.generate_content(parts)
        return response.text

    async def _invoke_claude(self, message: str, **kwargs) -> str:
        """Invoke Claude model."""
        response = self.claude_client.messages.create(
            model=self.settings.default_model,
            max_tokens=self.config.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": message}],
        )
        return response.content[0].text

    @abstractmethod
    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process input and return output.

        Args:
            input_data: Dictionary with input data for the agent

        Returns:
            Dictionary with the agent's output
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.config.name!r}, provider={self.config.provider.value!r})"


def load_tech_pack(tech_center: str) -> str:
    """Load tech pack content for a given tech center.

    Args:
        tech_center: Tech center code (e.g., "2100", "2600")

    Returns:
        Tech pack markdown content

    Raises:
        FileNotFoundError: If tech pack not found
    """
    mapping = {
        "1600": "TECH_BIOTECH_TC1600_OptionB.md",
        "1700": "TECH_Chemistry_TC1700.md",
        "2100": "TECH_SOFTWARE_TC2100.md",
        "2400": "TECH_NETWORKING_TC2400.md",
        "2600": "TECH_COMMUNICATIONS_TC2600.md",
        "2800": "TECH_SEMICONDUCTORS_TC2800.md",
        "2900": "TECH_DESIGNS_TC2900.md",
        "3600": "TECH_ECOM_BUSINESS_TC3600.md",
        "3700": "TECH_MECH_MED_TC3700.md",
    }

    filename = mapping.get(tech_center)
    if not filename:
        logger.warning("Unknown tech center, defaulting to TC2100", tech_center=tech_center)
        filename = "TECH_SOFTWARE_TC2100.md"

    path = TECHPACKS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Tech pack not found: {path}")

    return path.read_text(encoding="utf-8")

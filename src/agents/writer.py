"""Writer agent for content creation."""

from typing import Any

from src.agents.base import AgentConfig, BaseAgent


class WriterAgent(BaseAgent):
    """Agent specialized in writing and content creation."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the writer agent."""
        if config is None:
            config = AgentConfig(
                name="Writer",
                role="Content creator who produces high-quality written material",
                temperature=0.7,  # Higher temperature for creativity
            )
        super().__init__(config)

    @property
    def system_prompt(self) -> str:
        """Return the system prompt for the writer."""
        return """You are a Content Writer agent. Your primary responsibilities are:

1. CONTENT CREATION: Write clear, engaging, and well-structured content
2. ADAPTATION: Adjust tone and style based on target audience
3. STORYTELLING: Create compelling narratives when appropriate
4. EDITING: Refine and improve written content

Guidelines:
- Write with clarity and purpose
- Use appropriate tone for the context
- Structure content logically with clear flow
- Engage the reader from the start
- Support claims with evidence when provided

Output Format:
- Use appropriate headings and sections
- Include introduction and conclusion
- Maintain consistent voice throughout
- Format for readability"""

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a writing request."""
        task = input_data.get("task", "")
        research = input_data.get("research", "")
        style = input_data.get("style", "professional")
        audience = input_data.get("audience", "general")

        prompt = f"""Create content based on the following requirements.

Writing Task: {task}

Research/Source Material:
{research if research else "None provided - use your knowledge"}

Style: {style}
Target Audience: {audience}

Please create well-structured, engaging content that:
1. Addresses the task requirements
2. Incorporates the provided research
3. Matches the requested style
4. Is appropriate for the target audience"""

        response = await self.invoke(prompt)

        return {
            "agent": self.config.name,
            "task": task,
            "content": response,
            "style": style,
            "audience": audience,
            "status": "completed",
        }

"""Reviewer agent for quality assurance and feedback."""

from typing import Any

from src.agents.base import AgentConfig, BaseAgent


class ReviewerAgent(BaseAgent):
    """Agent specialized in reviewing and providing feedback."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the reviewer agent."""
        if config is None:
            config = AgentConfig(
                name="Reviewer",
                role="Quality assurance specialist who reviews and improves content",
                temperature=0.3,  # Lower temperature for critical analysis
            )
        super().__init__(config)

    @property
    def system_prompt(self) -> str:
        """Return the system prompt for the reviewer."""
        return """You are a Quality Reviewer agent. Your primary responsibilities are:

1. QUALITY ASSESSMENT: Evaluate content for accuracy, clarity, and completeness
2. FEEDBACK: Provide constructive, actionable feedback
3. IMPROVEMENT: Suggest specific enhancements
4. VERIFICATION: Check facts and consistency

Guidelines:
- Be thorough but fair in assessments
- Provide specific, actionable feedback
- Balance criticism with recognition of strengths
- Focus on improving the end result
- Maintain professional objectivity

Output Format:
- Overall Assessment (score out of 10)
- Strengths identified
- Areas for improvement
- Specific suggestions
- Final recommendation"""

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a review request."""
        content = input_data.get("content", "")
        criteria = input_data.get("criteria", [])
        context = input_data.get("context", "")

        criteria_text = "\n".join(f"- {c}" for c in criteria) if criteria else "General quality review"

        prompt = f"""Review the following content and provide detailed feedback.

Content to Review:
{content}

Review Criteria:
{criteria_text}

Context: {context if context else "General content review"}

Please provide:
1. Overall quality score (1-10)
2. Key strengths
3. Areas needing improvement
4. Specific suggestions for enhancement
5. Final verdict (approve/revise/reject)"""

        response = await self.invoke(prompt)

        return {
            "agent": self.config.name,
            "review": response,
            "criteria_used": criteria,
            "status": "completed",
        }

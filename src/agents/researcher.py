"""Researcher agent for gathering and analyzing information."""

from typing import Any

from src.agents.base import AgentConfig, BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent specialized in research and information gathering."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the researcher agent."""
        if config is None:
            config = AgentConfig(
                name="Researcher",
                role="Research specialist who gathers and analyzes information",
                temperature=0.3,  # Lower temperature for factual research
            )
        super().__init__(config)

    @property
    def system_prompt(self) -> str:
        """Return the system prompt for the researcher."""
        return """You are a Research Specialist agent. Your primary responsibilities are:

1. INFORMATION GATHERING: Collect relevant information on given topics
2. ANALYSIS: Analyze data and identify key insights
3. SUMMARIZATION: Provide clear, concise summaries of findings
4. SOURCE EVALUATION: Assess the reliability of information sources

Guidelines:
- Be thorough and systematic in your research approach
- Present findings in a structured format
- Highlight key facts, statistics, and insights
- Note any limitations or gaps in available information
- Maintain objectivity and avoid speculation

Output Format:
- Start with a brief overview
- Present findings in organized sections
- Include relevant quotes or data points
- End with key takeaways"""

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a research request."""
        topic = input_data.get("topic", "")
        context = input_data.get("context", "")

        prompt = f"""Research the following topic and provide comprehensive findings.

Topic: {topic}

Additional Context: {context if context else "None provided"}

Please provide:
1. Overview of the topic
2. Key findings and insights
3. Relevant data or statistics
4. Potential implications
5. Recommendations for further research"""

        response = await self.invoke(prompt)

        return {
            "agent": self.config.name,
            "topic": topic,
            "findings": response,
            "status": "completed",
        }

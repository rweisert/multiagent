"""Writer Agent - Stage 3 Report Generation."""

import json
from typing import Any

import structlog

from src.agents.base import AgentConfig, BaseAgent, LLMProvider, PROMPTS_DIR

logger = structlog.get_logger(__name__)


class WriterAgent(BaseAgent):
    """Agent specialized in generating patent litigation reports.

    Uses Claude for high-quality writing capabilities.
    Corresponds to Stage 3 of the patent pipeline.
    """

    prompt_file = "PROMPT_Pipeline1_Stage3_ReportGeneration_v2.md"

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the writer agent."""
        if config is None:
            config = AgentConfig(
                name="Writer",
                role="Report generation specialist - creates comprehensive litigation reports",
                provider=LLMProvider.CLAUDE,
                temperature=0.7,  # Higher temperature for creative writing
                max_tokens=8192,
            )
        super().__init__(config)

    def _default_system_prompt(self) -> str:
        """Return the default system prompt for report writing."""
        return """You are a patent litigation report writer. Your job is to create comprehensive,
well-structured reports based on forensic analysis data.

Focus on:
- Clear, professional prose
- Accurate representation of findings
- Proper citations and references
- Logical organization and flow

Output reports in Markdown format."""

    def _clean_markdown_response(self, text: str) -> str:
        """Clean markdown response from code block markers."""
        text = text.strip()
        if text.startswith("```markdown"):
            text = text[11:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    async def generate_report(
        self,
        extraction: dict[str, Any],
        forensic_analysis: dict[str, Any],
    ) -> str:
        """Generate a patent litigation report.

        Args:
            extraction: Stage 1 extraction data
            forensic_analysis: Stage 2 forensic analysis data

        Returns:
            Report as Markdown string
        """
        logger.info("Generating report", agent=self.config.name)

        prompt = f"""{self.system_prompt}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(extraction, indent=2)}
```

## STAGE 2 FORENSIC DATA

```json
{json.dumps(forensic_analysis, indent=2)}
```

Generate a comprehensive patent litigation report based on the above data.
"""

        response = await self.invoke(prompt)
        report = self._clean_markdown_response(response)

        logger.info("Report generated", agent=self.config.name, length=len(report))
        return report

    async def revise_report(
        self,
        original_report: str,
        feedback: dict[str, Any],
        extraction: dict[str, Any],
        forensic_analysis: dict[str, Any],
    ) -> str:
        """Revise a report based on QC feedback.

        Args:
            original_report: The original report to revise
            feedback: QC feedback with issues to address
            extraction: Stage 1 extraction data for reference
            forensic_analysis: Stage 2 forensic analysis data for reference

        Returns:
            Revised report as Markdown string
        """
        logger.info(
            "Revising report",
            agent=self.config.name,
            issues_count=len(feedback.get("qc_issues", [])),
        )

        issues_text = "\n".join(
            f"- {issue.get('issue', issue)}" for issue in feedback.get("qc_issues", [])
        )

        prompt = f"""You are revising a patent litigation report based on QC feedback.

## ORIGINAL REPORT

{original_report}

## QC FEEDBACK - ISSUES TO ADDRESS

{issues_text}

## REFERENCE DATA

### Stage 1 Extraction
```json
{json.dumps(extraction, indent=2)}
```

### Stage 2 Forensic Analysis
```json
{json.dumps(forensic_analysis, indent=2)}
```

## INSTRUCTIONS

1. Address each QC issue listed above
2. Ensure all facts align with the extraction data
3. Ensure all analysis aligns with the forensic data
4. Maintain the original report structure where appropriate
5. Fix any factual errors, missing citations, or formatting issues

Output the complete revised report in Markdown format.
"""

        response = await self.invoke(prompt)
        revised_report = self._clean_markdown_response(response)

        logger.info("Report revised", agent=self.config.name, length=len(revised_report))
        return revised_report

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a report generation or revision request.

        Args:
            input_data: Dictionary containing:
                - extraction: Stage 1 extraction data
                - forensic_analysis: Stage 2 forensic analysis data
                - mode: "generate" (default) or "revise"
                - original_report: Original report (for revise mode)
                - feedback: QC feedback (for revise mode)

        Returns:
            Dictionary with:
                - agent: Agent name
                - report: Generated/revised report
                - status: "completed" or "failed"
        """
        extraction = input_data.get("extraction", {})
        forensic_analysis = input_data.get("forensic_analysis", {})
        mode = input_data.get("mode", "generate")

        try:
            if mode == "revise":
                original_report = input_data.get("original_report", "")
                feedback = input_data.get("feedback", {})
                report = await self.revise_report(
                    original_report, feedback, extraction, forensic_analysis
                )
            else:
                report = await self.generate_report(extraction, forensic_analysis)

            return {
                "agent": self.config.name,
                "report": report,
                "status": "completed",
            }

        except Exception as e:
            logger.error("Report generation failed", agent=self.config.name, error=str(e))
            return {
                "agent": self.config.name,
                "report": "",
                "status": "failed",
                "error": str(e),
            }

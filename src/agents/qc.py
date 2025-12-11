"""QC Agent - Stage 4 Quality Verification."""

import json
from typing import Any

import structlog

from src.agents.base import AgentConfig, BaseAgent, LLMProvider

logger = structlog.get_logger(__name__)


class QCResult:
    """Result of QC verification."""

    def __init__(
        self,
        qc_json: dict[str, Any],
        corrected_report: str,
        score: int,
        passed: bool,
        needs_revision: bool,
        needs_clarification: bool,
        clarification_questions: list[str],
    ):
        self.qc_json = qc_json
        self.corrected_report = corrected_report
        self.score = score
        self.passed = passed
        self.needs_revision = needs_revision
        self.needs_clarification = needs_clarification
        self.clarification_questions = clarification_questions

    @property
    def issues(self) -> list[dict[str, Any]]:
        """Get list of QC issues."""
        return self.qc_json.get("qc_issues", [])

    @property
    def grade(self) -> str:
        """Get quality grade."""
        return self.qc_json.get("quality_grade", "C")


class QCAgent(BaseAgent):
    """Agent specialized in quality verification of patent reports.

    Uses Claude for detailed analysis capabilities.
    Corresponds to Stage 4 of the patent pipeline.
    Can request revisions from Writer or clarifications from Analyst.
    """

    prompt_file = "PROMPT_Pipeline1_Stage4_QC_Verification_v2.md"

    # Quality thresholds
    PASS_THRESHOLD = 8  # Score >= 8 passes
    REVISION_THRESHOLD = 5  # Score < 5 requires revision

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the QC agent."""
        if config is None:
            config = AgentConfig(
                name="QC",
                role="Quality assurance auditor - verifies and corrects reports",
                provider=LLMProvider.CLAUDE,
                temperature=0.2,  # Low temperature for precise auditing
                max_tokens=8192,
            )
        super().__init__(config)

    def _default_system_prompt(self) -> str:
        """Return the default system prompt for QC."""
        return """You are a quality assurance auditor for patent litigation reports.
Your job is to verify reports against source data and identify issues.

You check for:
- Factual accuracy against extraction data
- Analytical consistency with forensic analysis
- Proper citations and references
- Completeness of required sections
- Formatting and presentation

You DO NOT add new analysis or invent information. You only verify and correct."""

    def _parse_qc_response(self, text: str) -> tuple[dict[str, Any], str]:
        """Parse QC response into JSON and corrected report.

        Args:
            text: Raw response containing both QC JSON and corrected report

        Returns:
            Tuple of (QC JSON dict, corrected report markdown)
        """
        # Parse QC JSON
        qc_json = {}
        if "QC_JSON_OUTPUT" in text or "```json" in text:
            try:
                qc_start = text.find("```json")
                if qc_start != -1:
                    qc_end = text.find("```", qc_start + 7)
                    qc_json_str = text[qc_start + 7:qc_end].strip()
                    qc_json = json.loads(qc_json_str)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Failed to parse QC JSON", error=str(e))

        # Parse corrected report
        corrected_report = ""
        if "FINAL_REPORT_OUTPUT" in text:
            report_marker = text.find("FINAL_REPORT_OUTPUT")
            report_start = text.find("```", report_marker)
            if report_start != -1:
                # Skip the opening ``` and optional language tag
                content_start = text.find("\n", report_start) + 1
                report_end = text.rfind("```")
                if report_end > content_start:
                    corrected_report = text[content_start:report_end].strip()
        elif "```markdown" in text:
            # Fallback: look for markdown block
            start = text.rfind("```markdown") + 11
            end = text.rfind("```")
            if end > start:
                corrected_report = text[start:end].strip()

        return qc_json, corrected_report

    def _calculate_score(self, qc_json: dict[str, Any]) -> int:
        """Calculate numeric score from QC result.

        Args:
            qc_json: QC JSON result

        Returns:
            Score from 0-10
        """
        grade = qc_json.get("quality_grade", "C").upper()
        grade_scores = {"A": 10, "B": 8, "C": 6, "D": 4, "F": 2}
        base_score = grade_scores.get(grade, 6)

        # Deduct points for issues
        issues = qc_json.get("qc_issues", [])
        critical_issues = sum(1 for i in issues if i.get("severity") == "critical")
        major_issues = sum(1 for i in issues if i.get("severity") == "major")

        score = base_score - (critical_issues * 2) - (major_issues * 1)
        return max(0, min(10, score))

    def _identify_clarification_needs(self, qc_json: dict[str, Any]) -> list[str]:
        """Identify questions that need analyst clarification.

        Args:
            qc_json: QC JSON result

        Returns:
            List of clarification questions
        """
        questions = []
        for issue in qc_json.get("qc_issues", []):
            issue_type = issue.get("type", "")
            if issue_type in ["missing_analysis", "unclear_reasoning", "data_mismatch"]:
                questions.append(
                    f"Please clarify: {issue.get('description', issue.get('issue', ''))}"
                )
        return questions

    async def verify(
        self,
        report: str,
        extraction: dict[str, Any],
        forensic_analysis: dict[str, Any],
    ) -> QCResult:
        """Verify a report against source data.

        Args:
            report: Report to verify (Markdown)
            extraction: Stage 1 extraction data
            forensic_analysis: Stage 2 forensic analysis data

        Returns:
            QCResult with verification results
        """
        logger.info("Starting QC verification", agent=self.config.name)

        prompt = f"""{self.system_prompt}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(extraction, indent=2)}
```

## STAGE 2 FORENSIC DATA

```json
{json.dumps(forensic_analysis, indent=2)}
```

## STAGE 3 REPORT TO VERIFY

{report}

---

Please provide your response in two clearly separated sections:

### QC_JSON_OUTPUT
```json
{{
    "quality_grade": "A/B/C/D/F",
    "qc_issues": [
        {{
            "type": "factual_error|missing_citation|formatting|incomplete|unclear_reasoning|data_mismatch",
            "severity": "critical|major|minor",
            "location": "section or line reference",
            "issue": "description of the issue",
            "correction": "suggested fix"
        }}
    ],
    "auto_fixes_applied": ["list of automatic fixes"],
    "summary": "overall QC summary"
}}
```

### FINAL_REPORT_OUTPUT
```markdown
{{corrected final report here}}
```
"""

        response = await self.invoke(prompt)
        qc_json, corrected_report = self._parse_qc_response(response)

        # Calculate score and determine actions
        score = self._calculate_score(qc_json)
        passed = score >= self.PASS_THRESHOLD
        needs_revision = score < self.REVISION_THRESHOLD
        clarification_questions = self._identify_clarification_needs(qc_json)
        needs_clarification = len(clarification_questions) > 0

        logger.info(
            "QC verification completed",
            agent=self.config.name,
            score=score,
            grade=qc_json.get("quality_grade", "?"),
            issues_count=len(qc_json.get("qc_issues", [])),
            passed=passed,
            needs_revision=needs_revision,
        )

        return QCResult(
            qc_json=qc_json,
            corrected_report=corrected_report or report,
            score=score,
            passed=passed,
            needs_revision=needs_revision,
            needs_clarification=needs_clarification,
            clarification_questions=clarification_questions,
        )

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a QC verification request.

        Args:
            input_data: Dictionary containing:
                - report: Report to verify
                - extraction: Stage 1 extraction data
                - forensic_analysis: Stage 2 forensic analysis data

        Returns:
            Dictionary with:
                - agent: Agent name
                - qc_result: QC JSON results
                - corrected_report: Corrected report if fixes applied
                - score: Numeric score (0-10)
                - passed: Whether report passed QC
                - needs_revision: Whether report needs major revision
                - needs_clarification: Whether analyst clarification needed
                - clarification_questions: Questions for analyst
                - status: "completed" or "failed"
        """
        report = input_data.get("report", "")
        extraction = input_data.get("extraction", {})
        forensic_analysis = input_data.get("forensic_analysis", {})

        try:
            result = await self.verify(report, extraction, forensic_analysis)

            return {
                "agent": self.config.name,
                "qc_result": result.qc_json,
                "corrected_report": result.corrected_report,
                "score": result.score,
                "passed": result.passed,
                "needs_revision": result.needs_revision,
                "needs_clarification": result.needs_clarification,
                "clarification_questions": result.clarification_questions,
                "status": "completed",
            }

        except Exception as e:
            logger.error("QC verification failed", agent=self.config.name, error=str(e))
            return {
                "agent": self.config.name,
                "qc_result": {},
                "corrected_report": report,
                "score": 0,
                "passed": False,
                "needs_revision": True,
                "needs_clarification": False,
                "clarification_questions": [],
                "status": "failed",
                "error": str(e),
            }

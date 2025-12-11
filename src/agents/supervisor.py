"""Supervisor Agent - Orchestration and Routing."""

from typing import Any

import structlog

from src.agents.base import AgentConfig, BaseAgent, LLMProvider

logger = structlog.get_logger(__name__)


class SupervisorAgent(BaseAgent):
    """Agent specialized in orchestrating the patent pipeline workflow.

    Makes routing decisions, manages quality gates, and coordinates
    between specialist agents.
    """

    prompt_file = None  # Uses embedded prompt

    # Maximum iterations for revision loops
    MAX_REVISIONS = 2
    MAX_CLARIFICATIONS = 1

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the supervisor agent."""
        if config is None:
            config = AgentConfig(
                name="Supervisor",
                role="Pipeline orchestrator - routes tasks and manages quality gates",
                provider=LLMProvider.CLAUDE,
                temperature=0.1,  # Very low for deterministic decisions
                max_tokens=1024,
            )
        super().__init__(config)

    def _default_system_prompt(self) -> str:
        """Return the default system prompt for supervision."""
        return """You are a workflow supervisor for patent litigation report generation.
Your job is to make routing decisions based on the current state of the pipeline.

You coordinate between:
- Extractor: Parses PDFs into structured data
- Analyst: Performs legal and technical analysis
- Writer: Generates reports
- QC: Verifies report quality

Make decisions based on:
- Current pipeline stage
- Quality scores and feedback
- Iteration counts
- Error conditions"""

    def decide_next_action(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """Decide the next action based on current state.

        This is a deterministic decision function (no LLM call needed).

        Args:
            state: Current pipeline state

        Returns:
            Dictionary with:
                - action: Next action to take
                - reason: Explanation for the decision
        """
        status = state.get("status", "pending")
        current_stage = state.get("current_stage", "start")
        revision_count = state.get("revision_count", 0)
        clarification_count = state.get("clarification_count", 0)
        qc_score = state.get("qc_score", 0)
        qc_passed = state.get("qc_passed", False)
        needs_revision = state.get("needs_revision", False)
        needs_clarification = state.get("needs_clarification", False)

        # Handle error state
        if status == "failed":
            return {
                "action": "abort",
                "reason": f"Pipeline failed: {state.get('error', 'Unknown error')}",
            }

        # Route based on current stage
        if current_stage == "start":
            return {
                "action": "extract",
                "reason": "Starting pipeline with PDF extraction",
            }

        if current_stage == "extracted":
            return {
                "action": "analyze",
                "reason": "Extraction complete, proceeding to analysis",
            }

        if current_stage == "analyzed":
            return {
                "action": "write",
                "reason": "Analysis complete, proceeding to report generation",
            }

        if current_stage == "written":
            return {
                "action": "qc",
                "reason": "Report generated, proceeding to QC verification",
            }

        if current_stage == "qc_complete":
            # QC passed - finalize
            if qc_passed:
                return {
                    "action": "finalize",
                    "reason": f"QC passed with score {qc_score}, finalizing report",
                }

            # Need clarification from analyst
            if needs_clarification and clarification_count < self.MAX_CLARIFICATIONS:
                return {
                    "action": "clarify",
                    "reason": f"QC needs clarification (attempt {clarification_count + 1}/{self.MAX_CLARIFICATIONS})",
                }

            # Need revision from writer
            if needs_revision and revision_count < self.MAX_REVISIONS:
                return {
                    "action": "revise",
                    "reason": f"QC score {qc_score} below threshold, revision needed (attempt {revision_count + 1}/{self.MAX_REVISIONS})",
                }

            # Max iterations reached - accept with warnings
            if revision_count >= self.MAX_REVISIONS:
                return {
                    "action": "finalize",
                    "reason": f"Max revisions ({self.MAX_REVISIONS}) reached, finalizing with score {qc_score}",
                }

            # Default: finalize
            return {
                "action": "finalize",
                "reason": f"Finalizing report with score {qc_score}",
            }

        if current_stage == "clarified":
            return {
                "action": "write",
                "reason": "Clarification received, regenerating report",
            }

        if current_stage == "revised":
            return {
                "action": "qc",
                "reason": "Report revised, re-running QC verification",
            }

        # Unknown stage
        logger.warning("Unknown stage", stage=current_stage)
        return {
            "action": "abort",
            "reason": f"Unknown stage: {current_stage}",
        }

    def should_continue(self, state: dict[str, Any]) -> bool:
        """Determine if the pipeline should continue.

        Args:
            state: Current pipeline state

        Returns:
            True if pipeline should continue, False to end
        """
        decision = self.decide_next_action(state)
        return decision["action"] not in ["finalize", "abort"]

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process a supervision request.

        Args:
            input_data: Dictionary containing current pipeline state

        Returns:
            Dictionary with routing decision
        """
        decision = self.decide_next_action(input_data)

        logger.info(
            "Supervisor decision",
            action=decision["action"],
            reason=decision["reason"],
            current_stage=input_data.get("current_stage"),
        )

        return {
            "agent": self.config.name,
            "decision": decision,
            "status": "completed",
        }

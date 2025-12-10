"""Stage 2 Merge node - combines Stage 2A, 2B, and 2C outputs."""

import structlog

from src.patent_pipeline.state import PatentPipelineState

logger = structlog.get_logger(__name__)


def stage2_merge_node(state: PatentPipelineState) -> PatentPipelineState:
    """Merge Stage 2A, 2B, and 2C outputs into unified stage2_forensic.

    This node:
    1. Combines all Stage 2 outputs into a single dictionary
    2. Updates state with stage2_forensic

    Args:
        state: Pipeline state with stage2a, stage2b, stage2c

    Returns:
        Updated state with stage2_forensic
    """
    logger.info("Starting Stage 2 Merge")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 2 Merge due to previous failure")
        return state

    try:
        stage2a = state.get("stage2a", {})
        stage2b = state.get("stage2b", {})
        stage2c = state.get("stage2c", {})

        # Merge all Stage 2 outputs
        stage2_forensic = {
            # From Stage 2A
            "claim_construction_rows": stage2a.get("claim_construction_rows", []),
            "estoppel_matrix_rows": stage2a.get("estoppel_matrix_rows", []),
            "construction_summary": stage2a.get("construction_summary", ""),
            "estoppel_summary": stage2a.get("estoppel_summary", ""),
            # From Stage 2B
            "technical_reps": stage2b.get("technical_reps", []),
            "search_gap_analysis": stage2b.get("search_gap_analysis", []),
            "convergence_rows": stage2b.get("convergence_rows", []),
            "technical_summary": stage2b.get("technical_summary", ""),
            "search_summary": stage2b.get("search_summary", ""),
            # From Stage 2C
            "event_forensics": stage2c.get("event_forensics", []),
            "global_findings": stage2c.get("global_findings"),
            "timeline_summary": stage2c.get("timeline_summary", ""),
        }

        updates["stage2_forensic"] = stage2_forensic

        logger.info(
            "Stage 2 Merge completed",
            total_construction_rows=len(stage2_forensic["claim_construction_rows"]),
            total_estoppel_rows=len(stage2_forensic["estoppel_matrix_rows"]),
            total_technical_reps=len(stage2_forensic["technical_reps"]),
            total_convergence_rows=len(stage2_forensic["convergence_rows"]),
            total_event_forensics=len(stage2_forensic["event_forensics"]),
        )

    except Exception as e:
        logger.error("Stage 2 Merge failed", error=str(e))
        updates["error"] = f"Stage 2 Merge failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

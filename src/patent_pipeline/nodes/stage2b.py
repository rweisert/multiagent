"""Stage 2B node - Search & Technical Premise Analysis."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient
from src.patent_pipeline.models.stage2 import Stage2B

logger = structlog.get_logger(__name__)


def stage2b_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 2B - Search & Technical Premise.

    This node:
    1. Analyzes technical representations in prosecution
    2. Identifies prior art search gaps
    3. Performs prior art convergence analysis
    4. Updates state with stage2b

    Args:
        state: Pipeline state with stage1_extraction, stage2a, and tech_pack_content

    Returns:
        Updated state with stage2b
    """
    logger.info("Starting Stage 2B - Search & Technical Premise")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 2B due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 2B
        result = client.call_stage2b(
            stage1_extraction=state["stage1_extraction"],
            stage2a=state["stage2a"],
            tech_pack_content=state.get("tech_pack_content", ""),
        )

        # Validate output structure
        try:
            Stage2B.model_validate(result)
            logger.info("Stage 2B output validated successfully")
        except Exception as val_error:
            logger.warning(
                "Stage 2B output validation warning",
                error=str(val_error),
            )

        updates["stage2b"] = result

        logger.info(
            "Stage 2B completed",
            technical_reps=len(result.get("technical_reps", [])),
            search_gaps=len(result.get("search_gap_analysis", [])),
            convergence_rows=len(result.get("convergence_rows", [])),
        )

    except Exception as e:
        logger.error("Stage 2B failed", error=str(e))
        updates["error"] = f"Stage 2B failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

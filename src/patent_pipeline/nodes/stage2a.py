"""Stage 2A node - Claim Construction & Estoppel Analysis."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient
from src.patent_pipeline.models.stage2 import Stage2A

logger = structlog.get_logger(__name__)


def stage2a_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 2A - Claim Construction & Estoppel.

    This node:
    1. Analyzes claims for construction issues
    2. Identifies prosecution history estoppel risks
    3. Updates state with stage2a

    Args:
        state: Pipeline state with stage1_extraction and tech_pack_content

    Returns:
        Updated state with stage2a
    """
    logger.info("Starting Stage 2A - Claim Construction & Estoppel")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 2A due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 2A
        result = client.call_stage2a(
            stage1_extraction=state["stage1_extraction"],
            tech_pack_content=state.get("tech_pack_content", ""),
        )

        # Validate output structure
        try:
            Stage2A.model_validate(result)
            logger.info("Stage 2A output validated successfully")
        except Exception as val_error:
            logger.warning(
                "Stage 2A output validation warning",
                error=str(val_error),
            )

        updates["stage2a"] = result

        logger.info(
            "Stage 2A completed",
            construction_rows=len(result.get("claim_construction_rows", [])),
            estoppel_rows=len(result.get("estoppel_matrix_rows", [])),
        )

    except Exception as e:
        logger.error("Stage 2A failed", error=str(e))
        updates["error"] = f"Stage 2A failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

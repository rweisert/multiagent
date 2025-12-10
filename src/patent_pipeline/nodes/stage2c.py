"""Stage 2C node - Timeline & Global Synthesis."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient
from src.patent_pipeline.models.stage2 import Stage2C

logger = structlog.get_logger(__name__)


def stage2c_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 2C - Timeline & Global Synthesis.

    This node:
    1. Performs forensic timeline analysis
    2. Synthesizes global findings across prosecution
    3. Updates state with stage2c

    Args:
        state: Pipeline state with stage1_extraction, stage2a, stage2b, tech_pack_content

    Returns:
        Updated state with stage2c
    """
    logger.info("Starting Stage 2C - Timeline & Global Synthesis")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 2C due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 2C
        result = client.call_stage2c(
            stage1_extraction=state["stage1_extraction"],
            stage2a=state["stage2a"],
            stage2b=state["stage2b"],
            tech_pack_content=state.get("tech_pack_content", ""),
        )

        # Validate output structure
        try:
            Stage2C.model_validate(result)
            logger.info("Stage 2C output validated successfully")
        except Exception as val_error:
            logger.warning(
                "Stage 2C output validation warning",
                error=str(val_error),
            )

        updates["stage2c"] = result

        logger.info(
            "Stage 2C completed",
            event_forensics=len(result.get("event_forensics", [])),
            has_global_findings=result.get("global_findings") is not None,
        )

    except Exception as e:
        logger.error("Stage 2C failed", error=str(e))
        updates["error"] = f"Stage 2C failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

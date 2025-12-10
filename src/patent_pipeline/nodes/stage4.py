"""Stage 4 node - QC & Verification."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import GeminiClient
from src.patent_pipeline.models.stage4 import Stage4QC

logger = structlog.get_logger(__name__)


def stage4_qc_node(state: PatentPipelineState) -> PatentPipelineState:
    """Execute Stage 4 - QC & Verification.

    This node:
    1. Verifies Stage 3 report against source data
    2. Identifies and corrects issues
    3. Updates state with stage4_qc_json and stage4_final_report_md

    Args:
        state: Pipeline state with stage1_extraction, stage2_forensic, stage3_report_md

    Returns:
        Updated state with stage4_qc_json and stage4_final_report_md
    """
    logger.info("Starting Stage 4 - QC & Verification")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Stage 4 due to previous failure")
        return state

    try:
        client = GeminiClient()

        # Call Stage 4
        qc_json, final_report_md = client.call_stage4(
            stage1_extraction=state["stage1_extraction"],
            stage2_forensic=state["stage2_forensic"],
            stage3_report_md=state["stage3_report_md"],
        )

        # Validate QC output structure
        try:
            Stage4QC.model_validate(qc_json)
            logger.info("Stage 4 QC output validated successfully")
        except Exception as val_error:
            logger.warning(
                "Stage 4 QC output validation warning",
                error=str(val_error),
            )

        updates["stage4_qc_json"] = qc_json
        updates["stage4_final_report_md"] = final_report_md

        # Log QC metrics
        metrics = qc_json.get("metrics", {})
        logger.info(
            "Stage 4 completed",
            total_issues=metrics.get("total_issues_found", 0),
            issues_corrected=metrics.get("issues_corrected", 0),
            overall_score=metrics.get("overall_quality_score", 0),
            approved=qc_json.get("approved_for_delivery", False),
            final_report_length=len(final_report_md),
        )

    except Exception as e:
        logger.error("Stage 4 failed", error=str(e))
        updates["error"] = f"Stage 4 failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

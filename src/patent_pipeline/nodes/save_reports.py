"""Save Reports node - uploads final reports to Azure Blob Storage."""

import json
import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.azure_io import upload_blob

logger = structlog.get_logger(__name__)


def save_reports_node(state: PatentPipelineState) -> PatentPipelineState:
    """Save generated reports to Azure Blob Storage.

    This node:
    1. Uploads Stage 3 report as Markdown
    2. Uploads Stage 4 final report as Markdown
    3. Uploads Stage 4 QC JSON
    4. Uploads Search Intelligence report (if available)
    5. Updates state with output URLs

    Args:
        state: Pipeline state with reports to save

    Returns:
        Updated state with report URLs
    """
    logger.info("Starting Save Reports")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Save Reports due to previous failure")
        return state

    try:
        container_url = state["azure_container_url"]
        base_name = state["base_name"]

        # Save Stage 3 Report
        if state.get("stage3_report_md"):
            stage3_url = upload_blob(
                container_url=container_url,
                blob_name=f"{base_name}_Stage3_Report.md",
                content=state["stage3_report_md"].encode("utf-8"),
                content_type="text/markdown",
            )
            updates["stage3_url"] = stage3_url
            logger.info("Stage 3 report saved", url=stage3_url)

        # Save Stage 4 Final Report
        if state.get("stage4_final_report_md"):
            stage4_url = upload_blob(
                container_url=container_url,
                blob_name=f"{base_name}_Stage4_Final_Report.md",
                content=state["stage4_final_report_md"].encode("utf-8"),
                content_type="text/markdown",
            )
            updates["stage4_url"] = stage4_url
            logger.info("Stage 4 final report saved", url=stage4_url)

        # Save Stage 4 QC JSON
        if state.get("stage4_qc_json"):
            qc_url = upload_blob(
                container_url=container_url,
                blob_name=f"{base_name}_Stage4_QC.json",
                content=json.dumps(state["stage4_qc_json"], indent=2).encode("utf-8"),
                content_type="application/json",
            )
            logger.info("Stage 4 QC JSON saved", url=qc_url)

        # Save Search Intelligence Report
        if state.get("search_intel_report_md"):
            search_intel_url = upload_blob(
                container_url=container_url,
                blob_name=f"{base_name}_Search_Intelligence_Report.md",
                content=state["search_intel_report_md"].encode("utf-8"),
                content_type="text/markdown",
            )
            updates["search_intel_url"] = search_intel_url
            logger.info("Search Intelligence report saved", url=search_intel_url)

        # Mark pipeline as completed
        updates["status"] = "completed"

        logger.info(
            "Save Reports completed",
            stage3_url=updates.get("stage3_url"),
            stage4_url=updates.get("stage4_url"),
            search_intel_url=updates.get("search_intel_url"),
        )

    except Exception as e:
        logger.error("Save Reports failed", error=str(e))
        updates["error"] = f"Save Reports failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

"""Tech Pack Router node - selects appropriate tech pack based on metadata."""

import structlog

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.services.gemini_client import load_tech_pack

logger = structlog.get_logger(__name__)


def tech_pack_router_node(state: PatentPipelineState) -> PatentPipelineState:
    """Route to appropriate tech pack based on Stage 1 metadata.

    This node:
    1. Extracts tech center from Stage 1 metadata
    2. Loads the corresponding tech pack
    3. Updates state with tech pack content

    Args:
        state: Pipeline state with stage1_extraction

    Returns:
        Updated state with tech_center, tech_pack_name, tech_pack_content
    """
    logger.info("Starting Tech Pack Router")

    updates: dict = {}

    # Check for previous errors
    if state.get("status") == "failed":
        logger.warning("Skipping Tech Pack Router due to previous failure")
        return state

    try:
        extraction = state["stage1_extraction"]
        metadata = extraction.get("metadata", {})

        # Determine tech center
        tech_center = metadata.get("tech_center")
        art_unit = metadata.get("art_unit", "")

        if not tech_center and art_unit:
            # Derive tech center from art unit (first 2 digits + "00")
            tech_center = art_unit[:2] + "00"
            logger.info(
                "Derived tech center from art unit",
                art_unit=art_unit,
                tech_center=tech_center,
            )

        if not tech_center:
            # Default to software/2100 if we can't determine
            tech_center = "2100"
            logger.warning("Could not determine tech center, defaulting to 2100")

        updates["tech_center"] = tech_center

        # Load tech pack
        tech_pack_content = load_tech_pack(tech_center)
        updates["tech_pack_content"] = tech_pack_content

        # Determine tech pack name
        mapping = {
            "1600": "TECH_BIOTECH_TC1600_OptionB.md",
            "1700": "TECH_Chemistry_TC1700.md",
            "2100": "TECH_SOFTWARE_TC2100.md",
            "2400": "TECH_NETWORKING_TC2400.md",
            "2600": "TECH_COMMUNICATIONS_TC2600.md",
            "2800": "TECH_SEMICONDUCTORS_TC2800.md",
            "2900": "TECH_DESIGNS_TC2900.md",
            "3600": "TECH_ECOM_BUSINESS_TC3600.md",
            "3700": "TECH_MECH_MED_TC3700.md",
        }
        updates["tech_pack_name"] = mapping.get(tech_center, "TECH_SOFTWARE_TC2100.md")

        logger.info(
            "Tech Pack Router completed",
            tech_center=tech_center,
            tech_pack_name=updates["tech_pack_name"],
        )

    except FileNotFoundError as e:
        logger.error("Tech pack not found", error=str(e))
        # Use empty tech pack content but continue
        updates["tech_pack_content"] = "# Tech Pack Not Available\n\nNo specific tech pack guidance available."
        updates["tech_pack_name"] = "default"

    except Exception as e:
        logger.error("Tech Pack Router failed", error=str(e))
        updates["error"] = f"Tech Pack Router failed: {str(e)}"
        updates["status"] = "failed"

    return {**state, **updates}

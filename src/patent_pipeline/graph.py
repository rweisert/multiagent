"""LangGraph pipeline definition for patent litigation reports."""

import structlog
from langgraph.graph import StateGraph, END

from src.patent_pipeline.state import PatentPipelineState
from src.patent_pipeline.nodes import (
    ingest_pdfs_node,
    stage1_extraction_node,
    tech_pack_router_node,
    stage2a_node,
    stage2b_node,
    stage2c_node,
    stage2_merge_node,
    stage3_report_node,
    stage4_qc_node,
    search_intel_node,
    save_reports_node,
)

logger = structlog.get_logger(__name__)


def should_continue(state: PatentPipelineState) -> str:
    """Determine if pipeline should continue or end due to failure.

    Args:
        state: Current pipeline state

    Returns:
        "continue" or "end"
    """
    if state.get("status") == "failed":
        logger.warning("Pipeline ending due to failure", error=state.get("error"))
        return "end"
    return "continue"


def create_patent_pipeline() -> StateGraph:
    """Create the patent litigation report pipeline graph.

    The pipeline follows this flow:

    ```
    Ingest PDFs
         ↓
    Stage 1 – Record Extraction
         ↓
    Tech Pack Router
         ↓
    Stage 2A – Claim Construction & Estoppel
         ↓
    ┌────┴────┐
    ↓         ↓
    Stage 2B  Stage 2C (parallel)
    ↓         ↓
    └────┬────┘
         ↓
    Stage 2 Merge
         ↓
    ┌────┴────┐
    ↓         ↓
    Stage 3   Search Intel (parallel)
    ↓         ↓
    Stage 4   │
    ↓         │
    └────┬────┘
         ↓
    Save Reports
         ↓
        END
    ```

    Returns:
        Compiled LangGraph StateGraph
    """
    logger.info("Creating patent pipeline graph")

    # Create the graph
    graph = StateGraph(PatentPipelineState)

    # Add nodes
    graph.add_node("ingest_pdfs", ingest_pdfs_node)
    graph.add_node("stage1_extraction", stage1_extraction_node)
    graph.add_node("tech_pack_router", tech_pack_router_node)
    graph.add_node("stage2a", stage2a_node)
    graph.add_node("stage2b", stage2b_node)
    graph.add_node("stage2c", stage2c_node)
    graph.add_node("stage2_merge", stage2_merge_node)
    graph.add_node("stage3_report", stage3_report_node)
    graph.add_node("stage4_qc", stage4_qc_node)
    graph.add_node("search_intel", search_intel_node)
    graph.add_node("save_reports", save_reports_node)

    # Set entry point
    graph.set_entry_point("ingest_pdfs")

    # Define edges - sequential flow with some parallelism

    # Ingest -> Stage 1 -> Tech Pack Router -> Stage 2A
    graph.add_edge("ingest_pdfs", "stage1_extraction")
    graph.add_edge("stage1_extraction", "tech_pack_router")
    graph.add_edge("tech_pack_router", "stage2a")

    # Stage 2A -> Stage 2B and Stage 2C (can run in parallel conceptually,
    # but LangGraph will execute them sequentially by default)
    graph.add_edge("stage2a", "stage2b")
    graph.add_edge("stage2b", "stage2c")

    # Stage 2B and 2C -> Stage 2 Merge
    graph.add_edge("stage2c", "stage2_merge")

    # Stage 2 Merge -> Stage 3 and Search Intel (parallel branches)
    graph.add_edge("stage2_merge", "stage3_report")
    graph.add_edge("stage2_merge", "search_intel")

    # Stage 3 -> Stage 4
    graph.add_edge("stage3_report", "stage4_qc")

    # Stage 4 and Search Intel -> Save Reports
    graph.add_edge("stage4_qc", "save_reports")
    graph.add_edge("search_intel", "save_reports")

    # Save Reports -> END
    graph.add_edge("save_reports", END)

    logger.info("Patent pipeline graph created")

    return graph.compile()


# Create the compiled pipeline as a module-level singleton
patent_pipeline = create_patent_pipeline()


def run_patent_pipeline(
    patent_pdf_url: str,
    history_pdf_url: str,
) -> PatentPipelineState:
    """Run the patent litigation report pipeline.

    Args:
        patent_pdf_url: Azure Blob URL for the issued patent PDF
        history_pdf_url: Azure Blob URL for the prosecution history PDF

    Returns:
        Final pipeline state with report URLs
    """
    logger.info(
        "Starting patent pipeline",
        patent_pdf_url=patent_pdf_url[:50] + "...",
        history_pdf_url=history_pdf_url[:50] + "...",
    )

    initial_state: PatentPipelineState = {
        "patent_pdf_url": patent_pdf_url,
        "history_pdf_url": history_pdf_url,
        "status": "pending",
    }

    # Run the pipeline
    result = patent_pipeline.invoke(initial_state)

    logger.info(
        "Patent pipeline completed",
        status=result.get("status"),
        stage3_url=result.get("stage3_url"),
        stage4_url=result.get("stage4_url"),
        search_intel_url=result.get("search_intel_url"),
    )

    return result

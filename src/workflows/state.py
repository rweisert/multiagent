"""Workflow state definitions for patent pipeline."""

from typing import Any, TypedDict


class PatentWorkflowState(TypedDict, total=False):
    """State for the agent-based patent workflow.

    This state flows through all agents in the pipeline.
    """

    # Input
    patent_pdf_url: str
    history_pdf_url: str
    patent_pdf_bytes: bytes
    history_pdf_bytes: bytes

    # Pipeline tracking
    current_stage: str  # start, extracted, analyzed, written, qc_complete, revised, clarified, finalized
    status: str  # pending, running, completed, failed
    error: str | None

    # Iteration tracking
    revision_count: int
    clarification_count: int

    # Tech pack
    tech_center: str
    tech_pack_content: str

    # Stage 1 - Extraction (Extractor Agent)
    extraction: dict[str, Any]

    # Stage 2 - Analysis (Analyst Agent)
    forensic_analysis: dict[str, Any]
    clarification_answers: dict[str, Any]

    # Stage 3 - Report (Writer Agent)
    report: str
    report_history: list[str]  # Previous versions for tracking

    # Stage 4 - QC (QC Agent)
    qc_result: dict[str, Any]
    qc_score: int
    qc_passed: bool
    needs_revision: bool
    needs_clarification: bool
    clarification_questions: list[str]
    corrected_report: str

    # Final output
    final_report: str
    stage3_url: str
    stage4_url: str
    search_intel_url: str


def create_initial_state(
    patent_pdf_url: str,
    history_pdf_url: str,
) -> PatentWorkflowState:
    """Create initial workflow state.

    Args:
        patent_pdf_url: URL to the issued patent PDF
        history_pdf_url: URL to the prosecution history PDF

    Returns:
        Initial PatentWorkflowState
    """
    return PatentWorkflowState(
        patent_pdf_url=patent_pdf_url,
        history_pdf_url=history_pdf_url,
        patent_pdf_bytes=b"",
        history_pdf_bytes=b"",
        current_stage="start",
        status="pending",
        error=None,
        revision_count=0,
        clarification_count=0,
        tech_center="2100",  # Default, will be detected
        tech_pack_content="",
        extraction={},
        forensic_analysis={},
        clarification_answers={},
        report="",
        report_history=[],
        qc_result={},
        qc_score=0,
        qc_passed=False,
        needs_revision=False,
        needs_clarification=False,
        clarification_questions=[],
        corrected_report="",
        final_report="",
        stage3_url="",
        stage4_url="",
        search_intel_url="",
    )

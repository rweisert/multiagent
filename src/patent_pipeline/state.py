"""Patent Pipeline State Definition for LangGraph."""

from typing import Any, TypedDict


class PatentPipelineState(TypedDict, total=False):
    """State for the patent litigation report pipeline workflow.

    This state flows through all pipeline stages, accumulating data from
    each processing step.
    """

    # Input URLs (required)
    patent_pdf_url: str
    history_pdf_url: str

    # Ingested binary data
    patent_pdf_bytes: bytes
    history_pdf_bytes: bytes

    # Azure blob info (derived from input URLs)
    azure_container_url: str
    base_name: str  # e.g., "APPNO" derived from history filename

    # Tech pack routing
    tech_center: str | None
    tech_pack_name: str | None
    tech_pack_content: str | None

    # Stage 1 - Record Extraction Output
    stage1_extraction: dict[str, Any]
    # Contains: metadata, events, claims_diff, key_quotes, search_records, record_discrepancies

    # Stage 2A - Claim Construction & Estoppel Output
    stage2a: dict[str, Any]
    # Contains: claim_construction_rows, estoppel_matrix_rows

    # Stage 2B - Search & Technical Premise Output
    stage2b: dict[str, Any]
    # Contains: technical_reps, convergence_rows, search_gap_analysis

    # Stage 2C - Timeline & Global Synthesis Output
    stage2c: dict[str, Any]
    # Contains: event_forensics, global_findings

    # Stage 2 Merged Output
    stage2_forensic: dict[str, Any]
    # Union of stage2a, stage2b, stage2c

    # Stage 3 - Report Generation Output
    stage3_report_md: str

    # Stage 4 - QC & Verification Output
    stage4_qc_json: dict[str, Any]
    stage4_final_report_md: str

    # Search Intelligence Report (Pipeline 2 sidecar)
    search_intel_report_md: str | None

    # Final output URLs (populated after saving to Azure)
    stage3_url: str | None
    stage4_url: str | None
    search_intel_url: str | None

    # Pipeline metadata
    error: str | None
    status: str  # "pending", "processing", "completed", "failed"

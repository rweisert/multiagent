"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field, HttpUrl


class GenerateReportRequest(BaseModel):
    """Request model for generating patent litigation reports."""

    patent_pdf_url: str = Field(
        ...,
        description="Azure Blob URL for the issued patent PDF",
        examples=["https://account.blob.core.windows.net/container/patent.pdf"],
    )
    history_pdf_url: str = Field(
        ...,
        description="Azure Blob URL for the combined prosecution history PDF",
        examples=["https://account.blob.core.windows.net/container/wrapper.pdf"],
    )
    tech_center_override: str | None = Field(
        None,
        description="Optional tech center override (e.g., '2100', '2600')",
    )


class GenerateReportResponse(BaseModel):
    """Response model for generated patent litigation reports."""

    stage3_url: str = Field(
        ...,
        description="Azure Blob URL for Stage 3 main report",
    )
    stage4_url: str = Field(
        ...,
        description="Azure Blob URL for Stage 4 final QC'd report",
    )
    search_intel_url: str | None = Field(
        None,
        description="Azure Blob URL for Search Intelligence report (Pipeline 2)",
    )
    pipeline_status: str = Field(
        "completed",
        description="Pipeline execution status",
    )
    qc_score: float | None = Field(
        None,
        description="Overall QC score from Stage 4 (0-100)",
    )


class PipelineStatusResponse(BaseModel):
    """Response model for pipeline status queries."""

    job_id: str = Field(..., description="Pipeline job identifier")
    status: str = Field(
        ...,
        description="Status: pending, processing, completed, failed",
    )
    current_stage: str | None = Field(
        None,
        description="Current processing stage",
    )
    progress_percent: float = Field(
        0.0,
        description="Estimated progress percentage",
    )
    error_message: str | None = Field(
        None,
        description="Error message if failed",
    )
    result: GenerateReportResponse | None = Field(
        None,
        description="Result if completed",
    )

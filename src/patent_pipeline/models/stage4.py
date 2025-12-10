"""Pydantic models for Stage 4 - QC & Verification."""

from pydantic import BaseModel, Field


class Stage4QCIssue(BaseModel):
    """A QC issue identified during verification."""

    issue_id: str = Field(..., description="Unique issue identifier")
    issue_type: str = Field(
        ...,
        description="Type: factual_error, inconsistency, missing_info, formatting, citation_error",
    )
    severity: str = Field(..., description="low, medium, high, or critical")
    location: str = Field(..., description="Location in report (section/paragraph)")
    description: str = Field(..., description="Description of the issue")
    source_data_reference: str = Field(
        ..., description="Reference to source data (Stage 1/2)"
    )
    suggested_correction: str = Field(..., description="Suggested correction")
    corrected: bool = Field(False, description="Whether correction was applied")


class Stage4QCMetrics(BaseModel):
    """QC metrics summary."""

    total_issues_found: int = Field(0, description="Total issues found")
    critical_issues: int = Field(0, description="Critical issues count")
    high_issues: int = Field(0, description="High severity issues count")
    medium_issues: int = Field(0, description="Medium severity issues count")
    low_issues: int = Field(0, description="Low severity issues count")
    issues_corrected: int = Field(0, description="Issues corrected")
    factual_accuracy_score: float = Field(
        0.0, description="Factual accuracy score (0-100)"
    )
    completeness_score: float = Field(
        0.0, description="Completeness score (0-100)"
    )
    consistency_score: float = Field(
        0.0, description="Internal consistency score (0-100)"
    )
    overall_quality_score: float = Field(
        0.0, description="Overall quality score (0-100)"
    )


class Stage4QCVerification(BaseModel):
    """Verification checklist item."""

    check_id: str = Field(..., description="Check identifier")
    check_description: str = Field(..., description="What was verified")
    result: str = Field(..., description="pass, fail, or warning")
    notes: str = Field("", description="Additional notes")


class Stage4QC(BaseModel):
    """Stage 4 - QC & Verification output."""

    qc_issues: list[Stage4QCIssue] = Field(
        default_factory=list, description="List of QC issues found"
    )
    metrics: Stage4QCMetrics = Field(
        default_factory=Stage4QCMetrics, description="QC metrics summary"
    )
    verifications: list[Stage4QCVerification] = Field(
        default_factory=list, description="Verification checklist results"
    )
    qc_summary: str = Field("", description="QC summary narrative")
    recommendations: list[str] = Field(
        default_factory=list, description="Final recommendations"
    )
    approved_for_delivery: bool = Field(
        False, description="Whether report passes QC for delivery"
    )

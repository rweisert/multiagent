"""Pydantic models for Stage 2 - Analysis Stages."""

from pydantic import BaseModel, Field


# Stage 2A Models - Claim Construction & Estoppel


class ClaimConstructionRow(BaseModel):
    """A claim term construction analysis row."""

    claim_number: int = Field(..., description="Claim number")
    claim_term: str = Field(..., description="The claim term being construed")
    plain_meaning: str = Field(..., description="Plain/ordinary meaning")
    specification_support: str = Field(..., description="Support from specification")
    prosecution_history_context: str = Field(
        ..., description="Relevant prosecution history context"
    )
    proposed_construction: str = Field(..., description="Proposed claim construction")
    construction_rationale: str = Field(..., description="Rationale for construction")
    potential_disputes: list[str] = Field(
        default_factory=list, description="Potential construction disputes"
    )
    related_prior_art: list[str] = Field(
        default_factory=list, description="Prior art affecting construction"
    )


class EstoppelMatrixRow(BaseModel):
    """A prosecution history estoppel analysis row."""

    claim_number: int = Field(..., description="Affected claim number")
    amendment_date: str = Field(..., description="Date of narrowing amendment")
    original_language: str = Field(..., description="Original claim language")
    amended_language: str = Field(..., description="Amended claim language")
    reason_for_amendment: str = Field(
        ..., description="Stated reason for amendment (examiner rejection/applicant argument)"
    )
    surrendered_scope: str = Field(
        ..., description="Description of surrendered claim scope"
    )
    estoppel_strength: str = Field(..., description="weak, moderate, or strong")
    litigation_impact: str = Field(..., description="Impact on infringement analysis")
    doctrine_of_equivalents_risk: str = Field(
        ..., description="Risk to DOE arguments"
    )
    supporting_quotes: list[str] = Field(
        default_factory=list, description="Key quotes supporting estoppel finding"
    )


class Stage2A(BaseModel):
    """Stage 2A - Claim Construction & Estoppel output."""

    claim_construction_rows: list[ClaimConstructionRow] = Field(default_factory=list)
    estoppel_matrix_rows: list[EstoppelMatrixRow] = Field(default_factory=list)
    construction_summary: str = Field(
        "", description="Executive summary of construction issues"
    )
    estoppel_summary: str = Field(
        "", description="Executive summary of estoppel issues"
    )


# Stage 2B Models - Search & Technical Premise


class TechnicalRep(BaseModel):
    """A technical representation/premise from prosecution."""

    rep_id: str = Field(..., description="Unique identifier for this rep")
    source_document: str = Field(..., description="Source document/date")
    representation_text: str = Field(..., description="The technical representation made")
    context: str = Field(..., description="Context in which representation was made")
    technical_accuracy: str = Field(
        ..., description="Assessment of technical accuracy"
    )
    potential_misrepresentation: bool = Field(
        False, description="Whether this could be a misrepresentation"
    )
    attack_vector: str | None = Field(
        None, description="Potential attack vector if misrepresentation"
    )
    related_claims: list[int] = Field(default_factory=list, description="Related claims")


class SearchGapEntry(BaseModel):
    """A gap identified in prior art search."""

    gap_type: str = Field(
        ..., description="Type: database_gap, temporal_gap, foreign_art_gap, etc."
    )
    description: str = Field(..., description="Description of the gap")
    affected_claims: list[int] = Field(default_factory=list)
    severity: str = Field("medium", description="low, medium, or high")
    recommended_search: str = Field(..., description="Recommended additional search")


class ConvergenceRow(BaseModel):
    """A prior art convergence analysis row."""

    convergence_id: str = Field(..., description="Unique identifier")
    primary_reference: str = Field(..., description="Primary prior art reference")
    secondary_references: list[str] = Field(
        default_factory=list, description="Secondary references for combination"
    )
    claim_elements_addressed: list[str] = Field(
        default_factory=list, description="Claim elements addressed by combination"
    )
    missing_elements: list[str] = Field(
        default_factory=list, description="Elements not addressed"
    )
    combination_rationale: str = Field(
        ..., description="Rationale for combining references"
    )
    obviousness_strength: str = Field(..., description="weak, moderate, or strong")
    affected_claims: list[int] = Field(default_factory=list)


class Stage2B(BaseModel):
    """Stage 2B - Search & Technical Premise output."""

    technical_reps: list[TechnicalRep] = Field(default_factory=list)
    search_gap_analysis: list[SearchGapEntry] = Field(default_factory=list)
    convergence_rows: list[ConvergenceRow] = Field(default_factory=list)
    technical_summary: str = Field(
        "", description="Executive summary of technical issues"
    )
    search_summary: str = Field(
        "", description="Executive summary of search gaps"
    )


# Stage 2C Models - Timeline & Global Synthesis


class EventForensic(BaseModel):
    """Forensic analysis of a prosecution event."""

    event_date: str = Field(..., description="Event date")
    event_type: str = Field(..., description="Type of event")
    forensic_significance: str = Field(
        ..., description="Why this event is forensically significant"
    )
    timeline_anomalies: list[str] = Field(
        default_factory=list, description="Any timeline anomalies detected"
    )
    related_events: list[str] = Field(
        default_factory=list, description="Related prosecution events"
    )
    litigation_relevance: str = Field(..., description="Relevance to litigation")
    evidence_quality: str = Field(..., description="low, medium, or high")


class GlobalFindings(BaseModel):
    """Global synthesis findings across all prosecution."""

    overall_prosecution_quality: str = Field(
        ..., description="Assessment of prosecution quality"
    )
    key_vulnerabilities: list[str] = Field(
        default_factory=list, description="Key patent vulnerabilities"
    )
    key_strengths: list[str] = Field(
        default_factory=list, description="Key patent strengths"
    )
    recommended_focus_areas: list[str] = Field(
        default_factory=list, description="Recommended focus for litigation"
    )
    invalidity_attack_strength: str = Field(
        ..., description="Overall invalidity attack strength assessment"
    )
    infringement_defense_strength: str = Field(
        ..., description="Overall infringement defense strength"
    )
    critical_dates: list[dict] = Field(
        default_factory=list, description="Critical dates for litigation"
    )
    examiner_patterns: str | None = Field(
        None, description="Notable examiner behavior patterns"
    )


class Stage2C(BaseModel):
    """Stage 2C - Timeline & Global Synthesis output."""

    event_forensics: list[EventForensic] = Field(default_factory=list)
    global_findings: GlobalFindings | None = None
    timeline_summary: str = Field(
        "", description="Executive summary of timeline analysis"
    )


class Stage2Forensic(BaseModel):
    """Merged Stage 2 forensic output (union of 2A, 2B, 2C)."""

    # From Stage 2A
    claim_construction_rows: list[ClaimConstructionRow] = Field(default_factory=list)
    estoppel_matrix_rows: list[EstoppelMatrixRow] = Field(default_factory=list)
    construction_summary: str = ""
    estoppel_summary: str = ""

    # From Stage 2B
    technical_reps: list[TechnicalRep] = Field(default_factory=list)
    search_gap_analysis: list[SearchGapEntry] = Field(default_factory=list)
    convergence_rows: list[ConvergenceRow] = Field(default_factory=list)
    technical_summary: str = ""
    search_summary: str = ""

    # From Stage 2C
    event_forensics: list[EventForensic] = Field(default_factory=list)
    global_findings: GlobalFindings | None = None
    timeline_summary: str = ""

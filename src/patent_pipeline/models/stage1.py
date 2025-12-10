"""Pydantic models for Stage 1 - Record Extraction."""

from pydantic import BaseModel, Field


class Stage1Metadata(BaseModel):
    """Metadata extracted from the prosecution history."""

    application_number: str = Field(..., description="Patent application number")
    patent_number: str | None = Field(None, description="Issued patent number if available")
    filing_date: str | None = Field(None, description="Original filing date")
    issue_date: str | None = Field(None, description="Patent issue date if issued")
    title: str = Field(..., description="Invention title")
    inventors: list[str] = Field(default_factory=list, description="List of inventors")
    assignee: str | None = Field(None, description="Current assignee/owner")
    art_unit: str | None = Field(None, description="USPTO art unit")
    tech_center: str | None = Field(None, description="Technology center code")
    examiner: str | None = Field(None, description="Primary examiner name")
    cpc_classifications: list[str] = Field(
        default_factory=list, description="CPC classification codes"
    )
    uspc_classifications: list[str] = Field(
        default_factory=list, description="USPC classification codes"
    )
    priority_claims: list[str] = Field(
        default_factory=list, description="Priority claim references"
    )
    related_applications: list[str] = Field(
        default_factory=list, description="Related application numbers"
    )


class Stage1Event(BaseModel):
    """A prosecution history event."""

    date: str = Field(..., description="Event date (YYYY-MM-DD format)")
    document_code: str = Field(..., description="USPTO document code")
    document_description: str = Field(..., description="Document description")
    document_type: str = Field(
        ..., description="Type: office_action, response, amendment, interview, etc."
    )
    page_range: str | None = Field(None, description="Page range in file wrapper")
    key_content: str | None = Field(None, description="Summary of key content")
    examiner_rejections: list[str] = Field(
        default_factory=list, description="Rejection types/citations in this document"
    )
    applicant_arguments: list[str] = Field(
        default_factory=list, description="Key arguments made by applicant"
    )
    claim_amendments: list[str] = Field(
        default_factory=list, description="Claims amended in this document"
    )


class ClaimsDiffEntry(BaseModel):
    """A claim difference entry tracking claim evolution."""

    claim_number: int = Field(..., description="Claim number")
    claim_type: str = Field(..., description="independent or dependent")
    original_text: str | None = Field(None, description="Original claim text")
    final_text: str = Field(..., description="Final/current claim text")
    amendments: list[dict] = Field(
        default_factory=list,
        description="List of amendments with date, reason, and changes",
    )
    prosecution_history_estoppel_risk: str = Field(
        "low", description="low, medium, or high"
    )


class KeyQuoteEntry(BaseModel):
    """A key quote from prosecution history."""

    quote: str = Field(..., description="The exact quote")
    source_document: str = Field(..., description="Source document name/date")
    page_number: str | None = Field(None, description="Page number in file wrapper")
    context: str = Field(..., description="Context/significance of the quote")
    relevance: str = Field(..., description="Why this quote matters for litigation")


class KeyQuotes(BaseModel):
    """Collection of key quotes categorized by type."""

    examiner_statements: list[KeyQuoteEntry] = Field(default_factory=list)
    applicant_statements: list[KeyQuoteEntry] = Field(default_factory=list)
    claim_scope_discussions: list[KeyQuoteEntry] = Field(default_factory=list)
    prior_art_discussions: list[KeyQuoteEntry] = Field(default_factory=list)
    interview_summaries: list[KeyQuoteEntry] = Field(default_factory=list)


class SearchRecord(BaseModel):
    """A prior art search record."""

    search_date: str = Field(..., description="Date of search")
    search_query: str | None = Field(None, description="Search query/terms used")
    databases_searched: list[str] = Field(default_factory=list, description="Databases searched")
    prior_art_found: list[dict] = Field(
        default_factory=list,
        description="Prior art references found with citation details",
    )
    search_notes: str | None = Field(None, description="Examiner search notes")


class SearchRecords(BaseModel):
    """Collection of search records."""

    examiner_searches: list[SearchRecord] = Field(default_factory=list)
    isd_searches: list[SearchRecord] = Field(default_factory=list)
    ids_submissions: list[dict] = Field(
        default_factory=list, description="IDS submission records"
    )


class RecordDiscrepancy(BaseModel):
    """A discrepancy or issue found in the record."""

    discrepancy_type: str = Field(
        ..., description="Type: missing_document, date_inconsistency, etc."
    )
    description: str = Field(..., description="Description of the discrepancy")
    affected_documents: list[str] = Field(default_factory=list)
    severity: str = Field("medium", description="low, medium, or high")
    potential_impact: str = Field(..., description="Potential impact on litigation")


class Stage1Extraction(BaseModel):
    """Complete Stage 1 extraction output."""

    metadata: Stage1Metadata
    events: list[Stage1Event] = Field(
        default_factory=list, description="Chronological prosecution events"
    )
    claims_diff: list[ClaimsDiffEntry] = Field(
        default_factory=list, description="Claim evolution tracking"
    )
    key_quotes: KeyQuotes = Field(
        default_factory=KeyQuotes, description="Categorized key quotes"
    )
    search_records: SearchRecords = Field(
        default_factory=SearchRecords, description="Prior art search records"
    )
    record_discrepancies: list[RecordDiscrepancy] = Field(
        default_factory=list, description="Record issues found"
    )

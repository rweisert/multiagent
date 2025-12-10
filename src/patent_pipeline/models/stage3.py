"""Pydantic models for Stage 3 - Report Generation."""

from pydantic import BaseModel, Field


class ReportSection(BaseModel):
    """A section of the litigation report."""

    section_number: int = Field(..., description="Section number (1-10)")
    section_title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content in markdown")
    subsections: list[dict] = Field(
        default_factory=list, description="Subsections if any"
    )


class Stage3Report(BaseModel):
    """Stage 3 - Report Generation output structure.

    The actual output is markdown text (stage3_report_md in state),
    but this model can be used for structured parsing if needed.
    """

    title: str = Field(..., description="Report title")
    executive_summary: str = Field(..., description="Executive summary")
    sections: list[ReportSection] = Field(
        default_factory=list,
        description="10 main report sections",
    )

    # Standard 10-section structure for litigation reports:
    # 1. Patent Overview
    # 2. Prosecution History Summary
    # 3. Claim Construction Analysis
    # 4. Prosecution History Estoppel
    # 5. Prior Art Analysis
    # 6. Technical Representations
    # 7. Timeline Analysis
    # 8. Invalidity Considerations
    # 9. Infringement Considerations
    # 10. Conclusions & Recommendations

    full_markdown: str = Field("", description="Complete report as markdown")

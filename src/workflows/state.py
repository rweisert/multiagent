"""Workflow state definitions using TypedDict for LangGraph."""

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class ContentPipelineState(TypedDict):
    """State for the content creation pipeline workflow."""

    # Input
    topic: str
    style: str
    audience: str

    # Messages (for agent communication)
    messages: Annotated[list[BaseMessage], add_messages]

    # Research phase
    research_findings: str
    research_complete: bool

    # Writing phase
    draft_content: str
    writing_complete: bool

    # Review phase
    review_feedback: str
    review_score: int
    review_complete: bool

    # Final output
    final_content: str
    status: str
    iteration_count: int


class ResearchState(TypedDict):
    """State for a research-focused workflow."""

    # Input
    query: str
    depth: str  # 'quick', 'standard', 'deep'

    # Messages
    messages: Annotated[list[BaseMessage], add_messages]

    # Research phases
    initial_findings: str
    detailed_analysis: str
    sources: list[str]

    # Output
    final_report: str
    status: str

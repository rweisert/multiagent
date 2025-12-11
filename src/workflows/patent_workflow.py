"""Agent-based patent workflow using LangGraph."""

from typing import Literal

import structlog
from langgraph.graph import StateGraph, END

from src.agents import (
    ExtractorAgent,
    AnalystAgent,
    WriterAgent,
    QCAgent,
    SupervisorAgent,
    load_tech_pack,
)
from src.workflows.state import PatentWorkflowState, create_initial_state
from src.patent_pipeline.services.azure_io import download_blob, upload_report

logger = structlog.get_logger(__name__)


class PatentWorkflow:
    """Agent-based workflow for patent litigation report generation.

    Pipeline flow with revision loops:

    ```
    Ingest → Extract → Analyze → Write → QC
                                   ↑      ↓
                                   ├──────┤ (revision loop)
                                   ↓      ↓
                              Clarify   Finalize
    ```

    Agents:
    - Extractor: Stage 1 - PDF parsing (Gemini)
    - Analyst: Stage 2 - Legal/technical analysis (Gemini)
    - Writer: Stage 3 - Report generation (Claude)
    - QC: Stage 4 - Quality verification (Claude)
    - Supervisor: Routing decisions
    """

    def __init__(self) -> None:
        """Initialize the workflow with all agents."""
        self.extractor = ExtractorAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()
        self.qc = QCAgent()
        self.supervisor = SupervisorAgent()
        self._graph = None

        logger.info("PatentWorkflow initialized with agents")

    # --- Node Functions ---

    async def ingest_node(self, state: PatentWorkflowState) -> dict:
        """Download PDFs from Azure storage."""
        logger.info("Ingesting PDFs")

        try:
            history_pdf_bytes = download_blob(state["history_pdf_url"])
            patent_pdf_bytes = None
            if state.get("patent_pdf_url"):
                patent_pdf_bytes = download_blob(state["patent_pdf_url"])

            return {
                "history_pdf_bytes": history_pdf_bytes,
                "patent_pdf_bytes": patent_pdf_bytes or b"",
                "current_stage": "ingested",
                "status": "running",
            }
        except Exception as e:
            logger.error("Ingest failed", error=str(e))
            return {
                "status": "failed",
                "error": f"Ingest failed: {str(e)}",
            }

    async def extract_node(self, state: PatentWorkflowState) -> dict:
        """Run Extractor agent for Stage 1."""
        logger.info("Running Extractor agent")

        result = await self.extractor.process({
            "history_pdf_bytes": state["history_pdf_bytes"],
            "patent_pdf_bytes": state.get("patent_pdf_bytes"),
        })

        if result["status"] == "failed":
            return {
                "status": "failed",
                "error": result.get("error", "Extraction failed"),
            }

        # Detect tech center from extraction
        tech_center = self._detect_tech_center(result["extraction"])

        return {
            "extraction": result["extraction"],
            "tech_center": tech_center,
            "current_stage": "extracted",
        }

    def _detect_tech_center(self, extraction: dict) -> str:
        """Detect tech center from extraction data."""
        # Look for tech center in patent metadata
        patent_info = extraction.get("patent_info", {})
        class_info = patent_info.get("classification", "")

        # Simple mapping based on classification
        if "G06" in class_info or "software" in str(extraction).lower():
            return "2100"
        elif "H04" in class_info or "communication" in str(extraction).lower():
            return "2600"
        elif "H01" in class_info or "semiconductor" in str(extraction).lower():
            return "2800"

        return "2100"  # Default to software

    async def analyze_node(self, state: PatentWorkflowState) -> dict:
        """Run Analyst agent for Stage 2 (parallel sub-stages)."""
        logger.info("Running Analyst agent")

        try:
            tech_pack_content = load_tech_pack(state.get("tech_center", "2100"))
        except FileNotFoundError:
            tech_pack_content = ""

        result = await self.analyst.process({
            "extraction": state["extraction"],
            "tech_center": state.get("tech_center", "2100"),
            "mode": "full",  # Runs 2A, then 2B/2C in parallel
        })

        if result["status"] == "failed":
            return {
                "status": "failed",
                "error": result.get("error", "Analysis failed"),
            }

        return {
            "forensic_analysis": result["forensic_analysis"],
            "tech_pack_content": tech_pack_content,
            "current_stage": "analyzed",
        }

    async def write_node(self, state: PatentWorkflowState) -> dict:
        """Run Writer agent for Stage 3."""
        logger.info("Running Writer agent", revision_count=state.get("revision_count", 0))

        # Check if this is a revision
        is_revision = state.get("current_stage") == "qc_complete" or state.get("revision_count", 0) > 0

        if is_revision and state.get("report"):
            # Revision mode
            result = await self.writer.process({
                "extraction": state["extraction"],
                "forensic_analysis": state["forensic_analysis"],
                "mode": "revise",
                "original_report": state["report"],
                "feedback": state.get("qc_result", {}),
            })
        else:
            # Initial generation
            result = await self.writer.process({
                "extraction": state["extraction"],
                "forensic_analysis": state["forensic_analysis"],
                "mode": "generate",
            })

        if result["status"] == "failed":
            return {
                "status": "failed",
                "error": result.get("error", "Report generation failed"),
            }

        # Track report history
        report_history = state.get("report_history", [])
        if state.get("report"):
            report_history.append(state["report"])

        return {
            "report": result["report"],
            "report_history": report_history,
            "current_stage": "written",
        }

    async def qc_node(self, state: PatentWorkflowState) -> dict:
        """Run QC agent for Stage 4."""
        logger.info("Running QC agent")

        result = await self.qc.process({
            "report": state["report"],
            "extraction": state["extraction"],
            "forensic_analysis": state["forensic_analysis"],
        })

        if result["status"] == "failed":
            return {
                "status": "failed",
                "error": result.get("error", "QC verification failed"),
            }

        return {
            "qc_result": result["qc_result"],
            "qc_score": result["score"],
            "qc_passed": result["passed"],
            "needs_revision": result["needs_revision"],
            "needs_clarification": result["needs_clarification"],
            "clarification_questions": result["clarification_questions"],
            "corrected_report": result["corrected_report"],
            "current_stage": "qc_complete",
        }

    async def clarify_node(self, state: PatentWorkflowState) -> dict:
        """Run Analyst agent for clarification."""
        logger.info("Running Analyst agent for clarification")

        result = await self.analyst.process({
            "extraction": state["extraction"],
            "mode": "clarify",
            "questions": state.get("clarification_questions", []),
        })

        clarification_count = state.get("clarification_count", 0) + 1

        return {
            "clarification_answers": result.get("answers", {}),
            "clarification_count": clarification_count,
            "current_stage": "clarified",
        }

    async def revise_node(self, state: PatentWorkflowState) -> dict:
        """Update state for revision loop."""
        revision_count = state.get("revision_count", 0) + 1
        logger.info("Preparing for revision", revision_count=revision_count)

        return {
            "revision_count": revision_count,
            "current_stage": "qc_complete",  # Will route to write via supervisor
        }

    async def finalize_node(self, state: PatentWorkflowState) -> dict:
        """Finalize the report and save to storage."""
        logger.info("Finalizing report")

        # Use corrected report from QC if available, otherwise use last report
        final_report = state.get("corrected_report") or state.get("report", "")

        # Upload to Azure (if configured)
        stage3_url = ""
        stage4_url = ""
        try:
            if final_report:
                # Generate a unique report ID
                import uuid
                report_id = str(uuid.uuid4())[:8]

                stage3_url = upload_report(
                    final_report,
                    f"reports/{report_id}_stage3_report.md",
                )
                stage4_url = upload_report(
                    str(state.get("qc_result", {})),
                    f"reports/{report_id}_stage4_qc.json",
                )
        except Exception as e:
            logger.warning("Failed to upload reports", error=str(e))

        return {
            "final_report": final_report,
            "stage3_url": stage3_url,
            "stage4_url": stage4_url,
            "current_stage": "finalized",
            "status": "completed",
        }

    # --- Routing Functions ---

    def route_after_qc(self, state: PatentWorkflowState) -> Literal["revise", "clarify", "finalize"]:
        """Route based on QC results using Supervisor logic."""
        decision = self.supervisor.decide_next_action(state)
        action = decision["action"]

        logger.info("Routing after QC", action=action, reason=decision["reason"])

        if action == "revise":
            return "revise"
        elif action == "clarify":
            return "clarify"
        else:
            return "finalize"

    def route_after_clarify(self, state: PatentWorkflowState) -> Literal["write", "finalize"]:
        """Route after clarification."""
        decision = self.supervisor.decide_next_action(state)
        action = decision["action"]

        if action == "write":
            return "write"
        return "finalize"

    # --- Graph Construction ---

    def build_graph(self) -> StateGraph:
        """Build the workflow graph."""
        if self._graph is not None:
            return self._graph

        workflow = StateGraph(PatentWorkflowState)

        # Add nodes
        workflow.add_node("ingest", self.ingest_node)
        workflow.add_node("extract", self.extract_node)
        workflow.add_node("analyze", self.analyze_node)
        workflow.add_node("write", self.write_node)
        workflow.add_node("qc", self.qc_node)
        workflow.add_node("clarify", self.clarify_node)
        workflow.add_node("revise", self.revise_node)
        workflow.add_node("finalize", self.finalize_node)

        # Set entry point
        workflow.set_entry_point("ingest")

        # Linear flow: ingest -> extract -> analyze -> write -> qc
        workflow.add_edge("ingest", "extract")
        workflow.add_edge("extract", "analyze")
        workflow.add_edge("analyze", "write")
        workflow.add_edge("write", "qc")

        # Conditional routing after QC
        workflow.add_conditional_edges(
            "qc",
            self.route_after_qc,
            {
                "revise": "revise",
                "clarify": "clarify",
                "finalize": "finalize",
            },
        )

        # Revise goes back to write
        workflow.add_edge("revise", "write")

        # Clarify routes back to write or finalize
        workflow.add_conditional_edges(
            "clarify",
            self.route_after_clarify,
            {
                "write": "write",
                "finalize": "finalize",
            },
        )

        # Finalize ends the workflow
        workflow.add_edge("finalize", END)

        self._graph = workflow
        return workflow

    def compile(self):
        """Compile the workflow for execution."""
        return self.build_graph().compile()

    async def run(
        self,
        patent_pdf_url: str,
        history_pdf_url: str,
    ) -> PatentWorkflowState:
        """Run the patent workflow.

        Args:
            patent_pdf_url: URL to the issued patent PDF
            history_pdf_url: URL to the prosecution history PDF

        Returns:
            Final workflow state
        """
        logger.info(
            "Starting patent workflow",
            patent_pdf_url=patent_pdf_url[:50] + "..." if len(patent_pdf_url) > 50 else patent_pdf_url,
            history_pdf_url=history_pdf_url[:50] + "..." if len(history_pdf_url) > 50 else history_pdf_url,
        )

        app = self.compile()
        initial_state = create_initial_state(patent_pdf_url, history_pdf_url)

        result = await app.ainvoke(initial_state)

        logger.info(
            "Patent workflow completed",
            status=result.get("status"),
            qc_score=result.get("qc_score"),
            revision_count=result.get("revision_count"),
        )

        return result


# Create singleton instance
patent_workflow = PatentWorkflow()


async def run_patent_workflow(
    patent_pdf_url: str,
    history_pdf_url: str,
) -> PatentWorkflowState:
    """Run the patent workflow (convenience function).

    Args:
        patent_pdf_url: URL to the issued patent PDF
        history_pdf_url: URL to the prosecution history PDF

    Returns:
        Final workflow state
    """
    return await patent_workflow.run(patent_pdf_url, history_pdf_url)

"""Research-focused workflow using LangGraph."""

from langgraph.graph import END, StateGraph

from src.agents import ResearcherAgent, ReviewerAgent
from src.workflows.state import ResearchState


class ResearchWorkflow:
    """Multi-agent workflow for in-depth research.

    Pipeline: Initial Research -> Deep Analysis -> Review -> Report
    """

    def __init__(self) -> None:
        """Initialize the research workflow."""
        self.researcher = ResearcherAgent()
        self.reviewer = ReviewerAgent()
        self._graph: StateGraph | None = None

    async def initial_research_node(self, state: ResearchState) -> dict:
        """Perform initial research on the query."""
        result = await self.researcher.process({
            "topic": state["query"],
            "context": f"Initial research phase - {state['depth']} depth requested",
        })

        return {
            "initial_findings": result["findings"],
            "sources": [],  # Would be populated with real search results
        }

    async def deep_analysis_node(self, state: ResearchState) -> dict:
        """Perform deep analysis based on initial findings."""
        # Skip deep analysis for quick searches
        if state["depth"] == "quick":
            return {
                "detailed_analysis": state["initial_findings"],
            }

        prompt = f"""Based on the initial research findings, provide a deeper analysis.

Initial Findings:
{state['initial_findings']}

Please provide:
1. Deeper insights and connections
2. Critical analysis of the findings
3. Potential implications
4. Areas that need further investigation
"""
        analysis = await self.researcher.invoke(prompt)

        return {
            "detailed_analysis": analysis,
        }

    async def review_node(self, state: ResearchState) -> dict:
        """Review the research for quality and completeness."""
        result = await self.reviewer.process({
            "content": f"""
Research Query: {state['query']}

Initial Findings:
{state['initial_findings']}

Detailed Analysis:
{state['detailed_analysis']}
""",
            "criteria": [
                "Thoroughness of research",
                "Accuracy of information",
                "Quality of analysis",
                "Actionable insights",
            ],
        })

        return {
            "review_feedback": result["review"],
        }

    async def report_node(self, state: ResearchState) -> dict:
        """Generate the final research report."""
        report = f"""# Research Report: {state['query']}

## Executive Summary
{state['initial_findings'][:500]}...

## Detailed Analysis
{state['detailed_analysis']}

## Quality Review
{state.get('review_feedback', 'No review performed')}

## Sources
{chr(10).join(f'- {s}' for s in state.get('sources', ['No sources tracked']))}
"""

        return {
            "final_report": report,
            "status": "completed",
        }

    def build_graph(self) -> StateGraph:
        """Build and return the workflow graph."""
        if self._graph is not None:
            return self._graph

        workflow = StateGraph(ResearchState)

        # Add nodes
        workflow.add_node("initial_research", self.initial_research_node)
        workflow.add_node("deep_analysis", self.deep_analysis_node)
        workflow.add_node("review", self.review_node)
        workflow.add_node("report", self.report_node)

        # Define edges
        workflow.set_entry_point("initial_research")
        workflow.add_edge("initial_research", "deep_analysis")
        workflow.add_edge("deep_analysis", "review")
        workflow.add_edge("review", "report")
        workflow.add_edge("report", END)

        self._graph = workflow
        return workflow

    def compile(self):
        """Compile the workflow for execution."""
        return self.build_graph().compile()

    async def run(self, query: str, depth: str = "standard") -> dict:
        """Run the research workflow."""
        app = self.compile()

        initial_state: ResearchState = {
            "query": query,
            "depth": depth,
            "messages": [],
            "initial_findings": "",
            "detailed_analysis": "",
            "sources": [],
            "final_report": "",
            "status": "started",
        }

        result = await app.ainvoke(initial_state)
        return dict(result)

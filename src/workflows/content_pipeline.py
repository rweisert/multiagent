"""Content creation pipeline workflow using LangGraph."""

from typing import Literal

from langgraph.graph import END, StateGraph

from src.agents import ResearcherAgent, ReviewerAgent, WriterAgent
from src.workflows.state import ContentPipelineState


class ContentPipelineWorkflow:
    """Multi-agent workflow for content creation.

    Pipeline: Research -> Write -> Review -> (Revise if needed) -> Done
    """

    def __init__(self, max_iterations: int = 3) -> None:
        """Initialize the content pipeline workflow."""
        self.max_iterations = max_iterations
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()
        self._graph: StateGraph | None = None

    async def research_node(self, state: ContentPipelineState) -> dict:
        """Execute the research phase."""
        result = await self.researcher.process({
            "topic": state["topic"],
            "context": f"Creating content for {state['audience']} audience in {state['style']} style",
        })

        return {
            "research_findings": result["findings"],
            "research_complete": True,
        }

    async def write_node(self, state: ContentPipelineState) -> dict:
        """Execute the writing phase."""
        result = await self.writer.process({
            "task": f"Write about: {state['topic']}",
            "research": state["research_findings"],
            "style": state["style"],
            "audience": state["audience"],
        })

        return {
            "draft_content": result["content"],
            "writing_complete": True,
        }

    async def review_node(self, state: ContentPipelineState) -> dict:
        """Execute the review phase."""
        result = await self.reviewer.process({
            "content": state["draft_content"],
            "criteria": [
                "Accuracy and factual correctness",
                "Clarity and readability",
                "Engagement and flow",
                f"Appropriate for {state['audience']} audience",
                f"Matches {state['style']} style",
            ],
            "context": f"Topic: {state['topic']}",
        })

        # Parse score from review (simplified)
        review_text = result["review"]
        score = 7  # Default score

        # Try to extract score from review
        if "score" in review_text.lower():
            for i in range(10, 0, -1):
                if f"{i}/10" in review_text or f"{i} out of 10" in review_text.lower():
                    score = i
                    break

        return {
            "review_feedback": review_text,
            "review_score": score,
            "review_complete": True,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    async def revise_node(self, state: ContentPipelineState) -> dict:
        """Revise content based on feedback."""
        result = await self.writer.process({
            "task": f"Revise the following content based on feedback:\n\n"
                    f"Original Content:\n{state['draft_content']}\n\n"
                    f"Feedback:\n{state['review_feedback']}\n\n"
                    f"Please address the feedback and improve the content.",
            "research": state["research_findings"],
            "style": state["style"],
            "audience": state["audience"],
        })

        return {
            "draft_content": result["content"],
            "review_complete": False,  # Reset for another review
        }

    def should_revise(self, state: ContentPipelineState) -> Literal["revise", "finalize"]:
        """Determine if content needs revision or is ready for finalization."""
        score = state.get("review_score", 0)
        iterations = state.get("iteration_count", 0)

        # Approve if score is good enough or max iterations reached
        if score >= 8 or iterations >= self.max_iterations:
            return "finalize"
        return "revise"

    async def finalize_node(self, state: ContentPipelineState) -> dict:
        """Finalize the content."""
        return {
            "final_content": state["draft_content"],
            "status": "completed",
        }

    def build_graph(self) -> StateGraph:
        """Build and return the workflow graph."""
        if self._graph is not None:
            return self._graph

        # Create the graph
        workflow = StateGraph(ContentPipelineState)

        # Add nodes
        workflow.add_node("research", self.research_node)
        workflow.add_node("write", self.write_node)
        workflow.add_node("review", self.review_node)
        workflow.add_node("revise", self.revise_node)
        workflow.add_node("finalize", self.finalize_node)

        # Define edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "write")
        workflow.add_edge("write", "review")

        # Conditional edge after review
        workflow.add_conditional_edges(
            "review",
            self.should_revise,
            {
                "revise": "revise",
                "finalize": "finalize",
            },
        )

        # Revise goes back to review
        workflow.add_edge("revise", "review")

        # Finalize ends the workflow
        workflow.add_edge("finalize", END)

        self._graph = workflow
        return workflow

    def compile(self):
        """Compile the workflow for execution."""
        return self.build_graph().compile()

    async def run(
        self,
        topic: str,
        style: str = "professional",
        audience: str = "general",
    ) -> dict:
        """Run the content pipeline workflow."""
        app = self.compile()

        initial_state: ContentPipelineState = {
            "topic": topic,
            "style": style,
            "audience": audience,
            "messages": [],
            "research_findings": "",
            "research_complete": False,
            "draft_content": "",
            "writing_complete": False,
            "review_feedback": "",
            "review_score": 0,
            "review_complete": False,
            "final_content": "",
            "status": "started",
            "iteration_count": 0,
        }

        result = await app.ainvoke(initial_state)
        return dict(result)

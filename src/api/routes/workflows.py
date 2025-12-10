"""Workflow-related API endpoints."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from src.workflows import ContentPipelineWorkflow, ResearchWorkflow

router = APIRouter()


class ContentPipelineRequest(BaseModel):
    """Request model for content pipeline workflow."""

    topic: str = Field(..., description="Topic to create content about")
    style: str = Field(default="professional", description="Content style")
    audience: str = Field(default="general", description="Target audience")


class ResearchWorkflowRequest(BaseModel):
    """Request model for research workflow."""

    query: str = Field(..., description="Research query")
    depth: str = Field(
        default="standard",
        description="Research depth: 'quick', 'standard', or 'deep'",
    )


class WorkflowResponse(BaseModel):
    """Response model for workflow execution."""

    workflow: str
    status: str
    result: dict


# In-memory storage for async workflow results (use Redis in production)
workflow_results: dict[str, dict] = {}


@router.get("/")
async def list_workflows() -> dict:
    """List available workflows."""
    return {
        "workflows": [
            {
                "name": "content-pipeline",
                "description": "Multi-agent content creation: Research -> Write -> Review -> Revise",
                "endpoint": "/api/v1/workflows/content-pipeline",
            },
            {
                "name": "research",
                "description": "In-depth research workflow with analysis and review",
                "endpoint": "/api/v1/workflows/research",
            },
        ]
    }


@router.post("/content-pipeline", response_model=WorkflowResponse)
async def run_content_pipeline(request: ContentPipelineRequest) -> WorkflowResponse:
    """Run the content creation pipeline workflow.

    This executes a multi-agent workflow:
    1. Researcher gathers information on the topic
    2. Writer creates content based on research
    3. Reviewer evaluates the content
    4. Writer revises if needed (up to 3 iterations)
    """
    try:
        workflow = ContentPipelineWorkflow(max_iterations=3)
        result = await workflow.run(
            topic=request.topic,
            style=request.style,
            audience=request.audience,
        )

        return WorkflowResponse(
            workflow="content-pipeline",
            status=result.get("status", "completed"),
            result={
                "topic": result.get("topic"),
                "final_content": result.get("final_content"),
                "iterations": result.get("iteration_count"),
                "final_score": result.get("review_score"),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research", response_model=WorkflowResponse)
async def run_research_workflow(request: ResearchWorkflowRequest) -> WorkflowResponse:
    """Run the research workflow.

    This executes a multi-agent workflow:
    1. Initial research on the query
    2. Deep analysis of findings
    3. Quality review
    4. Final report generation
    """
    try:
        workflow = ResearchWorkflow()
        result = await workflow.run(
            query=request.query,
            depth=request.depth,
        )

        return WorkflowResponse(
            workflow="research",
            status=result.get("status", "completed"),
            result={
                "query": result.get("query"),
                "depth": result.get("depth"),
                "final_report": result.get("final_report"),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{workflow_id}")
async def get_workflow_result(workflow_id: str) -> dict:
    """Get the result of an async workflow execution."""
    if workflow_id not in workflow_results:
        raise HTTPException(status_code=404, detail="Workflow result not found")
    return workflow_results[workflow_id]

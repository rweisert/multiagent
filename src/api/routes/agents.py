"""Agent-related API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agents import ResearcherAgent, WriterAgent, ReviewerAgent

router = APIRouter()


class AgentRequest(BaseModel):
    """Request model for agent invocation."""

    message: str = Field(..., description="Message to send to the agent")


class AgentResponse(BaseModel):
    """Response model for agent invocation."""

    agent: str
    response: str
    status: str


class ResearchRequest(BaseModel):
    """Request model for research task."""

    topic: str = Field(..., description="Topic to research")
    context: str = Field(default="", description="Additional context")


class WriteRequest(BaseModel):
    """Request model for writing task."""

    task: str = Field(..., description="Writing task description")
    research: str = Field(default="", description="Research to incorporate")
    style: str = Field(default="professional", description="Writing style")
    audience: str = Field(default="general", description="Target audience")


class ReviewRequest(BaseModel):
    """Request model for review task."""

    content: str = Field(..., description="Content to review")
    criteria: list[str] = Field(default=[], description="Review criteria")
    context: str = Field(default="", description="Additional context")


@router.get("/")
async def list_agents() -> dict:
    """List available agents."""
    return {
        "agents": [
            {
                "name": "researcher",
                "description": "Research specialist for gathering and analyzing information",
                "endpoints": ["/api/v1/agents/researcher/invoke", "/api/v1/agents/researcher/research"],
            },
            {
                "name": "writer",
                "description": "Content creator for producing written material",
                "endpoints": ["/api/v1/agents/writer/invoke", "/api/v1/agents/writer/write"],
            },
            {
                "name": "reviewer",
                "description": "Quality assurance specialist for reviewing content",
                "endpoints": ["/api/v1/agents/reviewer/invoke", "/api/v1/agents/reviewer/review"],
            },
        ]
    }


@router.post("/researcher/invoke", response_model=AgentResponse)
async def invoke_researcher(request: AgentRequest) -> AgentResponse:
    """Send a message to the researcher agent."""
    try:
        agent = ResearcherAgent()
        response = await agent.invoke(request.message)
        return AgentResponse(
            agent="researcher",
            response=response,
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/researcher/research")
async def research_topic(request: ResearchRequest) -> dict:
    """Execute a research task."""
    try:
        agent = ResearcherAgent()
        result = await agent.process({
            "topic": request.topic,
            "context": request.context,
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/writer/invoke", response_model=AgentResponse)
async def invoke_writer(request: AgentRequest) -> AgentResponse:
    """Send a message to the writer agent."""
    try:
        agent = WriterAgent()
        response = await agent.invoke(request.message)
        return AgentResponse(
            agent="writer",
            response=response,
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/writer/write")
async def write_content(request: WriteRequest) -> dict:
    """Execute a writing task."""
    try:
        agent = WriterAgent()
        result = await agent.process({
            "task": request.task,
            "research": request.research,
            "style": request.style,
            "audience": request.audience,
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reviewer/invoke", response_model=AgentResponse)
async def invoke_reviewer(request: AgentRequest) -> AgentResponse:
    """Send a message to the reviewer agent."""
    try:
        agent = ReviewerAgent()
        response = await agent.invoke(request.message)
        return AgentResponse(
            agent="reviewer",
            response=response,
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reviewer/review")
async def review_content(request: ReviewRequest) -> dict:
    """Execute a review task."""
    try:
        agent = ReviewerAgent()
        result = await agent.process({
            "content": request.content,
            "criteria": request.criteria,
            "context": request.context,
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

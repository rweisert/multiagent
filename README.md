# Multi-Agent LLM Framework

A production-ready framework for building LLM multi-agent applications using Python, LangGraph, and Claude.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Agent Orchestration | LangGraph |
| LLM Provider | Anthropic Claude |
| API Framework | FastAPI |
| Vector Database | ChromaDB |
| State/Cache | Redis |
| Containerization | Docker |

## Project Structure

```
multiagent/
├── src/
│   ├── agents/           # Agent definitions
│   │   ├── base.py       # Base agent class
│   │   ├── researcher.py # Research specialist
│   │   ├── writer.py     # Content creator
│   │   └── reviewer.py   # Quality reviewer
│   ├── tools/            # Agent tools
│   │   ├── calculator.py # Math operations
│   │   ├── web_search.py # Web search
│   │   └── file_handler.py # File operations
│   ├── workflows/        # LangGraph workflows
│   │   ├── content_pipeline.py # Research→Write→Review
│   │   └── research_workflow.py # In-depth research
│   ├── memory/           # State management
│   │   ├── conversation.py # Redis conversation memory
│   │   └── vector_store.py # ChromaDB vector memory
│   ├── api/              # FastAPI application
│   │   └── routes/       # API endpoints
│   └── config.py         # Configuration
├── tests/                # Test suite
├── pyproject.toml        # Dependencies
├── Dockerfile            # Container build
└── docker-compose.yml    # Local development
```

## Quick Start

### 1. Setup Environment

```bash
# Clone and enter directory
cd multiagent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
ANTHROPIC_API_KEY=your-key-here
```

### 3. Run with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### 4. Run Locally

```bash
# Start Redis (required for conversation memory)
docker run -d -p 6379:6379 redis:7-alpine

# Run the API
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### List Agents

```bash
curl http://localhost:8000/api/v1/agents/
```

### Run Content Pipeline

```bash
curl -X POST http://localhost:8000/api/v1/workflows/content-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Benefits of multi-agent AI systems",
    "style": "technical",
    "audience": "developers"
  }'
```

### Run Research Workflow

```bash
curl -X POST http://localhost:8000/api/v1/workflows/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest developments in LLM agents",
    "depth": "deep"
  }'
```

## Python SDK Usage

```python
import asyncio
from src.workflows import ContentPipelineWorkflow, ResearchWorkflow
from src.agents import ResearcherAgent, WriterAgent

async def main():
    # Use individual agents
    researcher = ResearcherAgent()
    result = await researcher.process({
        "topic": "Multi-agent systems",
        "context": "AI research"
    })
    print(result["findings"])

    # Use workflows
    workflow = ContentPipelineWorkflow()
    result = await workflow.run(
        topic="Future of AI agents",
        style="engaging",
        audience="tech enthusiasts"
    )
    print(result["final_content"])

asyncio.run(main())
```

## Available Workflows

### Content Pipeline
Multi-agent content creation with quality feedback loop:
1. **Researcher** - Gathers information on the topic
2. **Writer** - Creates content based on research
3. **Reviewer** - Evaluates quality and provides feedback
4. **Revise Loop** - Writer improves based on feedback (up to 3 iterations)

### Research Workflow
In-depth research with analysis:
1. **Initial Research** - Broad information gathering
2. **Deep Analysis** - Detailed investigation
3. **Review** - Quality assessment
4. **Report Generation** - Final consolidated report

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v
```

## Configuration

All settings can be configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Required |
| `DEFAULT_MODEL` | LLM model to use | claude-sonnet-4-20250514 |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB storage path | ./data/chroma |
| `API_HOST` | API host address | 0.0.0.0 |
| `API_PORT` | API port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |

## Extending the Framework

### Adding a New Agent

```python
from src.agents.base import AgentConfig, BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="CustomAgent",
            role="Specialized task handler",
            temperature=0.5,
        )
        super().__init__(config)

    @property
    def system_prompt(self) -> str:
        return "You are a specialized agent..."

    async def process(self, input_data: dict) -> dict:
        # Implement your logic
        response = await self.invoke(input_data["message"])
        return {"result": response}
```

### Adding a New Tool

```python
from src.tools.base import BaseTool, ToolConfig

class MyTool(BaseTool):
    def __init__(self):
        config = ToolConfig(
            name="my_tool",
            description="Does something useful",
        )
        super().__init__(config)

    async def execute(self, **kwargs) -> dict:
        # Implement tool logic
        return {"result": "success"}
```

## License

MIT
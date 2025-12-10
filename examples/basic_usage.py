#!/usr/bin/env python3
"""Basic usage examples for the multi-agent framework."""

import asyncio
import os

# Ensure the package is importable
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents import ResearcherAgent, WriterAgent, ReviewerAgent
from src.workflows import ContentPipelineWorkflow, ResearchWorkflow
from src.tools import CalculatorTool


async def example_single_agent():
    """Example: Using a single agent."""
    print("=" * 50)
    print("Example: Single Agent Usage")
    print("=" * 50)

    # Create a researcher agent
    researcher = ResearcherAgent()

    # Process a research request
    result = await researcher.process({
        "topic": "Benefits of multi-agent AI systems",
        "context": "For a technical blog post",
    })

    print(f"Agent: {result['agent']}")
    print(f"Topic: {result['topic']}")
    print(f"Status: {result['status']}")
    print(f"\nFindings:\n{result['findings'][:500]}...")


async def example_agent_conversation():
    """Example: Having a conversation with an agent."""
    print("\n" + "=" * 50)
    print("Example: Agent Conversation")
    print("=" * 50)

    writer = WriterAgent()

    # First message
    response1 = await writer.invoke(
        "I need to write a blog post about Python async programming. "
        "What key points should I cover?"
    )
    print(f"Writer's outline:\n{response1[:400]}...")

    # Follow-up (maintains conversation history)
    response2 = await writer.invoke(
        "Great! Now write an engaging introduction based on those points."
    )
    print(f"\nWriter's introduction:\n{response2[:400]}...")


async def example_content_pipeline():
    """Example: Running the content pipeline workflow."""
    print("\n" + "=" * 50)
    print("Example: Content Pipeline Workflow")
    print("=" * 50)

    workflow = ContentPipelineWorkflow(max_iterations=2)

    result = await workflow.run(
        topic="The future of AI assistants in software development",
        style="technical but accessible",
        audience="software developers",
    )

    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iteration_count']}")
    print(f"Final Score: {result['review_score']}/10")
    print(f"\nFinal Content Preview:\n{result['final_content'][:500]}...")


async def example_research_workflow():
    """Example: Running the research workflow."""
    print("\n" + "=" * 50)
    print("Example: Research Workflow")
    print("=" * 50)

    workflow = ResearchWorkflow()

    result = await workflow.run(
        query="What are the latest trends in LLM agent architectures?",
        depth="standard",
    )

    print(f"Status: {result['status']}")
    print(f"\nResearch Report:\n{result['final_report'][:800]}...")


async def example_tool_usage():
    """Example: Using tools."""
    print("\n" + "=" * 50)
    print("Example: Tool Usage")
    print("=" * 50)

    calculator = CalculatorTool()

    # Simple calculation
    result = await calculator.execute(expression="(15 * 8) + (42 / 7)")
    print(f"Expression: {result['expression']}")
    print(f"Result: {result['result']}")
    print(f"Status: {result['status']}")


async def main():
    """Run all examples."""
    print("\n🤖 Multi-Agent Framework Examples\n")

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set.")
        print("   Set it to run LLM-dependent examples.\n")
        print("   Running tool example only...\n")
        await example_tool_usage()
        return

    # Run examples
    try:
        await example_tool_usage()
        await example_single_agent()
        await example_agent_conversation()
        await example_content_pipeline()
        await example_research_workflow()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure your ANTHROPIC_API_KEY is valid.")

    print("\n" + "=" * 50)
    print("✅ Examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

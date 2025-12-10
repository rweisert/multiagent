"""Tests for agent classes."""

import pytest
from unittest.mock import AsyncMock, patch

from src.agents.base import AgentConfig, BaseAgent
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.agents.reviewer import ReviewerAgent


class TestAgentConfig:
    """Tests for AgentConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AgentConfig(name="test", role="test role")
        assert config.name == "test"
        assert config.role == "test role"
        assert config.model == "claude-sonnet-4-20250514"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096

    def test_custom_config(self):
        """Test custom configuration values."""
        config = AgentConfig(
            name="custom",
            role="custom role",
            model="claude-3-opus-20240229",
            temperature=0.5,
            max_tokens=2048,
        )
        assert config.model == "claude-3-opus-20240229"
        assert config.temperature == 0.5
        assert config.max_tokens == 2048


class TestResearcherAgent:
    """Tests for ResearcherAgent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = ResearcherAgent()
        assert agent.config.name == "Researcher"
        assert agent.config.temperature == 0.3  # Lower for factual research

    def test_system_prompt(self):
        """Test system prompt content."""
        agent = ResearcherAgent()
        prompt = agent.system_prompt
        assert "Research Specialist" in prompt
        assert "INFORMATION GATHERING" in prompt

    @pytest.mark.asyncio
    async def test_process(self):
        """Test process method."""
        agent = ResearcherAgent()

        with patch.object(agent, 'invoke', new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = "Research findings here"

            result = await agent.process({
                "topic": "Test Topic",
                "context": "Test Context",
            })

            assert result["agent"] == "Researcher"
            assert result["topic"] == "Test Topic"
            assert result["status"] == "completed"
            mock_invoke.assert_called_once()


class TestWriterAgent:
    """Tests for WriterAgent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = WriterAgent()
        assert agent.config.name == "Writer"
        assert agent.config.temperature == 0.7  # Higher for creativity

    def test_system_prompt(self):
        """Test system prompt content."""
        agent = WriterAgent()
        prompt = agent.system_prompt
        assert "Content Writer" in prompt
        assert "CONTENT CREATION" in prompt

    @pytest.mark.asyncio
    async def test_process(self):
        """Test process method."""
        agent = WriterAgent()

        with patch.object(agent, 'invoke', new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = "Written content here"

            result = await agent.process({
                "task": "Write about testing",
                "style": "technical",
                "audience": "developers",
            })

            assert result["agent"] == "Writer"
            assert result["style"] == "technical"
            assert result["status"] == "completed"


class TestReviewerAgent:
    """Tests for ReviewerAgent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = ReviewerAgent()
        assert agent.config.name == "Reviewer"
        assert agent.config.temperature == 0.3  # Lower for critical analysis

    def test_system_prompt(self):
        """Test system prompt content."""
        agent = ReviewerAgent()
        prompt = agent.system_prompt
        assert "Quality Reviewer" in prompt
        assert "QUALITY ASSESSMENT" in prompt

    @pytest.mark.asyncio
    async def test_process(self):
        """Test process method."""
        agent = ReviewerAgent()

        with patch.object(agent, 'invoke', new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = "Review: Score 8/10. Good content."

            result = await agent.process({
                "content": "Test content to review",
                "criteria": ["accuracy", "clarity"],
            })

            assert result["agent"] == "Reviewer"
            assert result["status"] == "completed"
            assert result["criteria_used"] == ["accuracy", "clarity"]

"""Tests for tool classes."""

import pytest

from src.tools.calculator import CalculatorTool
from src.tools.base import ToolConfig


class TestCalculatorTool:
    """Tests for CalculatorTool."""

    @pytest.fixture
    def calculator(self):
        """Create calculator tool instance."""
        return CalculatorTool()

    def test_initialization(self, calculator):
        """Test tool initialization."""
        assert calculator.name == "calculator"
        assert calculator.is_enabled is True

    @pytest.mark.asyncio
    async def test_basic_addition(self, calculator):
        """Test basic addition."""
        result = await calculator.execute(expression="2 + 3")
        assert result["status"] == "success"
        assert result["result"] == 5.0

    @pytest.mark.asyncio
    async def test_basic_subtraction(self, calculator):
        """Test basic subtraction."""
        result = await calculator.execute(expression="10 - 4")
        assert result["status"] == "success"
        assert result["result"] == 6.0

    @pytest.mark.asyncio
    async def test_multiplication(self, calculator):
        """Test multiplication."""
        result = await calculator.execute(expression="6 * 7")
        assert result["status"] == "success"
        assert result["result"] == 42.0

    @pytest.mark.asyncio
    async def test_division(self, calculator):
        """Test division."""
        result = await calculator.execute(expression="15 / 3")
        assert result["status"] == "success"
        assert result["result"] == 5.0

    @pytest.mark.asyncio
    async def test_power(self, calculator):
        """Test exponentiation."""
        result = await calculator.execute(expression="2 ** 8")
        assert result["status"] == "success"
        assert result["result"] == 256.0

    @pytest.mark.asyncio
    async def test_complex_expression(self, calculator):
        """Test complex expression."""
        result = await calculator.execute(expression="(2 + 3) * 4 - 10 / 2")
        assert result["status"] == "success"
        assert result["result"] == 15.0

    @pytest.mark.asyncio
    async def test_negative_numbers(self, calculator):
        """Test negative numbers."""
        result = await calculator.execute(expression="-5 + 3")
        assert result["status"] == "success"
        assert result["result"] == -2.0

    @pytest.mark.asyncio
    async def test_division_by_zero(self, calculator):
        """Test division by zero error handling."""
        result = await calculator.execute(expression="10 / 0")
        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_invalid_expression(self, calculator):
        """Test invalid expression handling."""
        result = await calculator.execute(expression="2 + + 3")
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_unsafe_expression_rejected(self, calculator):
        """Test that unsafe expressions are rejected."""
        # Attempting to use functions or imports should fail
        result = await calculator.execute(expression="__import__('os').system('ls')")
        assert result["status"] == "error"


class TestToolConfig:
    """Tests for ToolConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ToolConfig(name="test", description="Test tool")
        assert config.name == "test"
        assert config.description == "Test tool"
        assert config.enabled is True

    def test_disabled_tool(self):
        """Test disabled tool configuration."""
        config = ToolConfig(name="test", description="Test", enabled=False)
        assert config.enabled is False

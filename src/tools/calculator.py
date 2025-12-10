"""Calculator tool for mathematical operations."""

import ast
import operator
from typing import Any

from langchain_core.tools import BaseTool as LangChainBaseTool, tool

from src.tools.base import BaseTool, ToolConfig


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations."""

    # Safe operators for evaluation
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }

    def __init__(self, config: ToolConfig | None = None) -> None:
        """Initialize the calculator tool."""
        if config is None:
            config = ToolConfig(
                name="calculator",
                description="Perform mathematical calculations. Supports +, -, *, /, **, %, //",
            )
        super().__init__(config)

    def _safe_eval(self, node: ast.AST) -> float:
        """Safely evaluate an AST node."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int | float):
                return float(node.value)
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = self._safe_eval(node.operand)
            op_type = type(node.op)
            if op_type in self.OPERATORS:
                return self.OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Expression):
            return self._safe_eval(node.body)
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    async def execute(self, expression: str, **kwargs: Any) -> dict[str, Any]:
        """Execute a mathematical calculation safely."""
        try:
            # Parse the expression
            tree = ast.parse(expression, mode="eval")
            # Evaluate safely
            result = self._safe_eval(tree)

            return {
                "tool": self.name,
                "expression": expression,
                "result": result,
                "status": "success",
            }
        except (ValueError, SyntaxError, ZeroDivisionError) as e:
            return {
                "tool": self.name,
                "expression": expression,
                "error": str(e),
                "status": "error",
            }

    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to a LangChain compatible tool."""

        @tool(name=self.name, description=self.description)
        async def calculator(expression: str) -> dict[str, Any]:
            """Calculate a mathematical expression."""
            return await self.execute(expression=expression)

        return calculator  # type: ignore

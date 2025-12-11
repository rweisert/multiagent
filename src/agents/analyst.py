"""Analyst Agent - Stage 2 Legal and Technical Analysis."""

import asyncio
import json
from typing import Any

import structlog

from src.agents.base import AgentConfig, BaseAgent, LLMProvider, load_tech_pack

logger = structlog.get_logger(__name__)


class AnalystAgent(BaseAgent):
    """Agent specialized in patent legal and technical analysis.

    Uses Gemini for analysis capabilities.
    Corresponds to Stage 2A, 2B, 2C of the patent pipeline.
    Can run sub-analyses in parallel.
    """

    # No single prompt file - loads stage-specific prompts dynamically
    prompt_file = None

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the analyst agent."""
        if config is None:
            config = AgentConfig(
                name="Analyst",
                role="Patent forensic analyst - claim construction, search analysis, timeline synthesis",
                provider=LLMProvider.GEMINI,
                temperature=0.3,
                max_tokens=8192,
            )
        super().__init__(config)
        self._stage_prompts: dict[str, str] = {}
        self._load_stage_prompts()

    def _load_stage_prompts(self) -> None:
        """Load all stage 2 prompts."""
        from src.agents.base import PROMPTS_DIR

        stage_files = {
            "2a": "PROMPT_Pipeline1_Stage2A_ClaimConstruction_Estoppel_v2.md",
            "2b": "PROMPT_Pipeline1_Stage2B_Search_Technical_v2.md",
            "2c": "PROMPT_Pipeline1_Stage2C_Timeline_Synthesis_v2.md",
        }

        for stage, filename in stage_files.items():
            path = PROMPTS_DIR / filename
            if path.exists():
                self._stage_prompts[stage] = path.read_text(encoding="utf-8")
                logger.debug("Loaded stage prompt", stage=stage)
            else:
                logger.warning("Stage prompt not found", stage=stage, path=str(path))

    def _default_system_prompt(self) -> str:
        """Return the default system prompt for analysis."""
        return """You are a patent forensic analyst. Your job is to analyze patent prosecution
history and provide detailed legal and technical analysis.

Focus on:
- Claim construction and prosecution history estoppel
- Prior art search analysis and technical premise
- Timeline synthesis and key events"""

    def _parse_json_response(self, text: str) -> dict[str, Any]:
        """Parse JSON from LLM response."""
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip()

        return json.loads(text)

    async def analyze_stage2a(
        self,
        extraction: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Perform Stage 2A - Claim Construction & Estoppel analysis.

        Args:
            extraction: Stage 1 extraction data
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2A analysis results
        """
        logger.info("Starting Stage 2A analysis", agent=self.config.name)

        prompt = f"""{self._stage_prompts.get("2a", self._default_system_prompt())}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(extraction, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = await self.invoke(prompt)
        result = self._parse_json_response(response)
        logger.info("Stage 2A completed", keys=list(result.keys()))
        return result

    async def analyze_stage2b(
        self,
        extraction: dict[str, Any],
        stage2a: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Perform Stage 2B - Search & Technical Premise analysis.

        Args:
            extraction: Stage 1 extraction data
            stage2a: Stage 2A analysis results
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2B analysis results
        """
        logger.info("Starting Stage 2B analysis", agent=self.config.name)

        prompt = f"""{self._stage_prompts.get("2b", self._default_system_prompt())}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(extraction, indent=2)}
```

## STAGE 2A DATA

```json
{json.dumps(stage2a, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = await self.invoke(prompt)
        result = self._parse_json_response(response)
        logger.info("Stage 2B completed", keys=list(result.keys()))
        return result

    async def analyze_stage2c(
        self,
        extraction: dict[str, Any],
        stage2a: dict[str, Any],
        stage2b: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Perform Stage 2C - Timeline & Global Synthesis analysis.

        Args:
            extraction: Stage 1 extraction data
            stage2a: Stage 2A analysis results
            stage2b: Stage 2B analysis results
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2C analysis results
        """
        logger.info("Starting Stage 2C analysis", agent=self.config.name)

        prompt = f"""{self._stage_prompts.get("2c", self._default_system_prompt())}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(extraction, indent=2)}
```

## STAGE 2A DATA

```json
{json.dumps(stage2a, indent=2)}
```

## STAGE 2B DATA

```json
{json.dumps(stage2b, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = await self.invoke(prompt)
        result = self._parse_json_response(response)
        logger.info("Stage 2C completed", keys=list(result.keys()))
        return result

    async def analyze_parallel(
        self,
        extraction: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Run Stage 2A, then 2B and 2C in parallel.

        Stage 2A must complete first as 2B and 2C depend on it.
        Stage 2B and 2C can then run in parallel.

        Args:
            extraction: Stage 1 extraction data
            tech_pack_content: Tech pack markdown content

        Returns:
            Merged forensic analysis containing all stage 2 results
        """
        logger.info("Starting parallel analysis", agent=self.config.name)

        # Stage 2A first (required by 2B and 2C)
        stage2a = await self.analyze_stage2a(extraction, tech_pack_content)

        # Stage 2B and 2C in parallel
        stage2b_task = asyncio.create_task(
            self.analyze_stage2b(extraction, stage2a, tech_pack_content)
        )
        stage2c_task = asyncio.create_task(
            self.analyze_stage2c(extraction, stage2a, {}, tech_pack_content)
        )

        stage2b, stage2c = await asyncio.gather(stage2b_task, stage2c_task)

        # Merge results
        forensic_analysis = {
            "stage2a": stage2a,
            "stage2b": stage2b,
            "stage2c": stage2c,
            **stage2a,
            **stage2b,
            **stage2c,
        }

        logger.info("Parallel analysis completed", agent=self.config.name)
        return forensic_analysis

    async def clarify(self, questions: list[str], context: dict[str, Any]) -> dict[str, Any]:
        """Answer clarification questions from QC agent.

        Args:
            questions: List of questions to answer
            context: Analysis context (extraction, forensic data)

        Returns:
            Dictionary with answers to each question
        """
        logger.info("Handling clarification request", questions_count=len(questions))

        prompt = f"""Based on the following analysis context, please answer these questions:

## QUESTIONS
{chr(10).join(f"- {q}" for q in questions)}

## CONTEXT
```json
{json.dumps(context, indent=2)}
```

Provide clear, specific answers with references to the source data.
Return as JSON with question as key and answer as value.
"""

        response = await self.invoke(prompt)
        answers = self._parse_json_response(response)

        logger.info("Clarification completed", answers_count=len(answers))
        return answers

    async def process(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Process analysis request.

        Args:
            input_data: Dictionary containing:
                - extraction: Stage 1 extraction data
                - tech_center: Tech center code for loading tech pack
                - mode: "full" (default), "2a", "2b", "2c", or "clarify"
                - questions: List of questions (for clarify mode)

        Returns:
            Dictionary with analysis results
        """
        extraction = input_data.get("extraction", {})
        tech_center = input_data.get("tech_center", "2100")
        mode = input_data.get("mode", "full")

        try:
            tech_pack_content = load_tech_pack(tech_center)

            if mode == "clarify":
                questions = input_data.get("questions", [])
                answers = await self.clarify(questions, {"extraction": extraction})
                return {
                    "agent": self.config.name,
                    "answers": answers,
                    "status": "completed",
                }

            if mode == "2a":
                result = await self.analyze_stage2a(extraction, tech_pack_content)
            elif mode == "2b":
                stage2a = input_data.get("stage2a", {})
                result = await self.analyze_stage2b(extraction, stage2a, tech_pack_content)
            elif mode == "2c":
                stage2a = input_data.get("stage2a", {})
                stage2b = input_data.get("stage2b", {})
                result = await self.analyze_stage2c(extraction, stage2a, stage2b, tech_pack_content)
            else:
                # Full parallel analysis
                result = await self.analyze_parallel(extraction, tech_pack_content)

            return {
                "agent": self.config.name,
                "forensic_analysis": result,
                "status": "completed",
            }

        except Exception as e:
            logger.error("Analysis failed", agent=self.config.name, error=str(e))
            return {
                "agent": self.config.name,
                "forensic_analysis": {},
                "status": "failed",
                "error": str(e),
            }

"""Gemini LLM client for patent pipeline stages."""

import json
import structlog
from pathlib import Path
from typing import Any

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import get_settings

logger = structlog.get_logger(__name__)

# Base path for prompts
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
TECHPACKS_DIR = Path(__file__).parent.parent / "techpacks"


class GeminiClient:
    """Client for Gemini LLM interactions in the patent pipeline."""

    def __init__(self) -> None:
        """Initialize Gemini client."""
        self.settings = get_settings()
        self._configure_client()
        self._load_prompts()
        self._model: genai.GenerativeModel | None = None

    def _configure_client(self) -> None:
        """Configure the Gemini API client."""
        if not self.settings.google_api_key:
            logger.warning("Google API key not configured")
            return
        genai.configure(api_key=self.settings.google_api_key)

    def _load_prompts(self) -> None:
        """Load all prompt templates."""
        self.prompts: dict[str, str] = {}

        prompt_files = {
            "stage1": "PROMPT_Pipeline1_Stage1_RecordExtraction_v2.md",
            "stage2a": "PROMPT_Pipeline1_Stage2A_ClaimConstruction_Estoppel_v2.md",
            "stage2b": "PROMPT_Pipeline1_Stage2B_Search_Technical_v2.md",
            "stage2c": "PROMPT_Pipeline1_Stage2C_Timeline_Synthesis_v2.md",
            "stage3": "PROMPT_Pipeline1_Stage3_ReportGeneration_v2.md",
            "stage4": "PROMPT_Pipeline1_Stage4_QC_Verification_v2.md",
            "search_intel": "PROMPT_Pipeline2_SearchIntelligence_Module_v1.md",
        }

        for key, filename in prompt_files.items():
            path = PROMPTS_DIR / filename
            if path.exists():
                self.prompts[key] = path.read_text(encoding="utf-8")
                logger.debug("Loaded prompt", key=key, path=str(path))
            else:
                logger.warning("Prompt file not found", key=key, path=str(path))

    @property
    def model(self) -> genai.GenerativeModel:
        """Get or create the Gemini model instance."""
        if self._model is None:
            self._model = genai.GenerativeModel(
                model_name=self.settings.gemini_model,
                generation_config=genai.GenerationConfig(
                    temperature=self.settings.gemini_temperature,
                    max_output_tokens=self.settings.gemini_max_output_tokens,
                ),
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                },
            )
        return self._model

    def _upload_pdf(self, pdf_bytes: bytes, display_name: str) -> Any:
        """Upload a PDF to Gemini for processing.

        Args:
            pdf_bytes: PDF content as bytes
            display_name: Display name for the uploaded file

        Returns:
            Uploaded file reference
        """
        import tempfile
        import os

        # Write to temp file (Gemini SDK requires file path)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(pdf_bytes)
            temp_path = f.name

        try:
            uploaded_file = genai.upload_file(
                path=temp_path,
                display_name=display_name,
                mime_type="application/pdf",
            )
            logger.info("Uploaded PDF to Gemini", display_name=display_name)
            return uploaded_file
        finally:
            os.unlink(temp_path)

    def _parse_json_response(self, text: str) -> dict[str, Any]:
        """Parse JSON from LLM response.

        Args:
            text: Raw response text

        Returns:
            Parsed JSON dictionary
        """
        # Try to extract JSON from markdown code blocks
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip()

        return json.loads(text)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage1(
        self,
        history_pdf_bytes: bytes,
        patent_pdf_bytes: bytes | None = None,
    ) -> dict[str, Any]:
        """Call Stage 1 - Record Extraction.

        Args:
            history_pdf_bytes: Prosecution history PDF content
            patent_pdf_bytes: Optional issued patent PDF content

        Returns:
            Stage 1 extraction JSON
        """
        logger.info("Calling Stage 1 - Record Extraction")

        # Upload PDFs
        history_file = self._upload_pdf(history_pdf_bytes, "prosecution_history.pdf")

        parts = [self.prompts["stage1"], history_file]

        if patent_pdf_bytes:
            patent_file = self._upload_pdf(patent_pdf_bytes, "issued_patent.pdf")
            parts.append(patent_file)

        response = self.model.generate_content(parts)
        result = self._parse_json_response(response.text)

        logger.info("Stage 1 completed", keys=list(result.keys()))
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage2a(
        self,
        stage1_extraction: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Call Stage 2A - Claim Construction & Estoppel.

        Args:
            stage1_extraction: Stage 1 output
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2A analysis JSON
        """
        logger.info("Calling Stage 2A - Claim Construction & Estoppel")

        prompt = f"""{self.prompts["stage2a"]}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(stage1_extraction, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = self.model.generate_content(prompt)
        result = self._parse_json_response(response.text)

        logger.info("Stage 2A completed", keys=list(result.keys()))
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage2b(
        self,
        stage1_extraction: dict[str, Any],
        stage2a: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Call Stage 2B - Search & Technical Premise.

        Args:
            stage1_extraction: Stage 1 output
            stage2a: Stage 2A output
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2B analysis JSON
        """
        logger.info("Calling Stage 2B - Search & Technical Premise")

        prompt = f"""{self.prompts["stage2b"]}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(stage1_extraction, indent=2)}
```

## STAGE 2A DATA

```json
{json.dumps(stage2a, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = self.model.generate_content(prompt)
        result = self._parse_json_response(response.text)

        logger.info("Stage 2B completed", keys=list(result.keys()))
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage2c(
        self,
        stage1_extraction: dict[str, Any],
        stage2a: dict[str, Any],
        stage2b: dict[str, Any],
        tech_pack_content: str,
    ) -> dict[str, Any]:
        """Call Stage 2C - Timeline & Global Synthesis.

        Args:
            stage1_extraction: Stage 1 output
            stage2a: Stage 2A output
            stage2b: Stage 2B output
            tech_pack_content: Tech pack markdown content

        Returns:
            Stage 2C analysis JSON
        """
        logger.info("Calling Stage 2C - Timeline & Global Synthesis")

        prompt = f"""{self.prompts["stage2c"]}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(stage1_extraction, indent=2)}
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

        response = self.model.generate_content(prompt)
        result = self._parse_json_response(response.text)

        logger.info("Stage 2C completed", keys=list(result.keys()))
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage3(
        self,
        stage1_extraction: dict[str, Any],
        stage2_forensic: dict[str, Any],
    ) -> str:
        """Call Stage 3 - Report Generation.

        Args:
            stage1_extraction: Stage 1 output
            stage2_forensic: Merged Stage 2 output

        Returns:
            Stage 3 report as Markdown string
        """
        logger.info("Calling Stage 3 - Report Generation")

        prompt = f"""{self.prompts["stage3"]}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(stage1_extraction, indent=2)}
```

## STAGE 2 FORENSIC DATA

```json
{json.dumps(stage2_forensic, indent=2)}
```
"""

        response = self.model.generate_content(prompt)

        # Stage 3 returns markdown, not JSON
        result = response.text.strip()

        # Remove code block markers if present
        if result.startswith("```markdown"):
            result = result[11:]
        elif result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        logger.info("Stage 3 completed", report_length=len(result))
        return result.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_stage4(
        self,
        stage1_extraction: dict[str, Any],
        stage2_forensic: dict[str, Any],
        stage3_report_md: str,
    ) -> tuple[dict[str, Any], str]:
        """Call Stage 4 - QC & Verification.

        Args:
            stage1_extraction: Stage 1 output
            stage2_forensic: Merged Stage 2 output
            stage3_report_md: Stage 3 report markdown

        Returns:
            Tuple of (QC JSON, corrected final report markdown)
        """
        logger.info("Calling Stage 4 - QC & Verification")

        prompt = f"""{self.prompts["stage4"]}

## STAGE 1 EXTRACTION DATA

```json
{json.dumps(stage1_extraction, indent=2)}
```

## STAGE 2 FORENSIC DATA

```json
{json.dumps(stage2_forensic, indent=2)}
```

## STAGE 3 REPORT

{stage3_report_md}

---

Please provide your response in two clearly separated sections:

### QC_JSON_OUTPUT
```json
{{your QC JSON here}}
```

### FINAL_REPORT_OUTPUT
```markdown
{{corrected final report here}}
```
"""

        response = self.model.generate_content(prompt)
        text = response.text

        # Parse QC JSON
        qc_start = text.find("```json", text.find("QC_JSON_OUTPUT"))
        qc_end = text.find("```", qc_start + 7)
        qc_json_str = text[qc_start + 7:qc_end].strip()
        qc_json = json.loads(qc_json_str)

        # Parse final report
        report_start = text.find("```markdown", text.find("FINAL_REPORT_OUTPUT"))
        if report_start == -1:
            report_start = text.find("```", text.find("FINAL_REPORT_OUTPUT"))
            report_start = text.find("\n", report_start) + 1
        else:
            report_start += 11
        report_end = text.rfind("```")
        final_report = text[report_start:report_end].strip()

        logger.info(
            "Stage 4 completed",
            qc_issues=len(qc_json.get("qc_issues", [])),
            report_length=len(final_report),
        )
        return qc_json, final_report

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def call_search_intel(
        self,
        search_records: dict[str, Any],
        convergence_rows: list[dict[str, Any]],
        technical_reps: list[dict[str, Any]],
        tech_pack_content: str,
    ) -> str:
        """Call Search Intelligence Module (Pipeline 2).

        Args:
            search_records: Search records from Stage 1
            convergence_rows: Convergence analysis from Stage 2B
            technical_reps: Technical representations from Stage 2B
            tech_pack_content: Tech pack markdown content

        Returns:
            Search Intelligence report as Markdown string
        """
        logger.info("Calling Search Intelligence Module")

        prompt = f"""{self.prompts["search_intel"]}

## SEARCH RECORDS

```json
{json.dumps(search_records, indent=2)}
```

## CONVERGENCE ANALYSIS

```json
{json.dumps(convergence_rows, indent=2)}
```

## TECHNICAL REPRESENTATIONS

```json
{json.dumps(technical_reps, indent=2)}
```

## TECH PACK

{tech_pack_content}
"""

        response = self.model.generate_content(prompt)

        # Returns markdown
        result = response.text.strip()

        # Remove code block markers if present
        if result.startswith("```markdown"):
            result = result[11:]
        elif result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]

        logger.info("Search Intelligence completed", report_length=len(result))
        return result.strip()


def load_tech_pack(tech_center: str) -> str:
    """Load tech pack content for a given tech center.

    Args:
        tech_center: Tech center code (e.g., "2100", "2600")

    Returns:
        Tech pack markdown content

    Raises:
        FileNotFoundError: If tech pack not found
    """
    mapping = {
        "1600": "TECH_BIOTECH_TC1600_OptionB.md",
        "1700": "TECH_Chemistry_TC1700.md",
        "2100": "TECH_SOFTWARE_TC2100.md",
        "2400": "TECH_NETWORKING_TC2400.md",
        "2600": "TECH_COMMUNICATIONS_TC2600.md",
        "2800": "TECH_SEMICONDUCTORS_TC2800.md",
        "2900": "TECH_DESIGNS_TC2900.md",
        "3600": "TECH_ECOM_BUSINESS_TC3600.md",
        "3700": "TECH_MECH_MED_TC3700.md",
    }

    filename = mapping.get(tech_center)
    if not filename:
        # Default to software if unknown
        logger.warning("Unknown tech center, defaulting to TC2100", tech_center=tech_center)
        filename = "TECH_SOFTWARE_TC2100.md"

    path = TECHPACKS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Tech pack not found: {path}")

    return path.read_text(encoding="utf-8")

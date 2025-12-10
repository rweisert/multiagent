# Patent Pipeline Prompts

This directory contains all LLM prompt templates used by the patent litigation report pipeline. Each prompt is a carefully engineered Markdown document that instructs Google Gemini on how to process patent documents and prosecution history.

## Prompt Architecture

The pipeline uses a multi-stage prompt system where each stage builds on the output of previous stages:

```
Stage 1 (Record Extraction)
         ↓
    Stage 2A (Claim Construction & Estoppel)
         ↓
    Stage 2B (Search & Technical Premise)
         ↓
    Stage 2C (Timeline & Global Synthesis)
         ↓
    Stage 3 (Report Generation)
         ↓
    Stage 4 (QC & Verification)

Pipeline 2 (parallel):
    Search Intelligence Module
```

## Prompt Files

| File | Stage | Purpose |
|------|-------|---------|
| `PROMPT_Pipeline1_Stage1_RecordExtraction_v2.md` | Stage 1 | Extracts structured JSON from prosecution history PDFs |
| `PROMPT_Pipeline1_Stage2A_ClaimConstruction_Estoppel_v2.md` | Stage 2A | Analyzes claim construction and prosecution history estoppel |
| `PROMPT_Pipeline1_Stage2B_Search_Technical_v2.md` | Stage 2B | Analyzes examiner search patterns and technical premise |
| `PROMPT_Pipeline1_Stage2C_Timeline_Synthesis_v2.md` | Stage 2C | Creates timeline analysis and global synthesis |
| `PROMPT_Pipeline1_Stage3_ReportGeneration_v2.md` | Stage 3 | Generates the comprehensive litigation report |
| `PROMPT_Pipeline1_Stage4_QC_Verification_v2.md` | Stage 4 | Quality control and verification of the final report |
| `PROMPT_Pipeline2_SearchIntelligence_Module_v1.md` | Search Intel | Generates search intelligence report (parallel track) |

## Naming Convention

Prompts follow this naming pattern:

```
PROMPT_Pipeline{N}_Stage{X}_{Description}_v{Version}.md
```

- **Pipeline N**: Pipeline number (1 = main pipeline, 2 = sidecar modules)
- **Stage X**: Stage identifier (1, 2A, 2B, 2C, 3, 4)
- **Description**: Human-readable description of the stage
- **Version**: Prompt version number

## Stage Descriptions

### Stage 1: Record Extraction

**Purpose**: Parse complete file wrapper PDFs into structured JSON

**Input**: Patent PDF + Prosecution History PDF
**Output**: JSON with `metadata`, `events`, `claims_diff`, `key_quotes`, `search_records`, `record_discrepancies`

The prompt instructs the LLM to act as a high-precision record extractor that:
- Extracts verbatim text with pin-cites
- Normalizes data structure
- Labels what is actually in the record
- Preserves exact quotes

### Stage 2A: Claim Construction & Estoppel

**Purpose**: Analyze claim language changes and prosecution history estoppel

**Input**: Stage 1 JSON + Tech Pack
**Output**: JSON with `claim_construction_rows`, `estoppel_matrix_rows`

Focuses on:
- Claim term construction analysis
- Prosecution history estoppel identification
- Argument-based and amendment-based estoppel

### Stage 2B: Search & Technical Premise

**Purpose**: Analyze examiner search patterns and technical foundations

**Input**: Stage 1 JSON + Stage 2A JSON + Tech Pack
**Output**: JSON with `technical_reps`, `convergence_rows`, `search_gap_analysis`

Analyzes:
- Technical representations made during prosecution
- Search convergence patterns
- Gaps in examiner search strategy

### Stage 2C: Timeline & Global Synthesis

**Purpose**: Create chronological analysis and synthesize findings

**Input**: Stage 1 JSON + Stage 2A JSON + Stage 2B JSON + Tech Pack
**Output**: JSON with `event_forensics`, `global_findings`

Produces:
- Event-by-event forensic analysis
- Global synthesis of prosecution patterns
- Strategic timeline observations

### Stage 3: Report Generation

**Purpose**: Generate comprehensive litigation report in Markdown

**Input**: Stage 1 JSON + Merged Stage 2 JSON
**Output**: Markdown report

Creates the final human-readable report with:
- Executive summary
- Claim construction tables
- Estoppel analysis
- Search gap findings
- Strategic recommendations

### Stage 4: QC & Verification

**Purpose**: Quality control and fact verification

**Input**: Stage 1 JSON + Merged Stage 2 JSON + Stage 3 Report
**Output**: QC JSON + Corrected Final Report

Performs:
- Citation verification
- Claim mapping validation
- Factual accuracy checks
- Report corrections

### Search Intelligence Module (Pipeline 2)

**Purpose**: Generate search-focused intelligence report (parallel track)

**Input**: Search Records + Convergence Analysis + Technical Reps + Tech Pack
**Output**: Markdown search intelligence report

Provides specialized analysis of:
- Prior art search strategies
- Classification coverage
- Keyword analysis
- Recommended search expansions

## Prompt Engineering Guidelines

When modifying prompts:

1. **Preserve Structure**: Maintain the existing section structure (ROLE, OBJECTIVE, OUTPUT FORMAT, etc.)
2. **Version Increment**: Create a new version file rather than modifying existing prompts in production
3. **Test Thoroughly**: Run the pipeline with sample documents before deploying prompt changes
4. **Document Changes**: Add comments describing significant changes
5. **Output Format**: Be explicit about expected JSON schemas and Markdown structure

## Integration

Prompts are loaded by the `GeminiClient` class in `services/gemini_client.py`:

```python
from src.patent_pipeline.services.gemini_client import GeminiClient

client = GeminiClient()
# Prompts available as: client.prompts["stage1"], client.prompts["stage2a"], etc.
```

## Tech Pack Integration

Prompts in Stages 2A-2C and Search Intelligence receive domain-specific context from Tech Packs. See `../techpacks/readme.md` for details on the tech pack system.

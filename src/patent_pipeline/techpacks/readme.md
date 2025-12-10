# Tech Packs

Tech Packs provide domain-specific knowledge and guidance to the patent litigation pipeline. Each tech pack contains specialized information about a USPTO Technology Center, helping the LLM understand the nuances of patent prosecution in different technical fields.

## Purpose

Tech Packs enable the pipeline to:

1. **Apply Domain Expertise**: Understand field-specific terminology, claim drafting conventions, and common rejection patterns
2. **Improve Accuracy**: Provide context about typical prior art sources and search strategies for each technology area
3. **Customize Analysis**: Tailor estoppel analysis and claim construction to domain-specific legal precedents

## Tech Center Mapping

The pipeline routes to tech packs based on the USPTO Art Unit extracted from prosecution history:

| Tech Center | Art Units | Domain | Tech Pack File |
|-------------|-----------|--------|----------------|
| TC 1600 | 1600-1699 | Biotechnology & Organic Chemistry | `TECH_BIOTECH_TC1600_OptionB.md` |
| TC 1700 | 1700-1799 | Chemical & Materials Engineering | `TECH_Chemistry_TC1700.md` |
| TC 2100 | 2100-2199 | Computer Architecture & Software | `TECH_SOFTWARE_TC2100.md` |
| TC 2400 | 2400-2499 | Networking & Cryptography | `TECH_NETWORKING_TC2400.md` |
| TC 2600 | 2600-2699 | Communications | `TECH_COMMUNICATIONS_TC2600.md` |
| TC 2800 | 2800-2899 | Semiconductors & Electrical Systems | `TECH_SEMICONDUCTORS_TC2800.md` |
| TC 2900 | 2900-2999 | Designs | `TECH_DESIGNS_TC2900.md` |
| TC 3600 | 3600-3699 | E-Commerce & Business Methods | `TECH_ECOM_BUSINESS_TC3600.md` |
| TC 3700 | 3700-3799 | Mechanical & Medical Devices | `TECH_MECH_MED_TC3700.md` |

## Tech Pack Structure

Each tech pack should follow this general structure:

```markdown
# Tech Pack: [Technology Center Name]

## Overview
Brief description of the technology center's focus areas.

## Key Technology Areas
- List of primary technical domains
- Sub-specialties within the tech center

## Common Claim Structures
Typical claim formats and language patterns for this domain.

## Prosecution Patterns
- Common rejection types (§102, §103, §101, §112)
- Typical examiner arguments
- Effective response strategies

## Prior Art Sources
- Primary databases and search tools
- Key classification codes (CPC/USPC)
- Important journals and publications

## Estoppel Considerations
Domain-specific estoppel issues and case law.

## Search Strategy Guidance
- Recommended keyword approaches
- Classification hierarchies
- Non-patent literature sources
```

## Routing Logic

The tech pack router (`nodes/tech_pack_router.py`) determines which tech pack to load:

1. Extracts `art_unit` from Stage 1 metadata
2. Derives tech center from first two digits (e.g., "2134" → "2100")
3. Loads corresponding tech pack file
4. Falls back to `TECH_SOFTWARE_TC2100.md` if tech center is unknown

```python
# Example routing
art_unit = "2134"
tech_center = art_unit[:2] + "00"  # "2100"
# Loads: TECH_SOFTWARE_TC2100.md
```

## Creating New Tech Packs

To add a new tech pack:

1. Create a Markdown file following the naming convention: `TECH_{NAME}_TC{XXXX}.md`
2. Add the tech center mapping to `services/gemini_client.py`:
   ```python
   mapping = {
       "XXXX": "TECH_{NAME}_TCXXXX.md",
       # ...
   }
   ```
3. Update the same mapping in `nodes/tech_pack_router.py`

## Integration

Tech packs are injected into prompts during Stages 2A, 2B, 2C, and the Search Intelligence module:

```python
# From services/gemini_client.py
prompt = f"""{self.prompts["stage2a"]}

## STAGE 1 EXTRACTION DATA
{json.dumps(stage1_extraction)}

## TECH PACK
{tech_pack_content}
"""
```

## Default Behavior

If a tech pack file is not found:
- The pipeline continues with a fallback message
- A warning is logged
- Analysis proceeds without domain-specific guidance

This ensures the pipeline remains functional even when tech packs are incomplete or missing.

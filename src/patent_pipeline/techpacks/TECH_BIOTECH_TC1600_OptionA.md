# Technology Pack — TC 1600: Biotechnology (Option A — Triage)

*(Lightweight triage pack for quick risk-flagging in TC 1600 matters. Not a full production tech pack; always hands off to Option B for deep analysis.)*

---

## STATUS & SCOPE

**Status:** ⚠️ DRAFT (Phase 0 – triage-only, not a stand-alone TC 1600 pack)

- **Intended role:** Fast triage and routing only.
- **Do not** use this pack by itself to drive Stage 2A/2B/2C conclusions, Stage 3 written reports, or Stage 4 QC.
- For any substantive biotech invalidity or FTO analysis, you **must** use **`TECH_BIOTECH_TC1600_OptionB.md`** (Option B — Deep Analysis) as the primary TC 1600 pack.
- This pack is intentionally **short and heuristic-heavy**. It exists only to:
  - Confirm that a matter really belongs in TC 1600.
  - Classify the biotech archetype.
  - Flag obvious 101 / 112 / 102–103 risk clusters.
  - Produce a **standardized triage note** that the Option B run can consume.

> **Triage-only rule:**  
> Option A may start the conversation, but **Option B must finish it** for any serious biotech matter.

---

## WHEN THIS PACK IS USED (STAGE 1)

**Tech Center:** TC 1600 – Biotechnology & Organic Chemistry  
**Technology Type:** biotech / life_sciences  
**Typical Art Units:** 1600-series biotech art units

### Stage 1 Detection & Routing

Use **Option A – Triage** when:

- `Stage1.metadata.tech_center = "1600"`
- `Stage1.metadata.technology_type` ∈ {"biotech", "life_sciences", "biologics", "diagnostics"}
- `Stage1.metadata.tech_pack_file = "TECH_BIOTECH_TC1600_OptionA.md"`

AND at least one of:

- The invention’s **core novelty** is biological (antibody, vector, sequence, biomarker, cell / gene therapy).
- Claims rely on **sequence IDs** or **biomarker correlations** as central elements.
- Stage 1 is still deciding whether to route to **Chemistry** vs **Biotech**, and a quick biotech risk snapshot would help.

#### Route to Other Packs Immediately When

- The invention is predominantly **small-molecule chemistry** (no biologic structures, no sequence/biomarker-centric claims)  
  → use **`TECHPACK_Chemistry.md`**.

- The invention is clearly a **deep biotech case** (antibody genera, complex diagnostics, cell/gene therapy, sophisticated sequence frameworks) **and** you are ready to do full analysis  
  → go directly to **`TECH_BIOTECH_TC1600_OptionB.md`** instead of lingering in Option A.

- The matter is plainly **not life-science** (software, networking, mechanical, semiconductors, designs, etc.)  
  → route to the appropriate non-1600 tech pack (TC 2100 / 2400 / 2600 / 2800 / 2900 / 3600 / 3700).

---

## 1. TRIAGE WORKFLOW (HIGH-LEVEL SCRIPT)

For Stage 1 / early Stage 2 triage, follow this minimal script:

1. **Step 0 – Confirm biotech center of gravity** (see §2).  
2. **Step 1 – Classify the archetype** (see §3).  
3. **Step 2 – Run the universal red-flag checklist** (see §4).  
4. **Step 3 – Apply archetype-specific questions** (see §5).  
5. **Step 4 – Do a lightweight search sanity check** (see §6).  
6. **Step 5 – Capture standardized triage output** (see §7) and explicitly hand off to **Option B**.

If Steps 0–5 suggest **material biotech risk or opportunity**, Stage 1 should:

- Set a flag like `Stage1.flags.requires_biotech_deep_dive = true`, and  
- Ensure that **Stage 2 uses Option B**, not Option A, for detailed guidance.

---

## 2. STEP 0 — CONFIRM BIOTECH CENTER OF GRAVITY

Ask:

1. Is the **core novelty** biological (antibody, vector, sequence, biomarker, cell)?
2. Would a **biologist** (rather than a chemist, software engineer, or EE) be the main PHOSITA?
3. Are **sequence IDs** or **biomarker correlations** central to the claims?
4. Is the invention tied to **biologic modalities** (proteins, viral vectors, engineered cells) rather than purely small molecules?

If “yes” to most → TC 1600-style biotech analysis is probably appropriate.

If “no” to most:

- Re-check whether TC 1700/3600 Chemistry, or another tech center (2100/2400/2600/2800/3700/2900), is a better fit.
- Do **not** force-fit such matters into biotech just because there is a medical context.

---

## 3. STEP 1 — CLASSIFY THE INVENTION ARCHETYPE

Pick the primary bucket (you can have secondary ones):

1. **Antibody / protein therapeutic**
2. **Sequence-centric** (DNA/RNA/protein; RNA therapeutics)
3. **Diagnostic / biomarker method**
4. **Cell / gene therapy**
5. **Formulation / dosing / treatment regimen**

You will use the archetype-specific checklists in §5.

If the matter plainly straddles **biotech + small-molecule chemistry** (e.g., antibody–drug conjugates where chemistry is central), flag for **dual-pack review** (Chemistry + Biotech Option B).

---

## 4. STEP 2 — UNIVERSAL RED-FLAG CHECKLIST

For **any** biotech claim set, quickly ask:

### §101 (Eligibility)

- Does the claim mainly recite a **natural correlation** (e.g., measuring biomarker X → inferring disease Y)?
- Is the composition essentially a **naturally occurring molecule** described as “isolated” or “purified” with no clear “markedly different” features?
- Are extra steps (sample acquisition, routine assays) just **conventional laboratory work** wrapped around a natural law?

### §112 (Written Description & Enablement)

- Is a **very broad genus** claimed (e.g., all antibodies to a target/epitope, or all sequences with ≥X% identity) with **only a few concrete examples**?
- Are key terms like **“stringent conditions”**, **“percent identity”**, or **“therapeutically effective amount”** vague, not tied to defined protocols or thresholds?
- Are **sequence listings** sparse, inconsistent, or missing for critical constructs?
- Does the specification feel like a **roadmap** (“try these techniques”) without actually teaching the claimed breadth?

### §102 / §103 (Novelty / Obviousness)

- Is the **target or biomarker** already well-known for the same disease/pathway?
- Does the invention look like **routine optimization** (e.g., humanizing, affinity maturation, minor vector tweaks, dose adjustments) without strong evidence of unexpected results?
- Does the claim merely combine **known components** (e.g., CAR domains, biomarkers in a panel) in a way that seems predictable?

If multiple “yes” answers appear, mark the matter as **high-risk** and escalate for deeper review using **Option B + targeted research**.

---

## 5. ARCHETYPE-SPECIFIC CHECKLISTS (STEP 3)

Use these after Steps 0–2 once you have an archetype from §3.

### 5.1 Antibodies / Protein Therapeutics

**Quick questions**

1. How is the antibody or protein claimed?
   - **Exact sequence**, **CDRs**, **epitope**, **function-only**, or a mix?
2. Are there **many examples** (multiple antibodies/variants) or just **one or two**?
3. Does the claim try to cover **all antibodies** that:
   - Bind a target or epitope, and
   - Achieve a functional result (block binding, reduce a biomarker, etc.)?
4. Are **sequence identity** thresholds used (e.g., ≥80–95% identity)?
   - If yes, are calculation methods / alignment parameters defined?
5. Do “stringent conditions” or similar hybridization/function terms appear without **concrete protocols**?

**Triage outcome**

- If the claim **leans heavily on function/epitope with sparse examples**, flag **§112 risk (enablement / written description)**.
- If the **target and mechanism** are well-known and the invention is largely **engineering optimization** (humanization, Fc tweaks, affinity maturation), flag **§103 risk**.

---

### 5.2 Diagnostics / Biomarker Claims

**Quick questions**

1. Is the core of the claim basically **“measure X → infer Y”**?
2. Are sample collection and assay steps **routine** (e.g., generic blood draw + ELISA/PCR)?
3. Is there a **concrete treatment step** (e.g., administering a particular therapy based on the result), or is it purely classification/prognosis?
4. Are **thresholds and cutoffs** (e.g., biomarker levels, risk scores) clearly defined and supported by data?
5. Does the specification provide **evidence** that using this marker/threshold actually improves decisions vs. prior art methods?

**Triage outcome**

- Pure “measure X → think Y” patterns with routine assays and no real technical add-on → **high §101 vulnerability**.
- Vague or unsupported threshold language (“elevated”, “reduced”, “high risk”) without clear ranges or data → **§112 risk**.
- If prior art already associates **the same marker with the same disease** and uses similar testing, focus on **§102/103 obviousness**.

---

### 5.3 Sequence-Centric Claims (DNA/RNA/Protein)

**Quick questions**

1. Are key sequences recited as **SEQ ID NOs** or only generically described?
2. Do claims rely on **percent identity** or **conservative substitutions** across long sequences?
3. Are **hybridization conditions** specified with actual parameters (temperature, salt, formamide, time) or left as generic “stringent conditions”?
4. Does the spec explain **which residues or motifs matter** for function, or just present a few sequences with little mechanistic insight?
5. Does the claimed sequence encode a **known protein/pathway** with only **minor changes** (e.g., conservative mutations)?

**Triage outcome**

- Missing or vague support for broad variant/identity ranges → **§112 risk** (written description + enablement).
- If the sequence encodes a known protein/pathway with **minor changes**, focus on **§103 risk** (routine optimization / obvious variants).

---

### 5.4 Cell & Gene Therapy

**Quick questions**

1. For **CAR-T / engineered cell** claims:
   - How are **scFv / antigen-binding domain, spacer/hinge, transmembrane, and signaling/co-stimulatory domains** defined?
   - Are domain combinations genuinely new, or just **permutations of well-known modules**?
2. For **viral vectors (AAV, lenti, retro, etc.)**:
   - Are capsid/backbone sequences new or variants of well-known serotypes?
   - Are tropism/efficacy improvements backed by **data across multiple constructs**, or just one example?
3. Are **manufacturing / expansion / transduction protocols** routine or clearly non-routine?

**Triage outcome**

- Claims to broad **CAR or vector architectures** built from known domain “lego pieces” → strong **§103 exposure**.
- Broad functional genera (e.g., “vector that increases transduction in tissue T”) with sparse sequence or construct diversity → **§112 risk**.
- If the case hinges on **dose, schedule, or patient subgroup** rather than construct design, also cross-check §5.5 (Formulations / dosing).

---

### 5.5 Formulations, Dosing & Treatment Regimens

**Quick questions**

1. Is the active agent **new** or already known for the same indication?
2. Are excipients and buffers **standard** or meaningfully unusual?
3. Is the dosage regimen a **narrow, data-backed range** or a **broad, routine-looking set of doses/schedules**?
4. Are “therapeutically effective” or “stabilizing” effects supported by **clear data**?
5. Does the spec explain **why** the claimed regimen is non-obvious vs. standard-of-care (e.g., improved PK/PD, reduced toxicity)?

**Triage outcome**

- New indication / regimen for an old biologic → emphasize **§103** (and sometimes **§101** if the claim looks like optimization without concrete technical improvement).
- Vague efficacy terms without data or defined endpoints → **§112 risk**.

---

## 6. SEARCH STARTING POINTS (LIGHTWEIGHT) – STEP 4

When you first touch a biotech matter, you usually don’t need a full-blown search right away. Start with:

1. **Target / biomarker name + disease**
   - Quick view of whether the **target–disease pair** is saturated with prior art.
2. **Key sequences (if provided)**
   - Check if exact or near-identical sequences show up in existing patents/literature via basic sequence search tools.
3. **Claimed “novel” vector or CAR components**
   - Look up whether the same **domain combinations or capsid mutations** already appear elsewhere.

If this **initial check** suggests the field is crowded or the claimed space is very broad compared to the examples, escalate to a **deeper search plan** using the frameworks in **`TECH_BIOTECH_TC1600_OptionB.md`** (sequence-driven, epitope-driven, diagnostics, and cell/gene therapy search).

---

## 7. RECOMMENDED TRIAGE OUTPUT (FOR NOTES / TICKETS) – STEP 5

When drafting your internal note or ticket, summarize using:

- **Pack source:**  
  - “Per `TECH_BIOTECH_TC1600_OptionA.md` (triage-only; see Option B for full analysis).”
- **Archetype:**  
  - e.g., “Antibody genus to target T”, “Diagnostic on biomarker B”, “AAV vector for liver targeting”.
- **Key claimed feature(s):**  
  - 1–3 bullets.
- **Main risk cluster(s):**
  - §101: [low / moderate / high] + 1–2 sentences.
  - §112: [low / moderate / high] + 1–2 sentences.
  - §102/103: [low / moderate / high] + 1–2 sentences.
- **Open questions / missing info:**
  - e.g., “Need actual sequences”, “Need clear definition of ‘stringent conditions’”, “Need data for claimed dosing range / subgroup”.
- **Next step recommendation:**
  - “Run full biotech analysis using `TECH_BIOTECH_TC1600_OptionB.md` (Option B).”
  - “Run focused search on [target / biomarker / vector] using Option B search frameworks.”
  - “Confirm whether additional data exists on claimed dosing regimen / subgroup.”

This keeps triage outcomes **concise, consistent, and easy to consume** by downstream reviewers and by the Option B-driven Stage 2 run.

---

## 8. STAGE 3 & STAGE 4 HOOKS – CLEAN HANDOFF TO OPTION B

Option A must plug cleanly into later stages **without being mistaken for a full tech pack**.

### 8.1 Stage 3 – Report Generation Hooks

When Stage 3 generates a report and sees triage data tagged as `tech_pack = TECH_BIOTECH_TC1600_OptionA`:

1. **Label it explicitly as triage.**

   Include a short paragraph such as:

   > **Biotech triage (TC 1600)** — Preliminary assessment based on `TECH_BIOTECH_TC1600_OptionA.md` (triage-only pack). A full analysis should use `TECH_BIOTECH_TC1600_OptionB.md` for claim construction, search, and vulnerability patterns.

2. **Never treat Option A as authoritative** if an Option B run is available.

   - If Stage 2 also contains `OptionB`-based outputs, **prefer those** for:
     - Claim construction & estoppel.
     - Detailed search themes.
     - Vulnerability pattern synthesis.
   - Option A content should appear only in:
     - Background / “initial triage” sections.
     - Notes explaining why a biotech deep-dive was (or was not) triggered.

3. **Surface next-step guidance.**

   - If Option A flagged **high-risk clusters** but no Option B run exists yet, Stage 3 should explicitly recommend:
     - “A dedicated TC 1600 deep-dive using `TECH_BIOTECH_TC1600_OptionB.md` is recommended before relying on this triage assessment.”

### 8.2 Stage 4 – QC & Verification Hooks

Stage 4 should treat Option A as **triage-only** and check that it was used appropriately.

**Minimum QC checks (biotech triage usage):**

- [ ] If `Stage1.flags.requires_biotech_deep_dive = true`, confirm that a **full Option B run** was executed or that the report clearly explains why not (e.g., client chose not to proceed).
- [ ] No final opinions on **validity strength** rely solely on Option A heuristics.
- [ ] Where Option A and Option B point in different directions, the report:
  - [ ] Identifies the discrepancy, and  
  - [ ] Favors **Option B** unless explicitly overruled with a reason.
- [ ] The report text clearly labels all Option A-derived content as **“preliminary / triage”**.

**Output-quality reminder for biotech matters:**

- [ ] When Option B is used, Stage 4 should verify that the report cites **“Per `TECH_BIOTECH_TC1600_OptionB.md`”** for core TC 1600 reasoning, and keeps Option A references limited to triage background.

---

## 9. REVISION HISTORY & META

**Version 0.2 – December 2025**

- Added explicit **triage-only scope** and “Option A must hand off to Option B” rule.
- Introduced **Stage 1 detection & routing** section tailored to TC 1600.
- Reorganized prior triage content into **Steps 0–5** with clearer archetype structure.
- Added **Stage 3/4 hooks** so Option A outputs are cleanly labeled and consumed downstream.

**Version 0.1 – Initial Draft**

- Created lightweight biotech triage notes (center-of-gravity check, archetype classification, basic risk prompts, and search starters).

---

**Tech Pack Maintainer:** [TBD]  
**Last Reviewed:** December 2025  
**Next Review Scheduled:** [TBD]

---

**END OF TRIAGE PACK – TC 1600 (Option A — Triage)**

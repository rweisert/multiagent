# TECHNOLOGY PACK: DESIGNS (TC 2900)
## Patent Invalidity Analysis – Design-Specific Guidance

---

## STATUS: ⚠️ DRAFT (Phase 0)

First-pass technology pack focused on **design patents** prosecuted in **TC 2900 – Designs**.  
Design patents protect **ornamental appearance** of an article of manufacture, not its utilitarian function.  
This pack is for invalidity analysis of **U.S. design patents (35 U.S.C. § 171)**, not utility patents.

---

## WHEN THIS PACK IS USED

**Tech Center(s):** TC 2900 – Designs  
**Technology Type:** designs  
**Typical Art Units:** 2900-series design art units

### Stage 1 Detection

Use this pack when:

- `Stage1.metadata.tech_center = "2900"`  
- `Stage1.metadata.technology_type = "design"`  
- `Stage1.metadata.design_flag = true` (if available)  
- `Stage1.metadata.tech_pack_file = "TECH_DESIGNS_TC2900.md"`

AND:

- The patent/application number has a **“D” prefix** (e.g., D8xxxxx), indicating a design patent, or  
- The claims are in **design format** (e.g., “The ornamental design for [article] as shown and described.”), with drawings being the main claim content.

### Route to Other Packs When

- The patent is **utility**, not design → Use a utility tech pack (e.g., TC 1700, 2100, 2400, 2600, 2800, etc.).  
- The matter involves **both** design and utility patents → Use this pack **for the design patents only**; use the appropriate utility tech pack for the utility patents.

### Example Design Patent Scenarios for This Pack (Illustrative)

- [Consumer electronics] – The ornamental design of a smartphone, smartwatch, tablet, earbuds.  
- [Automotive] – The ornamental design of a vehicle front grille, dashboard panel, lamp assembly.  
- [Footwear & apparel] – The ornamental design of a shoe upper/sole, apparel trim, pattern.  
- [UI/Icons] – The ornamental design of a display screen with an icon or graphical user interface (GUI).  
- [Packaging] – The ornamental design of a bottle, container, display package.

---

## TECHNOLOGY CHARACTERISTICS

### Overview

Design patents protect the **visual appearance** (ornamental design) of an article, as shown in the figures, not its functional or structural concepts per se. Key characteristics:

- The **claim** is typically a single sentence referencing the drawings; the drawings themselves define scope.  
- **Broken (dashed) lines** usually indicate **environment or unclaimed portions**; solid lines indicate the claimed design.  
- **Shading, contour, and surface treatment** can be significant to scope (e.g., flat vs convex surfaces, texture).  
- **Article context** matters: the same shape may be a different design when claimed for a different article.

For invalidity, design patents are assessed using:

- **Anticipation (35 U.S.C. § 102)** – A single prior art design that gives the same **overall visual impression** to an **ordinary observer** familiar with the prior art.  
- **Obviousness (35 U.S.C. § 103)** – Often under the **Rosen/Durling** framework (primary reference with basically the same overall visual impression + secondary references for modifications) or evolving case law.  
- **Functionality** – Designs that are **dictated by function** are not protectable; extensive functional constraints can narrow or eliminate protectable ornamentation.

Unlike utility patents:

- There is **no doctrine of equivalents for design patents**; scope is tied to the **overall appearance** defined by the drawings.  
- Prosecution history estoppel and Festo/DOE concepts apply only in limited ways (e.g., amendments to drawings that narrow claim scope).

---

### Typical Claim Structure (Design Patents)

Design claims generally take a standard form:

```text
The ornamental design for a [ARTICLE], as shown and described.
```

**Key elements:**

1. **Title / Article Identification**  
   - Identifies the article of manufacture (e.g., “smartphone”, “display screen with GUI”, “vehicle wheel”).  
   - Can affect scope by anchoring design to particular article context.

2. **Drawings / Figures**  
   - Multiple views: perspective, front, rear, left, right, top, bottom.  
   - Surface shading, contours, visible boundaries.  
   - Broken lines for environment or disclaimed portions.

3. **Description (if any)**  
   - Minimal; may identify the views and clarify broken-line usage or environment.

**Dependent Claims**  
- Design patents rarely have dependent claims; there is typically a single claim.  
- Variant designs are often filed as **continuations/continuations-in-part/divisionals**, each with its own drawings.

---

### Common Prior Art Forms (Designs)

**Design Prior Art**

- Prior **design patents** (U.S. and foreign).  
- Prior **utility patents with drawings** depicting similar articles.  
- **Catalogs, brochures, advertisements** showing product designs.  
- **Product packaging** and industrial design portfolios.  
- **Screenshots / UI designs** (for GUI/icon designs).  
- **Trade dress evidence** (packaging, store layouts, etc.) if disclosing specific ornamental designs.

**Non-Patent Literature (NPL)**

- Product catalogs (online and print).  
- Manufacturer and retailer websites, archived via Wayback Machine.  
- Design exhibitions and magazines (e.g., industrial design, furniture, automotive).  
- App stores, UI galleries, design award submissions (e.g., Red Dot, iF Design).  
- 3D model repositories, if publicly available and dated.

**Commercial Products / Public Use**

- Physical products in the marketplace; photographs and documentation establishing **pre-filing public use**.  
- Product launch events, trade shows, promotional videos.

**Standards & Specifications**

- Design standards are less formalized than technical standards; however, **ergonomic or safety constraints** may impact the functional/ornamental divide.

---

### Key Litigation Issues (Designs)

**Issue 1: Overall Visual Impression & Ordinary Observer Test**

- The core question: Does the prior art (or accused design) create **substantially the same overall visual impression** as the claimed design in the eyes of an **ordinary observer familiar with the prior art**?  
- Small differences in detail may not matter if the overall visual effect is the same.

**Issue 2: Role of Functionality**

- Features **dictated by function** (e.g., shape required to fit another part or meet safety standards) contribute less to protectable ornamentation.  
- High functional constraint can narrow the scope of protectable ornamentation and strengthen invalidity arguments.

**Issue 3: Prosecution History & Amendments to Drawings**

- Applicants may amend drawings to add/remove broken lines, change shading, or modify contours.  
- Such amendments can **narrow the visual scope** and create **estoppel-like effects**: later attempts to sweep in removed features are weak.

---

## STAGE 2A: CLAIM CONSTRUCTION & ESTOPPEL ADAPTATIONS (DESIGNS)

For design patents, “claim construction” is primarily **visual**:

- Identify what the drawings show.  
- Determine which portions are **claimed** vs **disclaimed** (broken lines).  
- Understand the **article context** and how an ordinary observer would perceive the design.

### Claim Construction Special Rules (Designs)

---

#### Special Rule Category 1: Claimed vs Unclaimed (Broken Lines)

**Description**

Broken lines usually indicate **unclaimed subject matter** (environment or portions not part of the claimed design). Solid lines are claimed.

**Application**

- Stage 2A must clearly identify **which elements are claimed ornamentation** vs environment.  
- If the specification explicitly states that broken lines are for **environment only** or are **not part of the claimed design**, treat them as excluded from claim scope.  
- Amendments that convert solid lines to broken lines (or vice versa) are **narrowing/broadening** and should be treated as such.

**Example**

> If the original drawings show the entire smartphone including screen and bezel in solid lines, but the amended drawings show only the bezel in solid lines and the screen in broken lines, the claim is **narrowed** to the bezel design.

---

#### Special Rule Category 2: Shading, Contours, and Surface Treatment

**Description**

Shading and contour lines can indicate **shape**, **depth**, **surface curvature**, and **texture**.

**Application**

- Consider whether the shading indicates **flat vs curved**, **convex vs concave**, or **recessed vs raised** surfaces.  
- If the applicant relied on particular contours/shading to distinguish prior art (e.g., emphasizing a “rounded edge” vs “sharp bevel”), treat those contours as **limiting**.  
- Absence of shading may signal that a surface is **flat or undefined**; presence of detail suggests more specific shape.

---

#### Special Rule Category 3: Article Context and Boundaries

**Description**

The design is for an **article of manufacture**, and article context can influence overall impression.

**Application**

- Title and specification may restrict the design to a specific article (e.g., “display screen with icon” vs entire device).  
- Stage 2A should identify whether the design is for:  
  - the **entire article**,  
  - a **portion of the article**, or  
  - a **surface pattern applied to the article**.  
- Boundaries between claimed and unclaimed article portions (e.g., a portion of a shoe sole vs the entire shoe) should be carefully noted.

---

#### Special Rule Category 4: Functional Constraints

**Description**

Features may be **dictated by function** (e.g., screw holes, hinge locations, plug geometry).

**Application**

- Stage 2A should note which features appear to be **purely functional** and which have **ornamental choices** (shape, proportion, surface detail).  
- For invalidity, functional aspects may contribute less to the protectable scope of the design.

---

### Technology-Specific “Estoppel” Patterns (Designs)

Although Festo/DOE do not apply directly to design patents, **amendments to drawings** and **statements about the design** in prosecution can narrow scope:

---

#### Pattern 1: Converting Solid Lines to Broken Lines (Narrowing the Claim)

**Scenario**

- Original drawings: large portion of the product shown in solid lines.  
- Amendment: many features converted to broken lines to avoid prior art.

**Effect**

- The claim is **narrowed** to exclude previously claimed features.  
- Later attempts to assert that those removed features are part of the design’s scope should be rejected; they are effectively disclaimed.

---

#### Pattern 2: Removing Views or Changing Contours/Shading

**Scenario**

- Original drawings show sharp corners; amended drawings smooth them out.  
- Original design shows certain surface textures or patterns; amended design removes or alters them.

**Effect**

- The new drawings define the effective scope; prior visual features are surrendered.  
- Prior art that matches the original but not the amended design can still inform the **design freedom** and **crowded field** analysis.

---

#### Pattern 3: Clarifying Article Scope (Environment vs Article)

**Scenario**

- Applicant clarifies that certain environment (e.g., a hand, mounting surface, surrounding housing) is **not part of the claimed design**.  
- Alternatively, applicant changes title from broad to narrower article context.

**Effect**

- The design is limited to the recited article/article portion; environment is excluded from comparative analysis except as context.

---

### Festo / DOE in the Design Context

- **Doctrine of Equivalents (DOE)** does **not** operate for design patents the way it does for utility patents.  
- **Festo** and its exceptions are not typically invoked in design cases.  
- Instead, Stage 2A should record drawing amendments and prosecution statements as **scope-narrowing events** and limit subsequent interpretation of the design accordingly.

For pipeline purposes, Stage 2A can:

- Record “amendment-driven scope narrowing” in place of Festo/DOE analysis.  
- Flag drawing changes as estoppel-like events for later synthesis.

---

## STAGE 2B: SEARCH & TECHNICAL ADAPTATIONS (DESIGNS)

Design prior art searching is **visual and article-focused**, not keyword-only.

### Primary Databases & Sources (Priority Order)

**1. Design Patent Databases**

- USPTO design patents (D numbers).  
- EPO / WIPO design databases, where available.  
- Use **classification** (e.g., Locarno classes, U.S. design classes) plus article keywords.

**2. Utility Patents with Drawings**

- Utility patents in relevant art (e.g., smartphones, footwear, furniture) often contain detailed figures showing ornamentation.  
- These can be **design prior art** if they disclose the claimed ornamental design.

**3. Commercial Product Catalogs & Websites**

- Manufacturer and retailer sites (archived if necessary).  
- Catalogs, lookbooks, online shops with product photos.  
- For UI/GUI: app stores, product screenshots, OS vendor docs.

**4. Design & Industrial Publications**

- Design magazines, product design blogs, award submissions (Red Dot, iF, Good Design).  
- Industrial design portfolios and case studies.

**5. Physical Products / Public Use Evidence**

- Photographs and documentation of actual products in the marketplace before the design patent’s priority date.  
- Trade show materials, launch events, packaging photos.

---

### Search Query Structures (High-Level)

Because design searching is visual, queries often start with:

- **Article type** (e.g., “smartphone”, “bottle”, “shoe”, “lamp”, “wheel”)  
- **Design theme** (e.g., “rounded rectangle display”, “notch”, “wave pattern”, “spoke pattern”)

Typical text search pattern:

```text
[ARTICLE TYPE] design
[ARTICLE TYPE] ornamental
[ARTICLE TYPE] catalog
[ARTICLE TYPE] product images
[ARTICLE TYPE] [unique feature term if any]
```

In patent databases:

- Combine **design classification** (USPC D-classes or CPC design codes) with **article keywords**.  
- For utility patents: use keywords for article type and terms like “perspective view”, “front view”, “rear view”.

---

### Non-Patent Literature (NPL) Source Priorities (Designs)

- **Commercial catalogs / lookbooks** for the industry at issue (electronics, furniture, consumer goods, fashion).  
- **Online marketplaces** (e.g., large retailers) with historical product listings.  
- **Brand websites**, archived using Wayback to show earlier designs.  
- **Design award archives** (Red Dot, iF, IDEA, Good Design, etc.).  
- **Design magazines / galleries** that show product shots with dates.

---

### Expert Witness Recommendations (Designs)

**Primary Expert Type**

- **Industrial designer** or **visual design expert** familiar with the product category (e.g., consumer electronics, automotive, footwear).  
- Expertise in **form, proportion, surface treatment, and visual impression**.

**Qualifications**

- Degree in industrial design or related field; practice in the relevant product category.  
- Familiarity with **design patent law concepts** (overall visual impression, ordinary observer).  
- Experience with **product development** and awareness of design freedom and functional constraints in the field.

**Common Expert Tasks**

- Describe **overall visual impression** of claimed and prior art designs.  
- Identify and explain **points of similarity and difference** from the perspective of an ordinary observer.  
- Discuss **design freedom** in the field (how constrained designers are by function, ergonomics, standards).  
- Provide context on **trends and crowded field** (how similar other designs are).

---

## STAGE 2C: SYNTHESIS ADAPTATIONS (DESIGNS)

Stage 2C integrates visual claim construction, prosecution history, and design public domain to form global invalidity views.

### Technology-Specific Vulnerability Patterns

---

**Vulnerability Pattern 1: Crowded Design Field with Many Similar Prior Art Designs**

- **Description:** Many prior designs share similar overall shapes, proportions, and visual motifs.  
- **Effect:** Even small changes may be insufficient to create a distinct overall visual impression.  
- **Strategy:**  
  1. Compile multiple prior art designs showing common motifs.  
  2. Show that the claimed design sits in a **crowded field**, lowering the threshold of similarity needed for invalidity.

---

**Vulnerability Pattern 2: Strong Functional Constraints**

- **Description:** The article’s form is heavily dictated by function (e.g., connectors, mechanical fit, ergonomic requirements).  
- **Effect:** Only minor room for ornamentation; small ornamental differences may not be enough for patentability.  
- **Strategy:**  
  1. Use expert testimony to explain functional constraints and limited design freedom.  
  2. Argue that claimed differences are functionally constrained or trivial variations.

---

**Vulnerability Pattern 3: Drawing Amendments Narrowing Ornamental Features**

- **Description:** Applicant amends drawings mid-prosecution (e.g., adding broken lines, simplifying contours).  
- **Effect:** Narrower design; earlier, more ornate features effectively surrendered.  
- **Strategy:**  
  1. Treat earlier designs as **evidence of original scope** and potential prior art similarity.  
  2. Emphasize that amended design is limited and cannot be stretched back to encompass removed features.

---

### Common Prosecution Mistakes (Designs)

1. **Over‑broad Initial Drawings**, then narrowing in response to prior art.  
2. **Inconsistent broken-line usage** across views, leading to ambiguity.  
3. **Poor article identification**, causing confusion about what is claimed (entire article vs portion vs screen).  
4. **Underestimating commercial prior art**, focusing only on design patents.

---

### Typical Examiner Search Gaps (TC 2900)

**Gap Type 1: Limited Non-Patent Product Search**

- Examiner may check only design patents or limited keyword searches, missing rich commercial product prior art.

**Gap Type 2: Narrow Article Keyword Usage**

- Using only a few keywords (e.g., “bottle”) without synonyms or related product categories.

**Gap Type 3: GUI / Screen Design Nuances**

- Examiners may search GUI patents but overlook app store screenshots, OS guidelines, and UI templates used in the industry.

**Search Strategy**

- Leverage web search, archive tools, and catalog databases more broadly than typical PTO searches.  
- For GUIs, look to OS vendor UX guidelines and early UI frameworks that predate the design patent.

---

## EXAMPLES (DESIGNS)

### Example 1: Construction – Claimed Bezel vs Unclaimed Screen

**Fact Pattern**

- Design title: “Display screen with graphical user interface”.  
- Drawings show a device outline in broken lines, with a GUI shape in solid lines.

**Analysis**

- The claim is to the **GUI shown in solid lines**, not the physical device.  
- Later arguments that the device body shape is part of the design should be rejected.

---

### Example 2: Amendment – Removing Surface Pattern

**Fact Pattern**

- Original drawings show a textured pattern on part of an article; amended drawings remove the pattern and show a smooth surface.  
- Amendment made to avoid prior art pattern.

**Analysis**

- The protected design is the **smooth-surfaced version**, not the original textured one.  
- Prior art with the texture may still be used to show design freedom and crowded field.  
- Surrendered ornamentation cannot be recaptured.

---

### Example 3: Search Strategy – Product Catalog & Online Images

**Fact Pattern**

- Claimed design: beverage bottle with a distinctive shoulder and cap shape.  
- Examiner cited only a couple of design patents.

**Search Plan**

- Search historical catalogs of beverage brands.  
- Use image search and Wayback Machine to locate similar bottles before priority date.  
- Collect photos and product pages showing substantially the same silhouette and details.

---

## TECHNOLOGY EVOLUTION CONSIDERATIONS (DESIGNS)

- Design trends evolve rapidly in some fields (fashion, consumer electronics), more slowly in others (industrial tools).  
- Crowding and saturation in certain product categories means many designs are close cousins; this can strengthen invalidity defenses.  
- Advances in manufacturing (3D printing, new materials) expand design freedom, which can alter how much weight “functional constraints” carry.

---

## QUALITY CHECKS

Before relying on this pack:

- Confirm that the patent is **design**, not utility.  
- Verify that Stage 2A has correctly identified **claimed vs unclaimed features** (broken vs solid lines).  
- Confirm that article context and boundaries are clearly understood (whole article vs portion vs GUI).  
- Ensure searches include **commercial products and NPL**, not just design patents.  
- Check whether drawings were **amended**; if so, treat amendments as narrowing events for scope and “estoppel”.

---

## REFERENCES & RESOURCES (DESIGNS)

(Non-exhaustive; adapt for production.)

- USPTO Design Examination Guidelines.  
- Design patent case law on ordinary observer test and functionality.  
- Locarno and U.S. design classifications for major article categories.  
- Design award archives (Red Dot, iF, IDEA, Good Design).  
- Major design magazines and industrial design resources.

---

## REVISION HISTORY

**Version 0.1 – December 2025**

- Initial draft of **TECH_DESIGNS_TC2900.md**.  
- Structured to mirror other technology packs but adapted for design patents (TC 2900).  
- Emphasizes visual claim scope, broken-line analysis, and commercial product prior art.


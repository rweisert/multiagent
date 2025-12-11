# TECHNOLOGY PACK: MECHANICAL ENGINEERING, MANUFACTURING, MEDICAL DEVICES & PROCESSES (TC 3700)
## Patent Invalidity Analysis – TC 3700-Specific Guidance

---

## STATUS: ⚠️ DRAFT (Phase 0)

First-pass technology pack focused on subject matter examined in **TC 3700 – Mechanical Engineering, Manufacturing, Medical Devices/Processes**.

This pack is intended for patents where the core inventive concept lies in **physical structures and mechanical systems**, including:

- Mechanical assemblies and mechanisms (linkages, gears, cams, actuators, valves, pumps, etc.)
- Vehicles and transportation components (automotive, rail, aerospace, marine)
- Construction equipment, tools, and fixtures
- Manufacturing machines, tooling, industrial processes, packaging machinery
- Medical devices and instruments (mechanical/surgical/implantable/non-biologic)
- Mechanical or electromechanical aspects of diagnostic and therapeutic equipment
- Mechanical/process aspects of patient handling, surgical techniques, and treatments

Not primarily:

- Pure **semiconductor/circuit/optical design** (TC 2800)
- Pure **software/computer architecture** (TC 2100)
- **Networking/communications protocol** inventions (TC 2400 / 2600)
- Pure **design patents** (TC 2900)

---

## WHEN THIS PACK IS USED

**Tech Center(s):** TC 3700 – Mechanical Engineering, Manufacturing, Medical Devices/Processes  
**Technology Type(s):** mechanical / manufacturing / medical_devices  
**Typical Art Units:** 3700-series (mechanical, manufacturing, tools, medical devices/procedures)

### Stage 1 Detection

Use this pack when:

- `Stage1.metadata.tech_center = "3700"`  
- `Stage1.metadata.technology_type` ∈ {"mechanical", "manufacturing", "medical_devices", "mechanical_med"}  
- `Stage1.metadata.tech_pack_file = "TECH_MECH_MED_TC3700.md"`  

AND at least one of:

- Independent claims recite **mechanical components** (frames, housings, shafts, bearings, levers, gears, cams, springs, valves, pistons, actuators, linkages, fasteners, couplings, manifolds, fluid paths) arranged in a **specific physical configuration**.  
- Claims recite **manufacturing or assembly processes** involving specific sequences of physical steps (cutting, shaping, forming, welding, molding, additive manufacturing, coating, sterilizing, packaging).  
- Claims recite **medical devices** or **treatment apparatus** (surgical instruments, catheters, stents, implants, prostheses, orthopedic devices, patient supports, diagnostic devices) with structural features.  
- The invention is framed as an improvement to **mechanical performance, durability, ergonomics, safety, efficiency, manufacturability, or surgical performance** through new **structures or process steps**, not merely new software logic.

### Route to Other Packs When

- Core novelty is in **IC/semiconductor** structures, optics, or electrical circuits → use **TECH_SEMICONDUCTORS_TC2800.md**.  
- Core novelty is in **software / algorithms / GUIs** (even if applied to mechanical devices) → use **TECH_SOFTWARE_TC2100.md**.  
- Core novelty is in **protocol/communications** aspects (e.g., wireless telemetry, network protocols for devices) → use **TC 2400 / 2600** packs.  
- Core novelty is in **ornamental appearance only** → use **TECH_DESIGNS_TC2900.md** for design patents.

### Example Patent Types for This Pack (Illustrative)

- [Mechanical] – Active suspension linkages, brake mechanisms, door latches, hinges, adjustable seats, linear actuators.  
- [Manufacturing] – Automated assembly lines, robotic workcells, injection molding sequences, printing/labeling machines, additive manufacturing methods.  
- [Medical devices] – Catheters, stents, balloon systems, orthopedic implants (plates, screws, joint prostheses), surgical staplers, endoscopes, laparoscopic instruments, infusion pumps, patient positioning systems.  
- [Medical processes] – Methods of positioning instruments, performing minimally invasive procedures, deploying implants, controlling mechanical therapy devices.

---

## TECHNOLOGY CHARACTERISTICS

### Overview

TC 3700 covers inventions grounded in **mechanics, kinematics, dynamics, materials, and manufacturing processes**. Claims typically include:

- **Physical structure** – parts, subassemblies, geometric relationships, joints, interfaces.  
- **Motion / operation** – relative movement of parts, loads, forces, pivoting, translation, rotation, deformation.  
- **Manufacturing steps** – how components are made or assembled.  
- **Interaction with human body** – for medical devices, how the device interacts with tissue, bone, organs, blood flow, etc.

From an invalidity perspective:

- The art is often **predictable** under classical mechanics: substituting known equivalent components, rearranging linkages, or changing dimensions within known ranges is frequently obvious.  
- However, in **medical devices**, human anatomy and physiology can add complexity and some degree of unpredictability.  
- **Obviousness (103)**: Many mechanical inventions combine known elements with predictable results, especially where design handbooks and industry standards describe such combinations.  
- **112(a)**: Broad functional claims (“configured to reduce force”, “adapted to stabilize”, “configured to facilitate surgery”) with minimal structural detail may not enable full scope across all forms that achieve the function.  
- **112(b)**: Terms like “substantially”, “about”, “ergonomic”, “comfortably”, “minimally invasive”, “biocompatible” can be problematic when not anchored to measurable criteria or standard meanings.

---

### Typical Claim Structure

#### 1. Apparatus / Device / System Claims

> “A surgical stapling device comprising:  
>  a handle assembly;  
>  an elongate shaft extending from the handle assembly;  
>  a tool assembly at a distal end of the shaft; and  
>  an actuation mechanism configured to move the tool assembly between an open position and a closed position…”

> “A hinge assembly comprising:  
>  a first leaf;  
>  a second leaf;  
>  a pivot pin coupling the first leaf to the second leaf; and  
>  a biasing member configured to bias the second leaf toward a closed position…”

#### 2. Structural Element Claims

> “A prosthetic knee joint comprising: …”  
> “A vehicle suspension component comprising: …”

#### 3. Method-of-Use Claims

> “A method of deploying a stent, comprising:  
>  advancing a catheter into a vessel;  
>  positioning the stent at a target location; and  
>  expanding the stent to contact the vessel wall…”

These may overlap with medical **methods of treatment**; for eligibility issues see separate guidance. Here we focus on structural and process aspects.

#### 4. Method-of-Manufacture / Assembly Claims

> “A method of manufacturing a multi-part housing, comprising:  
>  molding a first shell;  
>  molding a second shell;  
>  joining the first shell and the second shell using ultrasonic welding; and  
>  forming an opening in the housing…”

**Common Elements**

- **Structure nouns:** frame, housing, base, support, arm, rod, shaft, bracket, link, lever, cam, gear, spring, bearing, pad, strap, cuff, lumen, balloon, stent, anchor, fastener, screw, nail, pin, rivet.  
- **Relationships:** attached to, fixed to, connected to, coupled to, pivotally mounted to, slidably engaged with, disposed between, coaxial with, adjacent to, spaced apart from.  
- **Motion verbs:** rotate, pivot, translate, slide, flex, compress, expand, articulate, bend.  
- **Medical-specific:** lumen, distal/proximal, tissue contact, deployment, retraction, inflation, deflation.

---

### Common Prior Art Forms

**Patent Literature**

- Global patents on mechanical systems, vehicles, tools, manufacturing equipment, and medical devices.  
- Often extensive families in orthopedics, cardiovascular devices, surgical systems, and industrial machinery.

**Non-Patent Literature (NPL)**

- **Mechanical engineering:** ASME conference papers, SAE papers, mechanical journals, engineering handbooks.  
- **Manufacturing:** journals on manufacturing systems, robotics, automation, process engineering.  
- **Medical devices:** journals, conference proceedings (e.g., biomedical engineering, interventional cardiology, orthopedics), clinical technique descriptions.  
- **Standards:** ISO/ASTM/EN standards for device design, safety, and testing (especially medical devices and industrial safety).

**Commercial Products / Catalogs**

- Manufacturer catalogs (implants, tools, industrial components, fasteners, motion systems).  
- Product specification sheets and brochures.  
- Surgical technique guides, product IFUs (Instructions For Use), and training materials.  
- Trade show materials and demo videos.

**Regulatory Filings**

- For medical devices: FDA 510(k) summaries, PMA summaries, and EU/other regulator summaries, which often describe device structure and function.

---

### Key Litigation Issues (TC 3700)

**Issue 1: Structural vs Functional Limitations**

- Mechanical/medical device claims often mix **structural features** (“a link, a lever, a hinge”) with **functional statements** (“configured to reduce force on tissue”).  
- Claim construction must anchor functional limitations to specific structural relationships, not treat them as free-floating performance aspirational language.

**Issue 2: “Intended Use” vs Structural Limitations**

- Preambles and certain functional phrases may be “intended use” and not limiting (e.g., “for stapling tissue”); others can import real structural constraints.  
- Distinguishing these affects both infringement and invalidity.

**Issue 3: Terms of Degree and Relative Terms**

- “Substantially”, “about”, “near”, “adjacent”, “aligned”, “ergonomic”, “configured to fit” must be construed in light of the spec and common engineering understanding.  
- Ambiguous or purely subjective terms can be attacked under 112(b) or narrowed to specific embodiments.

**Issue 4: Combination and Design Choice Obviousness**

- Many mechanical inventions claim combinations of known components (springs, levers, cams) arranged in predictable ways.  
- Courts often view **substitutions of known equivalents, scaling, or simple rearrangements** as obvious design choices absent unexpected results.

---

## STAGE 2A: CLAIM CONSTRUCTION & ESTOPPEL ADAPTATIONS (TC 3700)

Stage 2A applies mechanical/medical-device-specific rules when construing terms and analyzing estoppel.

### Claim Construction Special Rules

---

#### Special Rule Category 1: Connection and Relationship Terms

**Description**

Terms like “connected to”, “coupled to”, “attached to”, “pivotally mounted to”, “slidably engaged with” are central in mechanical claims.

**Application**

- “Connected to” often implies **direct physical connection** unless otherwise broadened in the spec or prosecution.  
- “Coupled to” may allow intervening components, but Stage 2A should consider whether applicant used it to **distinguish direct vs indirect coupling**.  
- “Pivotally mounted”, “rotatably supported” imply a joint permitting **relative rotation** about some axis; that axis and support structure should be identified.  
- If applicant argued that prior art lacked a particular **type of connection** (e.g., pivot vs fixed), that distinction becomes limiting.

**Example**

> Term: “pivotally coupled”  
> Construction: Connected such that one part can rotate relative to the other about a defined pivot axis, as implemented by hinge, pin joint, or equivalent structure described in the specification.

---

#### Special Rule Category 2: Relative Position / Orientation Terms

**Description**

“Adjacent”, “aligned with”, “above”, “below”, “coaxial”, “concentric”, “radially outward”, “distal/proximal” (medical) are common.

**Application**

- Use figures and textual description to determine **reference frames** and **measurement directions**.  
- “Adjacent” may mean **directly next to** or “near but not necessarily touching”; Stage 2A should anchor meaning to usage in the spec and any prosecution arguments.  
- Distal/proximal in medical devices are usually defined relative to the **operator** or **access site**; construction should reflect that.

---

#### Special Rule Category 3: Terms of Degree (“substantially”, “about”, “approximately”)

**Description**

Used for clearances, angles, alignment, symmetry, or ranges (e.g., “substantially parallel”, “about 30 degrees”).

**Application**

- Determine whether the spec provides **tolerances**, examples, or context (manufacturing tolerances, anatomical variation).  
- Where applicant distinguished prior art claiming “perfectly parallel” or “exactly 90 degrees” by arguing “substantially parallel” has leeway, Stage 2A should document how much leeway is implied.  
- Ambiguity can be a basis for 112(b) indefiniteness if not reasonably clear to a PHOSITA.

---

#### Special Rule Category 4: Functional Terms in Apparatus Claims (“configured to”, “adapted to”)

**Description**

Phrases like “configured to compress tissue”, “adapted to engage a fastener”, “configured to reduce friction”.

**Application**

- Anchor the function to specific **structural configurations** described in the spec (e.g., particular geometry, material, surface treatment).  
- Construction should reflect that the device must be **structurally capable** of performing the function under normal use, not just described as such.  
- If applicant narrowed from generic “configured to attach” to specific structural implementations to overcome prior art, treat those structures as limiting.

---

#### Special Rule Category 5: Medical Anatomical Terms and Interfaces

**Description**

Terms like “lumen”, “vessel wall”, “bone”, “tissue-contacting surface”, “distal tip”.

**Application**

- Clarify anatomical reference (e.g., which vessel, which bone) if necessary.  
- Construction of structural terms should incorporate any **contours, dimensions, or surface features** intended to interface with anatomy as described.

---

### Technology-Specific Estoppel Patterns

---

#### Pattern 1: Generic Mechanical Device → Narrowed to Specific Linkage/Geometry

**Typical Scenario**

- Original: “a mechanism for opening and closing a door”.  
- Rejection: 103 over generic hinges and known door closers.  
- Amendment: “a four-bar linkage comprising links A, B, C, and D connected at joints J1–J4 with [specified] geometric relationships, configured to open the door along a predefined path”.

**Estoppel Analysis**

- **Surrendered territory:** other mechanisms achieving opening/closing via different linkages (e.g., single hinge, three-bar linkage) if those differences were emphasized.  
- **Estoppel risk:** HIGH – specific four-bar linkage geometry becomes key to patentability.  
- **DOE implication:** patentee cannot later capture different linkage topologies by DOE.

---

#### Pattern 2: Generic “Support” → Narrowed to Specific Mounting / Adjustment Features

**Typical Scenario**

- Original: “a support configured to support a patient limb”.  
- Rejection: prior art limb supports.  
- Amendment: add details: “a base, a telescoping arm, a pivot joint, and a clamp arranged such that …”

**Estoppel Analysis**

- **Surrendered territory:** supports lacking telescoping or pivoting as claimed.  
- **Estoppel risk:** MEDIUM–HIGH – structural features added specifically to overcome prior art.  
- **DOE impact:** limited ability to assert other adjustment mechanisms as equivalents.

---

#### Pattern 3: Medical Device – Generic Catheter / Implant → Specific Structural Array or Pattern

**Typical Scenario**

- Original: “a stent having a plurality of struts forming an expandable structure”.  
- Rejection: prior stent designs.  
- Amendment: “struts arranged in repeating ring patterns with alternating peak-and-valley configurations and particular connectors between rings”.

**Estoppel Analysis**

- **Surrendered territory:** stent patterns not using the specified repeating structures or connectivities.  
- **Estoppel risk:** HIGH – detailed pattern is the distinguishing feature.  
- **DOE implication:** cannot later rely on DOE to cover substantially different strut patterns.

---

### Festo Exception Analysis – TC 3700

**Predictability**

- Mechanical systems are largely **predictable**; many variations (e.g., alternative linkages, fasteners, materials) are known options.  
- In medical devices, interplay with anatomy introduces some unpredictability, but PHOSITA often still has **predictable design tools**.

**Tangential Exception**

- Rare where amendments add specific mechanical structures to overcome prior art; those are usually central, not tangential.  
- More plausible where amendments correct part labels or clarify directions (“proximal”, “distal”) without affecting function.

**Unforeseeable Exception**

- Hard to satisfy for typical mechanical variations (alternative hinges, springs, linkages) that are well-known.  
- Some potential in medical devices if later-developed biomaterials or structures were not foreseeable at filing, but requires strong proof.

**Other-Reason Exception**

- Possible where amendment is clearly to satisfy formality (e.g., adding “non-transitory” to CRM of a control unit, or clarifying “mounted on” vs “mounted to”) and examiner expressly indicates no 102/103 reliance.

---

### DOE Considerations – TC 3700

**Function–way–result in mechanical/medical devices**

- **Function:** e.g., fastening, supporting, guiding, cutting, compressing, expanding.  
- **Way:** specific configuration of parts, motions, and materials.  
- **Result:** mechanical outcome (movement, load distribution, tissue compression).

**Limitations**

1. **Topology-specific amendments** (e.g., four-bar vs three-bar vs slider-crank) sharply limit DOE.  
2. **Material and geometry amendments** used to distinguish prior art (e.g., specific cross-sections, thicknesses, or stiffness) reduce scope for claiming other materials/sections as equivalents.  
3. **Medical device pattern amendments** (e.g., stent cell pattern) often leave little room for DOE because minor geometric changes can significantly alter performance.  
4. **Foreseeability:** Many alternative mechanisms are standard in the field, undermining Festo “unforeseeable” arguments.

---

## STAGE 2B: SEARCH & TECHNICAL ADAPTATIONS (TC 3700)

Stage 2B leverages typical examiner search gaps: underuse of **industry catalogs, standards, regulatory filings, and practical literature**.

### Primary Databases & Sources (Priority Order)

**1. Patent Databases (USPTO, EPO, JPO, CNIPA)**

- Use CPC/IPC for mechanical systems (e.g., F16, F01–F04, B60/B62, A61B/A61F for medical devices).  
- For medical devices, search both **device CPC** and more general mechanical classes.

**2. Industry Catalogs & Product Literature**

- Catalogs from major manufacturers (tools, fasteners, actuators, bearings, gears, valves, implants, surgical instruments).  
- Medical device brochures and IFUs (instructions for use).  
- Online catalog archives and product pages.

**3. Standards & Guidelines**

- ISO/ASTM standards (e.g., for implants, surgical instruments, industrial safety).  
- Medical device standards, testing protocols, and guidance documents.  
- Vehicle, aerospace, and construction standards (SAE, ASME, building codes) where relevant.

**4. Engineering & Medical Journals / Conferences**

- ASME, SAE, and mechanical engineering journals for mechanisms and machines.  
- Biomedical engineering, orthopedic, interventional cardiology, and surgical technique publications for medical devices.  
- Manufacturing journals for production and assembly processes.

**5. Regulatory Filings (Medical Devices)**

- FDA 510(k) summaries, PMA summaries.  
- CE/MDR summary documents where accessible.  
- These often illustrate devices and their features.

**6. Textbooks & Handbooks**

- Standard mechanical design texts; machine design handbooks.  
- Orthopedic and interventional procedure technique manuals.

---

### Search Query Structures

**A. Mechanical Mechanism Example (Hinge/Linkage)**

```text
(hinge OR "hinge assembly" OR "pivot joint" OR "door closer") AND
("four-bar" OR "linkage" OR "link mechanism" OR "articulation") AND
(adjustable OR "controlled trajectory" OR "soft close")
```

**B. Manufacturing Process Example**

```text
("assembly line" OR "production line" OR "workcell") AND
("robot" OR "robotic arm" OR "manipulator") AND
("fixture" OR "jig" OR "pallet" OR "conveyor") AND
("alignment" OR "positioning" OR "clamping")
```

**C. Medical Device Example (Stent/Catheter)**

```text
(stent OR "endovascular prosthesis" OR "vascular stent") AND
("ring pattern" OR "cell pattern" OR "strut" OR "connector") AND
("balloon catheter" OR "delivery catheter" OR "deployment")
```

**D. Medical Instrument Example**

```text
("surgical stapler" OR "endoscopic stapler" OR "medical stapling device") AND
("cartridge" OR "anvil" OR "jaw" OR "firing mechanism")
```

Use field filters (title/abstract/claims) and CPC filters to focus results.

---

### Classification Search Patterns (CPC/IPC)

Illustrative CPC codes:

- **F16** – Engineering elements (springs, joints, couplings, supports).  
- **F01–F04** – Engines, pumps, turbines, compressors.  
- **B60/B62** – Vehicles, vehicle parts.  
- **B25/B26/B27** – Tools and machine tools.  
- **B65** – Conveying, packaging, storing.  
- **B29** – Plastic shaping (molding, injection molding).  
- **B33Y** – Additive manufacturing.  
- **A61B** – Medical or veterinary science; surgery (devices).  
- **A61F** – Filters, prostheses, orthopedic devices, etc.

Example:

```text
CPC: A61B17/* AND text:("bone plate" OR "bone screw" OR "orthopedic implant")
CPC: B33Y80/* AND text:("additive manufacturing" OR 3D printing OR "layerwise")
```

---

### NPL Source Priorities (TC 3700)

- **Mechanical / Manufacturing:** ASME, SAE, CIRP Annals, Journal of Manufacturing Systems, Journal of Mechanical Design.  
- **Medical Devices:** Journal of Biomechanics, Journal of Orthopaedic Research, Catheterization and Cardiovascular Interventions, surgical technique journals.  
- **Standards:** ISO/ASTM implant, instrument, and machinery standards.

---

### Expert Witness Recommendations

**Primary Expert Types**

- **Mechanical engineer** – general mechanical systems, linkages, structures.  
- **Manufacturing engineer** – assembly lines, fixtures, processing.  
- **Biomedical/biomechanical engineer** – medical devices, implants, device-tissue interaction.  
- **Clinician / surgeon** – for use-based method claims and surgical devices (orthopedic, cardiac, endoscopic, etc.).

**Qualifications**

- Engineering degrees with relevant specialization and 10+ years of experience.  
- For medical devices, practical experience in device design, testing, or clinical use.  
- Publications, standards committee participation, or experience at device manufacturers a plus.

**Common Expert Tasks**

- Explain to the court how a PHOSITA in mechanical/medical devices would interpret structural terms.  
- Map mechanical features in prior art to claim elements.  
- Evaluate mechanical plausibility of claimed benefits (force reduction, range of motion, fatigue life).  
- For medical devices, address safety, usage patterns, and real-world context.

---

## STAGE 2C: SYNTHESIS ADAPTATIONS (TC 3700)

Stage 2C integrates mechanical/medical-device-specific patterns into overall invalidity analysis.

### Technology-Specific Vulnerability Patterns

---

**Vulnerability Pattern 1: “New Combination” of Standard Components**

- **Description:** Invention combines familiar mechanical elements (springs, hinges, levers, cams) in a straightforward configuration to achieve a predictable function.  
- **Strategy:**  
  1. Use handbooks and prior art patents to show each component and its standard use.  
  2. Demonstrate that combining them as claimed is a **predictable design choice** in light of known constraints.  
  3. Emphasize lack of unexpected results.

---

**Vulnerability Pattern 2: “Optimized Geometry” Without Unexpected Results**

- **Description:** Patent tweaks angles, lengths, or clearances (e.g., “between 20 and 30 degrees”) but faces strong prior art.  
- **Strategy:**  
  1. Identify prior art with overlapping or adjacent ranges.  
  2. Show that claimed range is result of routine optimization or design choices.  
  3. Highlight absence of evidence for unexpected performance at claimed range.

---

**Vulnerability Pattern 3: Medical Device – Incremental Changes to Known Designs**

- **Description:** Device is a minor variation on known catheter, stent, implant, or instrument (e.g., modifying strut widths, adding a notch, altering handle ergonomics).  
- **Strategy:**  
  1. Use commercial catalogs and regulatory filings to show evolution of similar designs.  
  2. Demonstrate that differences are small relative to known design space and governed by routine engineering trade-offs.  
  3. Use clinical/engineering experts to explain why changes would have been obvious.

---

### Common Prosecution Mistakes (TC 3700)

1. **Over-relying on Functional Phrasing without Structural Detail**  
   - Claiming high-level benefits (“reduces surgeon fatigue”) without structural explanation.

2. **Underestimating Standard Mechanisms and Design Guides**  
   - Ignoring that many mechanical solutions are standard (e.g., four-bar linkages, universal joints, ratcheting mechanisms).

3. **Narrowing to Specific Geometries/Patterns Without Recognizing Estoppel**  
   - Amending to precise patterns (e.g., stent cell shapes) to avoid prior art, then later arguing broader coverage.

---

### Typical Examiner Search Gaps (TC 3700)

**Gap Type 1: Limited Use of Product Catalogs and Regulatory Filings**

- Examiners may focus on patents and limited technical papers, missing rich commercial product documentation.

**Gap Type 2: Underuse of Mechanical and Medical Standards**

- ISO/ASTM/industry standards are sometimes overlooked, though they often describe standard structural features and test arrangements.

**Gap Type 3: Narrow Keyword Choices**

- Using one terminology (e.g., “bone plate”) and missing synonyms/related terms (“fixation plate”, “osteosynthesis plate”).

**Search Strategy**

- Expand synonyms and cross-language terms (e.g., “prosthesis” vs “implant”).  
- Incorporate standards, catalogs, and regulatory filings systematically.  
- Use images and figures in prior art to visually compare structures.

---

## EXAMPLES (TC 3700)

### Example 1: Claim Construction – “Substantially Parallel” Support Arms

**Fact Pattern**

- Claim recites “first and second support arms substantially parallel to each other”.  
- Spec shows arms slightly converging to meet at a pivot.

**Analysis**

- “Substantially parallel” should account for small angular deviations necessary for assembly or function.  
- If applicant distinguished prior art with clearly non-parallel arms, construction should reflect a narrower tolerance band.

---

### Example 2: Estoppel – Generic Hinge → Four-Bar Linkage

**Fact Pattern**

- Original: “a mechanism configured to move a door between closed and open positions”.  
- Amendment: “the mechanism comprising a four-bar linkage with links arranged as shown in Fig. 3”.

**Estoppel**

- Surrenders simpler hinge-only or alternate linkage mechanisms.  
- DOE around topology (e.g., slider-crank) is strongly constrained.

---

### Example 3: Search Gap – Medical Device Catalogs

**Fact Pattern**

- Patent on an orthopedic implant plate with specific hole patterns and curvature.  
- Examiner cited only patent prior art.

**Search Plan**

- Gather catalogs and technique guides from major orthopedic vendors predating the filing date.  
- Compare hole patterns, contouring, and features to claimed design.  
- Use documents and images to support obviousness or anticipation.

---

## TECHNOLOGY EVOLUTION CONSIDERATIONS (TC 3700)

- Mechanical design fundamentals (linkages, joints, gears) are very mature; many patterns are long-established.  
- Medical device fields evolve continuously but often via **incremental improvement** of established device families.  
- Manufacturing trends (automation, robotics, additive manufacturing) often deploy known engineering principles in new settings.

Implications:

- Expect rich prior art across **patents, standards, catalogs, and regulatory filings**.  
- Many TC 3700 patents may be incremental variations in well-understood design spaces.

---

## QUALITY CHECKS

Before relying on this pack for a matter:

- Confirm the patent’s core is **mechanical/structural/manufacturing/medical device**, not primarily software or networks.  
- Ensure Stage 2A has clearly construed **connection, orientation, functional, and anatomical** terms using the spec and figures.  
- Identify amendments that narrow claims via **materials, geometries, topologies, or patterns**, and treat them as strong estoppel events.  
- Check that Stage 2B search plan includes **catalogs, standards, regulatory filings**, not just patents and a few papers.  
- Match expert specialties (mechanical vs manufacturing vs biomedical vs clinical) to the claims.

---

## REFERENCES & RESOURCES (TC 3700)

(Non-exhaustive; expand in production.)

- CPC/IPC classes: F16, F01–F04, B25/B26/B27, B60/B62, B29, B33Y, A61B, A61F.  
- ASME, SAE, and mechanical design literature.  
- Manufacturing and automation journals/conferences.  
- Biomedical engineering/medical device literature.  
- ISO/ASTM standards for implants, instruments, and machinery.  
- Medical device regulatory summaries (FDA 510(k), PMA, etc.).

---

## REVISION HISTORY

**Version 0.1 – December 2025**

- Initial draft of **TECH_MECH_MED_TC3700.md**.  
- Structured to align with other tech packs (TC 1600, 1700, 2100, 2400, 2600, 2800, 2900, 3600).  
- Focused on mechanical, manufacturing, and medical device/process technologies examined in TC 3700.  
- Requires further calibration with multiple real file wrappers for Phase 1 “production ready” status.


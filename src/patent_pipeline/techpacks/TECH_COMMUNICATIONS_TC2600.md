# TECHNOLOGY PACK: COMMUNICATIONS (TC 2600)
## Patent Invalidity Analysis – Communications-Specific Guidance

---

## STATUS: ⚠️ DRAFT (Phase 0)

First-pass technology pack focused on **communications technology** prosecuted in **TC 2600 – Communications**. This pack is intended for patents where the core inventive concept lies in:

- Wireless and radio communications (cellular, Wi‑Fi, satellite, etc.)
- Physical layer (PHY) signaling and modulation
- Medium access control (MAC) procedures
- Link adaptation, HARQ, error correction
- Channelization, frame/slot/symbol structures
- Uplink/downlink control and reference signals
- Multi-antenna (MIMO, beamforming) techniques

Not primarily:

- Networking / routing / VPNs (TC 2400), or
- Pure software / application logic (TC 2100), or
- Pure semiconductor / circuit design (TC 2800).

---

## WHEN THIS PACK IS USED

**Tech Center(s):** TC 2600 – Communications  
**Technology Type:** communications  
**Typical Art Units:** 2600–2699

### Stage 1 Detection

Use this pack when:

- `Stage1.metadata.tech_center = "2600"`  
- `Stage1.metadata.technology_type` ∈ {"communications", "wireless", "radio", "cellular"}  
- `Stage1.metadata.tech_pack_file = "TECH_COMMUNICATIONS_TC2600.md"`  

AND at least one of:

- Independent claims recite **base stations, user equipment (UEs), terminals, transceivers, radios, antennas, channels, carriers, beams, slots, subframes, physical channels (PDCCH, PDSCH, PUSCH, etc.), HARQ, CQI, MCS, PRBs, reference signals, pilot signals**.
- The invention is framed as an improvement to **coverage, throughput, latency, spectral efficiency, robustness to fading/interference**, or **link reliability**.
- The specification is heavy on **3GPP / 3GPP2 / IEEE 802.x / satellite / broadcast standards**, including references to working groups (RAN1, RAN2, 802.11, etc.).

### Route to Other Packs When

- Claims primarily concern **IP routing, switching, QoS, VPN, or network security** → use **TC 2400 – Networking** pack.
- Claims primarily concern **application-level behavior, data structures, OS behavior, or compilers** → use **TC 2100 – Software** pack.
- Claims primarily concern **integrated circuits, RF front-end circuits, RFIC/PA/LNA design, ADC/DAC, optics** → use **TC 2800** pack.

### Example Patent Types for This Pack (Illustrative)

- [Cellular] – Uplink scheduling and HARQ feedback in LTE or 5G NR.  
- [Wi‑Fi] – Contention window and backoff modifications in IEEE 802.11.  
- [MIMO] – Beamforming weight computation and feedback quantization.  
- [Broadcast] – Frame and pilot structure in digital TV or satellite systems.  
- [Random access] – Preamble design and contention resolution for access channels.

---

## TECHNOLOGY CHARACTERISTICS

### Overview

TC 2600 covers **communications systems** in which information is transmitted over physical media (wireless, cable, optical, satellite) using layered protocols and physical layer techniques. Typical inventions involve:

- **Waveforms and modulation** – OFDM/SC‑FDMA/SC‑FDE, QPSK/QAM, spread spectrum, CDMA/TDMA/FDMA.  
- **Channel coding** – convolutional codes, turbo codes, LDPC, polar codes, hybrid ARQ.  
- **Radio frame structures** – frames, subframes, slots, symbols, resource elements, resource blocks.  
- **Multi-antenna techniques** – MIMO (spatial multiplexing, diversity), beamforming, MU‑MIMO, massive MIMO.  
- **MAC procedures** – random access, scheduling, retransmission, power control, handover, control signaling.  
- **Control channels & reference signals** – PDCCH, PUCCH, PHICH, PSS/SSS, CRS/DM‑RS, CSI‑RS, sounding signals.  

Communications is partly **predictable (protocol design)** and partly **unpredictable (radio channel, propagation)**:

- **Predictable aspects** – assignment of bits to fields, mapping of channels, timer states, algorithms for scheduling and HARQ. These are often treated as **predictable design choices** and thus more susceptible to obviousness.  
- **Unpredictable aspects** – RF channel behavior, fading, mobility effects. These are more relevant to performance analysis, not usually patentability per se.

This mix affects:

- **Obviousness (103):** Many claims are incremental tweaks to standard procedures (e.g., different timing offsets, different mapping of bits, additional fields); these are often obvious in light of standardization history and academic literature.  
- **112(a):** Broad functional claims claiming “improved coverage/throughput” but disclosing only a single parameter tweak may not enable the full scope across channels, topologies, and deployment scenarios.  
- **112(b):** Terms like “near real time”, “high reliability”, “robust”, “optimum”, “substantially orthogonal” are suspect if not defined.

---

### Typical Claim Structure

Communications claims usually fall into:

1. **Apparatus / Transceiver / Node Claims**

> “A base station apparatus comprising: a transmitter; a receiver; and a processor configured to: transmit a synchronization signal …; receive a random access preamble …; allocate uplink resources …; and transmit an uplink grant.”

2. **Method Claims (Base Station / UE)**

> “A method of wireless communication performed by a user equipment (UE), comprising: receiving control information; determining a resource allocation; transmitting a data signal based on the resource allocation; and transmitting hybrid automatic repeat request (HARQ) feedback.”

3. **System Claims**

> “A wireless communication system comprising: a base station; a plurality of user equipments; and a backhaul network, wherein the base station is configured to … and each user equipment is configured to …”

4. **Computer‑Readable Medium Claims**

> “A non‑transitory computer-readable medium storing instructions that, when executed by one or more processors, cause a user equipment to perform: …”

**Common Claim Elements**

- **Preamble:** “A method for wireless communication”, “An apparatus for transmitting data in a wireless network”, “A user equipment configured to…”.  
- **Entities:** base station (eNB/gNB/NodeB / AP), UE, terminal, access point, relay node, repeater.  
- **Signals/Channels:** PDSCH, PUSCH, PDCCH, PUCCH, PRACH, PBCH, RACH preambles, pilots/reference signals.  
- **Resources:** resource blocks, subcarriers, time slots, frequency bands, beams, codewords, layers.  
- **Parameters:** MCS, CQI, rank indicator (RI), precoding matrix indicator (PMI), timing advance, power levels, thresholds, timers, offsets.  
- **Procedures:** random access, scheduling, HARQ, handover, carrier aggregation, beam management, power control.

Dependent claims often:

- Narrow **standard context** (e.g., “wherein the wireless communication system conforms to LTE / NR / 802.11”).  
- Narrow **numerical parameters** (e.g., specific timing offsets, numbers of symbols, thresholds).  
- Narrow **mapping** (fields to positions in frames, channels to symbols).  
- Narrow **antenna behavior** (number of antennas, beam patterns).

---

### Common Prior Art Forms

**Patent Literature**

- Global patents by major vendors and operators (Qualcomm, Ericsson, Nokia, Huawei, Samsung, ZTE, etc.) on PHY/MAC, MIMO, HARQ, frame structures.  
- Often part of **standard-essential patent (SEP)** families tied to 3GPP, 3GPP2, and IEEE standards.

**Non‑Patent Literature (NPL)**

- **3GPP / 3GPP2 / IEEE 802.x standards:** TS/TR docs, specifications for LTE, NR, WCDMA, CDMA2000, 802.11, 802.16, 802.15, etc.  
- **Standardization contributions:** 3GPP Tdocs (RAN1, RAN2, RAN3, SAx), 802.x meeting contributions.  
- **Academic conferences:** IEEE ICC, GLOBECOM, VTC, PIMRC, WCNC, SPAWC.  
- **Journals:** IEEE Transactions on Communications, Wireless Communications, Vehicular Technology, JSAC.  
- **Technical Reports & Theses:** University research work on MIMO, scheduling, coding, random access, interference management.

**Commercial Products / Field Deployments**

- Network infrastructure (base stations, small cells, repeaters) and device firmware behaviors.  
- Test equipment (channel emulators, protocol testers).  
- Vendor whitepapers and performance reports.

**Standards & Specifications**

- 3GPP TS 36.xxx / 38.xxx (LTE, NR), 25.xxx (UMTS), etc.  
- IEEE 802.11 (Wi‑Fi), 802.16 (WiMAX), 802.15 (WPAN).  
- Satellite and broadcast standards (DVB, DVB‑S/S2, DVB‑T/T2, ATSC).

---

### Key Litigation Issues (Communications)

**Issue 1: Standards Context and Claim Construction**

- Many communications patents are **standard‑aligned** (SEP or SEP‑adjacent). Claims may mirror or paraphrase standard text or figures.  
- Construction may hinge on whether terms are given their **standard‑defined meaning** or a broader/literal reading.  
- Cross‑mapping claim elements to standard clauses is often critical for both infringement and invalidity.

**Issue 2: Narrow Parameter / Index Tweaks**

- Inventions often boil down to **changing an index, offset, or mapping** (e.g., which symbol carries a reference signal, which bits are used for HARQ feedback).  
- These tweaks may be obvious optimizations or alternate embodiments already contemplated in standardization discussions.

**Issue 3: Performance Claims Without Solid Technical Support**

- Patents often assert **improved throughput, latency, or robustness** but show only limited simulations or qualitative diagrams.  
- Vulnerable to attack for lack of **scope‑wide enablement** or for obviousness when the benefit follows directly from known trade‑offs (e.g., more pilots improve channel estimation but reduce data throughput).

---

## STAGE 2A: CLAIM CONSTRUCTION & ESTOPPEL ADAPTATIONS (COMMUNICATIONS)

Stage 2A should apply these tech‑specific rules in communications cases.

### Claim Construction Special Rules

---

#### Special Rule Category 1: Frame / Subframe / Slot / Symbol Terms

**Description**

Communications claims heavily rely on time/frequency structures:

- “frame”, “subframe”, “slot”, “symbol”, “resource element”, “resource block”, “subcarrier”.

**Application**

- Use the spec and (if present) explicit references to standards to pin down **time/frequency granularity**.  
- If applicant distinguished prior art based on **specific positions (e.g., symbol index), periodicity, or alignment**, treat those as limiting.  
- Beware of mixing **standard terminology** (e.g., “subframe” in LTE vs NR) – construction should align with the standard context used in the spec.

**Example**

> Term: “subframe” in an LTE context  
> Construction: A 1 ms subframe comprising two slots of 0.5 ms each (14 OFDM symbols for normal CP), as defined in the LTE standard, when the spec clearly incorporates LTE definitions.

---

#### Special Rule Category 2: “Control Information”, “Signaling”, “Resource Allocation”

**Description**

Generic terms like “control information”, “signaling”, “resource allocation”, “scheduling information” can be vague.

**Application**

- Look for **bit-level or field-level** descriptions in the spec (e.g., DCI formats, MAC headers, control channel structures).  
- If claims were amended to specify **which fields** or **which channel** carries the control information, construction should reflect those.  
- Prosecution arguments often differentiate “control information” from “data” based on **channel type (PDCCH vs PDSCH)** or **content (grant vs payload)**.

**Example**

> Term: “resource allocation information”  
> Construction: Information comprising at least the frequency and/or time resources assigned to a UE, encoded in the control channel format described in the specification, not any metadata about the UE.

---

#### Special Rule Category 3: “Predetermined” / “Predefined” / “Reference” Values

**Description**

Terms like “predetermined pattern”, “predefined offset”, “reference signal” are common.

**Application**

- Identify whether “predetermined” is truly arbitrary or is defined by **table, formula, or standard parameter set** in the spec.  
- If applicant narrowed claims to specific patterns (e.g., reference signal positions, scrambling sequences), treat those as definitive.

**Example**

> Term: “predetermined reference signal pattern”  
> Construction: The specific pattern of resource elements designated as reference signals as described in the specification (e.g., every fourth subcarrier in every other symbol for certain antenna ports), not any arbitrary pattern.

---

#### Special Rule Category 4: “Configured To” / “To Perform Wireless Communication”

**Description**

Apparatus claims frequently use “configured to” language for base stations and UEs.

**Application**

- Treat “configured to” as requiring that the device **actually implement the claimed PHY/MAC procedure**, not just be hardware capable in the abstract.  
- In standard‑aligned claims, “configured to” often implicitly means “configured, consistent with standard X, to perform Y” – especially where the spec ties it to specific standard behavior.

---

### Technology-Specific Estoppel Patterns

---

#### Pattern 1: Generic Wireless System → Narrowing to Specific Standard (LTE, NR, 802.11, etc.)

**Typical Scenario**

- Original: “A method for wireless communication in a communication system…”  
- Rejection: 102/103 over generic wireless prior art.  
- Amendment: “wherein the communication system is an LTE system and the method is performed according to 3GPP TS 36.xxx, wherein the base station transmits a PDCCH signal in a control region of each subframe…”

**Estoppel Analysis**

- **Surrendered territory:** non‑LTE systems, non‑3GPP systems, or significantly different frame/control structures.  
- **Estoppel risk:** MEDIUM–HIGH – explicit 3GPP conformance used to distinguish prior art.  
- **DOE consequence:** patentee is constrained when trying to read claims onto non‑LTE technologies; cannot easily assert that different frame structures are “equivalents”.

---

#### Pattern 2: Generic “Pilot / Reference Signal” → Specific Positions or Patterns

**Typical Scenario**

- Original: “A method comprising transmitting a reference signal to enable channel estimation.”  
- Rejection: 103 over prior art pilots/reference signals.  
- Amendment: “transmitting the reference signal in a first OFDM symbol of a subframe and a second OFDM symbol of the subframe, where the first symbol is at index 0 and the second symbol is at index 4, and the reference signal occupies every fourth subcarrier.”

**Estoppel Analysis**

- **Surrendered territory:** other pilot positions, densities, or symbol indices; alternative patterns.  
- **Estoppel risk:** HIGH – specific pattern used to overcome prior art.  
- **DOE consequence:** alternative pilot patterns or symbol positions are likely surrendered, especially if the applicant argued performance differences.

---

#### Pattern 3: Generic Feedback / Link Adaptation → Specific Feedback Format (CQI/RI/PMI/HARQ ACK)

**Typical Scenario**

- Original: “transmitting feedback information indicating channel quality.”  
- Rejection: 103 over prior art channel quality indicators.  
- Amendment: “wherein the feedback information comprises a CQI value encoded as a 4‑bit field, a rank indicator (RI) encoded as a 2‑bit field, and a precoding matrix indicator (PMI) encoded as a 4‑bit field, all transmitted on a control channel in a predetermined subframe.”

**Estoppel Analysis**

- **Surrendered territory:** other feedback arrangements (format, bits, positions) not matching the amended combination.  
- **Estoppel risk:** HIGH – detailed feedback format is now core to patentability.  
- **DOE consequence:** later attempts to treat different feedback formats or channels as equivalent are constrained.

---

### Festo Exception Analysis – Communications

**Predictability**

- Many alternatives in communications (different symbol positions, pilot densities, coding schemes) are **readily foreseeable** to PHOSITA at filing, especially in the context of ongoing standardization.

**Tangential Exception**

- Rare where amendment directly addresses prior art pilot positions, frame structures, or feedback formats.  
- Possible if an amendment addresses side issues (e.g., clarifying notation) while prior art problem lies elsewhere.

**Unforeseeable Exception**

- Difficult to establish: alternative waveforms, pilot patterns, or feedback schemes are often being actively researched and standardized around the filing time.

**Other‑Reason Exception**

- More plausible where amendments respond to formal objections (e.g., terminology alignment with standard, fixing mislabeled channels) and clearly are not about patentability.

---

### DOE Considerations – Communications

**Function–way–result in communications**

- **Function:** transmit/receive/control data, estimate channels, adapt link parameters.  
- **Way:** specific time/frequency mappings, coding, pilot positions, control formats, antenna patterns.  
- **Result:** reliability, throughput, coverage.

**Technology-specific DOE limitations**

1. **Specific timing/frequency patterns** – once narrowed to particular slot/symbol positions, alternatives are likely surrendered.  
2. **Standard‑driven structures** – if applicant claims conformance to a specific standard mechanism, DOE is limited when attempting to capture alternative standard or non‑standard mechanisms.  
3. **Parameter/format amendments** – altering bit lengths, field positions, or mapping is often treated as a material difference, not a trivial equivalent.  
4. **Foreseeability** – because many variants are proposed in standards meetings and literature, Festo “unforeseeable” is hard to satisfy.

---

## STAGE 2B: SEARCH & TECHNICAL ADAPTATIONS (COMMUNICATIONS)

Stage 2B should exploit known search gaps for TC 2600: limited search of standards contributions, academic literature, and non‑US patents, and over‑focus on a few keywords.

### Primary Databases (Priority Order)

**1. 3GPP / 3GPP2 / Standards Archives (HIGHEST PRIORITY for cellular)**

- 3GPP TS/TR documentation (LTE, NR) and meeting contributions (Tdocs) from RAN1/RAN2/RAN3 groups.  
- 3GPP2 and older standards (CDMA2000, EV‑DO).

**2. IEEE Xplore (Wi‑Fi, WiMAX, other wireless)**

- IEEE 802.11 (Wi‑Fi), 802.16 (WiMAX), 802.15 (short‑range), etc.  
- Papers and standards on MAC, PHY, MIMO, OFDM, resource allocation, interference management.

**3. Major Wireless Conferences**

- IEEE ICC, GLOBECOM, VTC, PIMRC, WCNC, SPAWC.  
- Look for pre‑standardization papers on similar techniques.

**4. Patent Databases**

- USPTO, EPO, JPO, CNIPA – heavy activity in communications from major vendors.

**5. Vendor and Test Equipment Documentation**

- Whitepapers, solution briefs, technical manuals from Ericsson, Nokia, Qualcomm, Huawei, Samsung, etc.  
- Documentation from test equipment vendors (Keysight, Rohde & Schwarz).

**6. Theses / Tech Reports**

- University theses on MIMO, scheduling, random access, and coding.

---

### Search Query Structures

**A. Cellular Protocol Example – HARQ / Scheduling**

```text
("hybrid automatic repeat request" OR HARQ) AND
("uplink" OR "downlink") AND
("LTE" OR "Long Term Evolution" OR "NR" OR "5G") AND
("scheduling" OR "resource allocation" OR "grant" OR "feedback")
```

**B. Pilot / Reference Signal Example**

```text
("reference signal" OR "pilot signal" OR "channel estimation") AND
(OFDM OR "orthogonal frequency division") AND
("resource element" OR "resource block" OR "subcarrier") AND
("LTE" OR "NR" OR "802.11")
```

**C. Random Access / RACH Example**

```text
("random access" OR RACH) AND
("preamble" OR "signature" OR "contention") AND
("LTE" OR "NR" OR "3GPP")
```

Use field filters (title/abstract) and classification filters to keep results focused.

---

### Classification Search Patterns (CPC/IPC)

Common CPC codes (illustrative; refine case‑by‑case):

- **H04W** – Wireless communication networks (general).  
- **H04L 5/** – Arrangements affording multiple use of the transmission path (TDMA/FDMA/CDMA/OFDM).  
- **H04B** – Transmission, e.g., analog/digital transmission, radio.  
- **H03M** – Coding/decoding.  

**Example**

```text
CPC: H04W72/* AND text:("HARQ" OR "Hybrid ARQ" OR "uplink scheduling")
CPC: H04L5/* AND text:("OFDM" OR "subcarrier" OR "resource block")
```

---

### NPL Source Priorities (Communications)

1. **Standards:** 3GPP TS 36.xxx / 38.xxx, IEEE 802.11/16/15.  
2. **Standardization Contributions:** 3GPP Tdocs, IEEE 802.x contributions.  
3. **Conferences:** ICC, GLOBECOM, VTC, PIMRC, WCNC, SPAWC.  
4. **Journals:** IEEE Trans. on Wireless Communications, Commun., VTC, JSAC.  
5. **Theses & Technical Reports:** from major wireless research groups (Aalto, Aalborg, Stanford, etc.).

---

### Expert Witness Recommendations

**Primary Expert Types**

- **Wireless communications engineers** specializing in:  
  - Cellular PHY/MAC (LTE, NR, WCDMA, CDMA2000).  
  - Wi‑Fi / WLAN.  
  - Satellite and broadcasting systems.  
  - MIMO, OFDM, interference management.

**Qualifications**

- PhD or equivalent experience in Electrical/Communications Engineering.  
- 10+ years hands-on experience or research in wireless communications.  
- Participation in **3GPP/IEEE standardization** is a strong plus.  
- Publications in major wireless venues; familiarity with system‑level simulation and link‑level models.

**Typical Expert Tasks**

- Define PHOSITA and state of the art at the relevant date.  
- Map claimed PHY/MAC behavior to standard specifications and contributions.  
- Evaluate claimed performance benefits via simulation or analysis.  
- Explain why parameter/index tweaks would be obvious in view of known trade‑offs.  
- Support 103 and 112 arguments based on communications theory and practice.

---

## STAGE 2C: SYNTHESIS ADAPTATIONS (COMMUNICATIONS)

Stage 2C integrates prosecution history, standard context, and search gaps into global findings.

### Technology-Specific Vulnerability Patterns

---

**Vulnerability Pattern 1: “Standard Overlay” Claims**

- **Description:** Patent mirrors standard text/behavior with minimal additional detail, claiming what is effectively standard practice.  
- **Signals:** Heavy quotation/citation of standard; minimal independent technical contribution.  
- **Exploitation:**  
  1. Show that standard (or contributions leading to it) predates priority date.  
  2. Use obviousness to argue standard adoption of well-known techniques.  
  3. Attack any broad functional language as overreaching beyond the actual contribution.

---

**Vulnerability Pattern 2: Parameter / Index Fiddling**

- **Description:** The “innovation” is changing symbol indices, resource block mappings, or parameter thresholds.  
- **Signals:** Claims differ from prior art primarily in numeric offsets, number of symbols, or bit lengths.  
- **Exploitation:**  
  1. Show that such tweaks are routine design choices documented in literature or contributions.  
  2. Emphasize predictable trade‑offs (e.g., pilots vs data, overhead vs accuracy).  
  3. Use 103 arguments rooted in communications design principles.

---

**Vulnerability Pattern 3: Link Adaptation Heuristics without Deep Justification**

- **Description:** Claims a new CQI/HARQ/MCS selection rule or scheduler heuristic with minimal theoretical justification.  
- **Signals:** Simple rules-of-thumb, little discussion of stability, fairness, or convergence.  
- **Exploitation:**  
  1. Search for similar heuristics in earlier academic papers, contributions, or vendor whitepapers.  
  2. Show that claimed heuristic is one of a finite, predictable set of alternatives.

---

### Common Prosecution Mistakes (Communications)

1. **Over‑reliance on Identifying with a Standard Without Showing Novelty Over Contributions**  
   - Failing to distinguish from early drafts, contributions, or prior versions of the standard.

2. **Equating Simulation Diagrams with Proof of Nonobviousness**  
   - Simulations often do not compare against the actual closest prior art or full design space.

3. **Using Vague Performance / Robustness Language**  
   - Lacking rigorous definitions or metrics for “improved coverage, reduced interference, enhanced robustness”.

---

### Typical Examiner Search Gaps (TC 2600)

**Gap Type 1: Limited Search of 3GPP / IEEE Contributions**

- Examiner may check final TS/TR documents but not draft contributions where features were first proposed.

**Gap Type 2: Underuse of Academic Literature**

- Examiners may rely on a subset of patents and a few papers, missing critical conference work.

**Gap Type 3: Narrow Parameter Keywords**

- Searching only for a specific symbol index or feature name, missing synonyms or alternative parameter names.

**Exploitation**

- Perform **systematic search of 3GPP/IEEE contributions** and cross‑reference to final standards.  
- Use academic and vendor literature to show ideas were in public circulation.  
- Explore alternative indexing/parameter names and synonyms in communications literature.

---

## EXAMPLES (COMMUNICATIONS)

### Example 1: Claim Construction – “Subframe” in LTE vs NR

**Fact Pattern**

- Claim recites “a reference signal transmitted in a subframe”.  
- Spec cites LTE TS 36.xxx but also mentions 5G NR TS 38.xxx.

**Analysis**

- Stage 2A should determine whether “subframe” is intended in the LTE sense (1 ms structure) or more generically.  
- If prosecution arguments or spec focus on LTE downlink reference signal patterns, construe “subframe” per LTE, not NR.

---

### Example 2: Estoppel – Generic Reference Signal → Specific Pattern

**Fact Pattern**

- Original: “transmitting a reference signal for channel estimation”.  
- Amendment: “transmitting, in a first symbol and a fifth symbol of a subframe, reference signals occupying every fourth subcarrier in those symbols.”

**Estoppel**

- Surrenders alternative pilot positions and densities.  
- DOE for pilots in other symbols or patterns is strongly limited.

---

### Example 3: Search Gap – Post‑Amendment Random Access Procedure

**Fact Pattern**

- Critical limitation: specific sequence of RACH preamble transmissions and response windows.  
- Examiner’s search logs show generic “RACH” prior art before amendment but no later searches focusing on new timing values or sequence ordering.

**Search Plan**

- Search 3GPP RAN1/RAN2 Tdocs around priority date for alternative RACH designs with similar sequences and timing.  
- Search ICC/GLOBECOM/VTC papers on RACH contention and backoff.  
- Use discovered art to challenge novelty and nonobviousness of the amended procedure.

---

## TECHNOLOGY EVOLUTION CONSIDERATIONS (COMMUNICATIONS)

- Cellular standards (2G/3G/4G/5G) and Wi‑Fi standards have evolved through **incremental enhancements** over decades.  
- Many “new” techniques in later releases are refinements or parameterization of older ideas.  
- Standardization working groups generate **large volumes of contributions** that often anticipate or render obvious later patents.

---

## QUALITY CHECKS

Before relying on this pack:

- Confirm tech match: **wireless/radio/PHY/MAC**, not pure networking or software.  
- Map claim language to **specific standard context**, if present.  
- Identify amendments that narrow to **particular standards, patterns, or index/parameter choices**.  
- Check whether examiner search logs show **standards contributions and relevant conferences**; treat absences as search gaps.  
- Align expert profile (cellular/Wi‑Fi/satellite) to claims’ domain.

---

## REFERENCES & RESOURCES (COMMUNICATIONS)

(Non‑exhaustive; adapt to case.)

- 3GPP TS/TR documentation and meeting contribution archives.  
- IEEE 802.11/16/15 standards and meeting minutes.  
- IEEE Xplore (wireless journals and conference proceedings).  
- Major wireless engineering textbooks (channel coding, OFDM, MIMO, radio resource management).  
- CPC classes H04W, H04L5, H04B, H03M.

---

## REVISION HISTORY

**Version 0.1 – December 2025**

- Initial draft of **TECH_COMMUNICATIONS_TC2600.md**  
- Based on generic tech pack structure and aligned with TC 1700/1600/2100/2400 packs.  
- Focused on PHY/MAC procedures, standard‑aligned communications systems, and common estoppel/search patterns.


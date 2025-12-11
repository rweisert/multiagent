# TECHNOLOGY PACK: COMPUTER ARCHITECTURE & SOFTWARE (TC 2100)
## Patent Invalidity Analysis – Software-Specific Guidance

## STATUS: ⚠️ DRAFT (Phase 0)
First-pass technology pack focused on software and computer architecture prosecuted in TC 2100. Intended for patents whose novelty lies in algorithms, data structures, program logic, execution models, OS/VM internals, GUIs, compilers, and application frameworks.

---

## WHEN THIS PACK IS USED

**Tech Center:** TC 2100 – Computer Architecture & Software  
**Technology Type:** software  
**Typical Art Units:** 2100–2199  

### Stage 1 Detection  
- Stage1.metadata.tech_center = "2100"  
- Stage1.metadata.technology_type = "software"  
- Stage1.metadata.tech_pack_file = "TECH_SOFTWARE_TC2100.md"  

### Use this pack when:
- Claims recite processors, memory, instructions, modules, logic, engines.  
- Claims focus on software behavior (algorithms, data structures).  
- Claims seek improvements to computer functionality itself.  

### Route to other packs when:
- Networking/communications dominate → TC 2400 / 2600  
- Semiconductor/hardware dominates → TC 2800  

---

## TECHNOLOGY CHARACTERISTICS

### Overview
TC 2100 covers inventions where novelty lies mainly in software execution, architecture, or algorithmic logic. Software is treated as a *predictable art*, influencing obviousness, DOE, and Festo analyses.

Domains include:
- OS kernels, scheduling, memory management  
- Virtualization, hypervisors, cloud orchestration  
- Compilers, VMs, interpreters, runtimes  
- Databases, storage engines, indexing, logging, replication  
- GUI frameworks, interaction patterns  
- Security software (authN/authZ, sandboxing, policy engines)

### Typical Claim Structure

**System claims:** processors + memory + instructions configured to perform algorithmic steps.  
**Method claims:** sequences of information-processing steps.  
**CRM claims:** instructions stored on non-transitory medium.

**Example Claim Skeleton:**
```
A computer-implemented method comprising:
  receiving input X;
  determining Y based on X;
  storing Y in memory; and
  transmitting Y to a client device.
```

### Common Prior Art Forms

**Patent Literature:** US/EPO/JP/CN patents on OS, storage, scheduling, GUIs, compilers.  
**NPL:** IEEE, ACM, USENIX, OSDI, SOSP, NSDI, FAST, PLDI, POPL, SIGMOD, VLDB.  
**Open Source:** GitHub, Linux kernel, Apache projects, PostgreSQL/MySQL docs.  
**Standards:** IETF RFCs, POSIX, SQL standards, W3C specifications.

### Key Litigation Issues
1. **Functional claiming & 112(f):** requires disclosed algorithm as corresponding structure.  
2. **Broad functional genus:** often vulnerable to 112(a) enablement and written description.  
3. **Predictable art obviousness:** combining known algorithms/data structures is frequently obvious.

---

## STAGE 2A: CLAIM CONSTRUCTION & ESTOPPEL ADAPTATIONS

### Special Rule Category 1: “Module / Logic / Engine / Component”
These are *software placeholders*, often triggering §112(f) if no structure is described. Construction must anchor to algorithms in the spec.

### Special Rule Category 2: “Configured to / to cause the processor to”
Treat as requiring actual programmed behavior. Links apparatus claims to method steps.

### Special Rule Category 3: Data Structures
Named structures (B‑trees, hash tables, queues) are limiting. Amending to a specific structure creates strong estoppel.

### Functional Language in Software
Terms like “dynamically”, “optimizing”, “intelligently selecting” require concrete algorithmic boundaries from spec or are vulnerable under 112.

---

## Technology-Specific Estoppel Patterns

### Pattern 1: Generic→Specific Algorithm or Data Structure
Amending “searching data” → “traversing a B‑tree index” surrenders alternative algorithms (hash tables, tries). HIGH estoppel.

### Pattern 2: Abstract→Specific Architecture
Amending to “proxy-based load balancing using weighted round-robin” surrenders alternative architectures and algorithms.

### Pattern 3: Business Method→Technical Protocol
Adding specifics like MVCC, logging, replication to overcome 101/103 creates high estoppel tied to those protocols.

---

## Festo Exception Analysis
Software is a *predictable art* → alternatives generally foreseeable → *unforeseeable* exception rarely applies.  
Tangential exception applies only if amendment is unrelated to prior art rationale.  
Other-reason applies for formal amendments (e.g., “non‑transitory”).

---

## DOE Considerations
- Algorithmic amendments strongly limit DOE.  
- Alternative algorithms/data structures rarely considered equivalent given foreseeability.  
- Vitiation risk high: cannot equate, e.g., B‑tree ↔ hash table.

---

## STAGE 2B: SEARCH & TECHNICAL ADAPTATIONS

### Primary Databases
1. **IEEE Xplore** — systems, architecture, security.  
2. **ACM DL** — OS, databases, PL, HCI.  
3. **USENIX / OSDI / SOSP / NSDI** — highly relevant to OS/storage/distributed systems.  
4. **arXiv & institutional tech reports**.  
5. **Open source documentation** (GitHub, Wayback Machine).  
6. **Google Patents / Espacenet** with CPC filters (G06F, G06Q).

### Query Structures
```
("thread scheduling" OR scheduler) AND (multicore OR SMP) AND ("work stealing" OR deque)
```
Or classification-driven:
```
CPC: G06F9/46 AND text:("cache eviction" OR "LRU" OR "adaptive replacement")
```

---

## NPL Source Priorities
Systems: OSDI, SOSP, NSDI, ATC  
Architecture: ISCA, MICRO, HPCA  
Databases: VLDB, SIGMOD, ICDE  
Security: S&P, USENIX Sec, CCS, NDSS  
PL: PLDI, POPL, OOPSLA  
HCI: CHI, UIST

---

## Expert Witness Recommendations
Experts should match domain: OS, distributed systems, DB/storage, compilers, security, HCI.  
Tasks: define PHOSITA, map algorithms/data structures, evaluate performance claims, present experiments when needed.

---

## STAGE 2C: SYNTHESIS ADAPTATIONS

### Vulnerability Pattern 1: Broad Functional Genus
Thin algorithmic disclosure → attack via 112(a).

### Vulnerability Pattern 2: Algorithm/Data Structure Narrowing
Use estoppel to block DOE and attack with prior art implementing disclosed algorithm.

### Vulnerability Pattern 3: Unsupported “Computer Improvement”
Performance claims with no evidence → weaken 103 and 112.

### Examiner Search Gaps
- Little use of NPL or open-source prior art.  
- Narrow CPC/keyword searches.  
- No search for algorithmic synonyms.

---

## EXAMPLES

### Example 1: Claim Construction — “Recommendation Module”
Construe to the specific algorithms disclosed (rules/ML models), not every recommendation algorithm.

### Example 2: Estoppel — “Data Structure”→“B‑Tree”
Surrenders non‑B‑tree structures; strong 103 opportunities.

### Example 3: Search Gap — Work‑Stealing Scheduler
Examiner searched generic scheduling; missed well-known deque-based work‑stealing literature.

---

## REFERENCES & RESOURCES
- IEEE/ACM/USENIX search guides  
- CPC G06F classification resources  
- Standard OS/DB/PL textbooks  
- IETF RFC libraries  

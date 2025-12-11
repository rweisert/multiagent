# TECHNOLOGY PACK: ELECTRONIC COMMERCE & BUSINESS SYSTEMS (TC 3600)
## Patent Invalidity Analysis – TC 3600-Specific Guidance

---

## STATUS: ⚠️ DRAFT (Phase 0)

First-pass technology pack focused on **systems and methods examined in TC 3600 – Transportation, Construction, Agriculture, Electronic Commerce, Licensing & Review, National Security-related**.

This pack is primarily aimed at **information-processing / business-method style inventions** in TC 3600, including:

- Electronic commerce (online marketplaces, shopping carts, checkout, payments)
- Finance, insurance, risk scoring, billing, pricing, promotions
- Advertising, recommendations, targeting, user profiling
- Logistics, transportation & routing **at the system/data level** (not the mechanical vehicle itself)
- Reservations, scheduling, ticketing, bookings
- Licensing, compliance, workflow, review/approval systems
- National security–related information systems (screening, watchlists, access control) that are essentially data/decision systems

**Mechanical structures and devices** (vehicles, machines, tools) are handled primarily by **TC 3700** and should use the mechanical/medical tech pack when the novelty is in physical structure rather than business logic.

---

## WHEN THIS PACK IS USED

**Tech Center(s):** TC 3600 – Transportation, Construction, Agriculture, Electronic Commerce, Licensing & Review, National Security-related  
**Technology Type:** e-commerce / business systems  
**Typical Art Units:** 3600-series **business methods, e-commerce, finance, logistics, and admin systems** art units

### Stage 1 Detection

Use this pack when:

- `Stage1.metadata.tech_center = "3600"`  
- `Stage1.metadata.technology_type` ∈ {"ecommerce", "business_methods", "finance", "insurance", "logistics", "transportation_systems", "scheduling", "advertising", "licensing", "workflow"}  
- `Stage1.metadata.tech_pack_file = "TECH_ECOM_BUSINESS_TC3600.md"`

AND at least one of:

- Independent claims recite **transactions, orders, offers, bids, accounts, users, customers, merchants, advertisers, publishers, policies, rules, workflows, approvals, scores, risk assessments, recommendations, or reservations**, implemented on **servers, client devices, networks, databases**.  
- The invention is framed as an improvement to **e-commerce, advertising, payments, pricing, risk management, logistics, or administrative/review processes**, not to underlying computer hardware or network protocols.  
- The specification uses heavy **business-domain language** (customers, orders, providers, policies, incentives, rewards, auctions, bids, reservations) with generic computer implementation.

### Route to Other Packs When

- Core novelty is in **computer architecture, OS, storage, or algorithms** (e.g., caching, DB internals, thread scheduling) → use **TC 2100 – Software** pack.  
- Core novelty is in **network routing, packet handling, VPNs, network security** → use **TC 2400 – Networking** pack.  
- Core novelty is in **wireless PHY/MAC, RF, radio signaling** → use **TC 2600 – Communications** pack.  
- Core novelty is in **mechanical structures or devices** (vehicle hardware, cranes, farming implements, etc.) → use **TC 3700 – Mechanical/Med Devices** pack.  

It is common that a TC 3600 case has **generic computing environment** plus **business-domain logic**; this pack is for those.

### Example Patent Types for This Pack (Illustrative)

- [E-commerce] – Dynamic pricing of items in an online marketplace based on demand and inventory levels.  
- [Payments] – Tokenization and authorization flows for online or mobile payments.  
- [Advertising] – Auction-based ad serving with budget and pacing controls.  
- [Recommendations] – Recommending products or content based on user behavior profiles.  
- [Logistics] – Assigning deliveries to drivers/routes based on constraints and costs.  
- [Licensing/Workflow] – Policy-based access/review/approval workflows for documents or licenses.  
- [National security] – Automated screening systems that match traveler data against watchlists.

---

## TECHNOLOGY CHARACTERISTICS

### Overview

TC 3600 business-method style cases typically combine:

- **Domain concepts:** orders, offers, accounts, users, merchants, inventories, policies, scores, routes, vehicles, shipments, tickets, ads, auctions, bids, budgets.  
- **Generic computing environment:** one or more servers, databases, networks, user devices, APIs, web frontends, mobile apps.  
- **Algorithms/heuristics:** rules, scoring functions, rankings, eligibility checks, threshold comparisons, constraint solvers.

The **technical content** of many TC 3600 patents is thin relative to domain modeling:

- Computers and networks are often described **at a high level** (e.g., generic servers, “the Internet”, “a web browser”).  
- Key “innovations” are frequently **new business rules**, workflows, or data relationships rather than novel computing techniques.

From an invalidity perspective:

- **§ 101 (Alice)** – Many claims raise abstract-idea issues (e.g., intermediated settlement, hedging risk, targeted advertising). Those are handled in **eligibility analysis**, not this pack, but they shape context.  
- **§ 103 (obviousness)** – Business methods implemented on generic computers are often predictable combinations of known **business practices** and **well-known computing tools** (databases, web forms, messaging).  
- **§ 112(a)/(b)** – Overly broad functional claims (“optimizing”, “maximizing revenue”, “improving efficiency”) with little algorithmic detail can be vulnerable on enablement/written description/indefiniteness grounds.

---

### Typical Claim Structure

Most TC 3600 business-method claims fall into:

1. **Computer-Implemented Method Claims**

> “A computer-implemented method for processing orders, comprising:  
>  receiving, by a server, an order from a client device;  
>  determining, by the server, a price based on [factors];  
>  storing the order and the price in a database; and  
>  transmitting a confirmation message to the client device.”

2. **System/Apparatus Claims**

> “A system comprising:  
>  one or more processors;  
>  a memory storing instructions that, when executed by the one or more processors, cause the system to: [carry out the same steps as the method].”

3. **Computer-Readable Medium Claims**

> “A non-transitory computer-readable medium storing instructions that, when executed, cause a processor to: [carry out the method].”

4. **“Platform” / “Network” Claims**

> “An electronic commerce platform comprising:  
>  a merchant interface;  
>  a consumer interface;  
>  a transaction engine;  
>  a recommendation engine;  
>  … where each is configured to perform [functions].”

**Common Claim Elements**

- **Actors:** users/customers, merchants/sellers, advertisers, publishers, drivers, riders, couriers, regulators, reviewers.  
- **Data structures:** accounts, profiles, items, listings, inventory records, orders, offers, bids, reservations, routes, ratings, reviews, scores, policies/rules.  
- **Actions:** receiving, transmitting, storing, updating, matching, scoring, recommending, authorizing, verifying, scheduling, assigning, notifying, logging.  
- **Conditions:** based on time, location, price, risk, rating, history, attributes, rules, thresholds.  
- **Results:** “improving efficiency”, “reducing fraud”, “maximizing revenue”, “optimizing matching”, “improving user experience”.

Dependent claims often:

- Narrow to **specific factors** (e.g., using customer location and purchase history).  
- Narrow to **specific rule/score types** (e.g., logistic regression, weighted sum).  
- Narrow to **payment methods, channels, or device types**.

---

### Common Prior Art Forms

**Patent Literature**

- Extensive portfolios on e-commerce, online advertising, payments, logistics, online auctions, recommendation systems, pricing, etc.  
- Many patents by large platforms (Amazon, eBay, Google, Meta, Microsoft, PayPal, Uber, Lyft, Expedia, airlines, shipping carriers).

**Non-Patent Literature (NPL)**

- **Academic CS/Econ/Operations Research:**  
  - Recommender systems (collaborative filtering, content-based, hybrid).  
  - Operations research / logistics (vehicle routing problems, scheduling, matching, auctions).  
  - Computer science HCI and web systems.  
- **Industry whitepapers and technical blogs** from major platforms.  
- **Standards and protocols** for payments, identity, security (e.g., PCI DSS docs, EMV, ISO 8583, OAuth).

**Commercial Systems / Product Documentation**

- Public documentation of platforms (user guides, developer docs, API docs, admin consoles).  
- Archived website behavior (Wayback Machine) for checkout flows, layout, and interactions.  
- Terms of service, help center articles describing workflows.

**Business Practice / Prior Use**

- Manuals, policy documents, training materials describing pre-computer versions of claimed methods.  
- Evidence of **longstanding brick-and-mortar practices** that the patent merely computerizes (layaway, coupons, loyalty points, tiered pricing, etc.).

---

### Key Litigation Issues (TC 3600 Business Systems)

**Issue 1: Functional Claiming & Abstract Business Logic**

- Claims often recite **results** (“optimizing”, “improving”, “reducing”) without concrete algorithmic detail.  
- Important to separate **business-domain abstractions** from **specific technical implementations**.

**Issue 2: Generic Computer / Network Context**

- Many patents place ordinary business concepts “on a computer” with generic servers and databases.  
- For 103, this often means combining **prior business methods** with **generic computing art**.

**Issue 3: Data Semantics vs Data Structures**

- Claims may treat particular sets of data as a new “data structure” (e.g., record with fields for X, Y, Z).  
- In reality, storing additional fields in a record is often an obvious extension.

---

## STAGE 2A: CLAIM CONSTRUCTION & ESTOPPEL ADAPTATIONS (TC 3600)

Stage 2A must adapt claim construction and estoppel analysis to business-method style software claims.

### Claim Construction Special Rules

---

#### Special Rule Category 1: “Module / Engine / Component” in Business Systems

**Description**

Terms like “transaction engine”, “recommendation module”, “risk scoring component”, “matching engine”, “auction module” are business-flavored analogues of the “module/engine” terms in software.

**Application**

- Determine whether the term is **pure business function** (no technical structure) or whether the spec describes **specific algorithms/data models**.  
- If claims were amended to specify particular algorithmic or data-structure details (e.g., weighted scoring, kind of model), treat that as narrowing.  
- Avoid treating “engine” terms as self-authenticating structure; scope should be tied to **disclosed processes**.

**Example**

> Term: “recommendation engine configured to recommend products based on user behavior”  
> Construction: Software executing on one or more processors that implements the recommendation processes described in the specification (e.g., collaborative filtering using purchase history and ratings), not any arbitrary method of recommending products.

---

#### Special Rule Category 2: “Transaction”, “Order”, “Offer”, “Bid”, “Reservation”

**Description**

Business artifacts are key to scope; their semantics can vary.

**Application**

- Use the spec to understand whether “transaction” includes **all interactions** or only ones that change account balances / ownership.  
- If applicant distinguished prior art based on types of “transactions” (e.g., “our system covers pre-authorization, not just settlement”), treat that as limiting.  
- For “reservation” or “booking”, clarify what rights are conferred (seat allocation, ticket issuance, time-of-service guarantee).

---

#### Special Rule Category 3: “Score”, “Risk”, “Rating”, “Relevance”

**Description**

Claims often rely on **scores** and **ratings** (e.g., risk scores, relevance scores, quality ratings) as key elements.

**Application**

- Construe “score” with reference to **inputs**, **scale**, and **use** described in the spec.  
- If applicant amended claims to specify particular **input features** or **weighting schemes**, treat those as limiting.  
- Avoid reading “score” as any operation on any inputs; anchor to the described modeling approach.

---

#### Special Rule Category 4: “Configured to” in Business Systems

**Description**

Apparatus claims use “configured to” to tie servers and systems to business-process steps.

**Application**

- Treat “configured to” as requiring **actual programming** to carry out steps, not mere generic capability.  
- In cases where standard software (e.g., off-the-shelf database + simple script) plainly implements claimed steps, highlight genericity in 103.

---

### Technology-Specific Estoppel Patterns (TC 3600)

---

#### Pattern 1: Generic Business Process → Narrowed to Specific Technical Workflow

**Typical Scenario**

- Original: “A method for processing transactions, comprising: receiving a transaction request; determining whether to authorize; and sending a response.”  
- Rejection: broad 103 and 101 rejections over generic authorization systems.  
- Amendment: Add **specific steps** (e.g., tokenization, CVV check, geo-location comparison, 3DS-type challenge flow).

**Estoppel Analysis**

- **Surrendered territory:** generic authorization flows without the specific added steps; flows using different sequences or data cross-checks if argued as critical.  
- **Estoppel risk:** HIGH – applicant ties patentability to specific workflow details.  
- **Litigation impact:** Prior art with different but similar flows may still be used for 103, while DOE for omitted steps is constrained.

---

#### Pattern 2: Generic “Scoring/Ranking” → Specific Formula / Feature Set

**Typical Scenario**

- Original: “calculating a score representing risk”.  
- Rejection: 103 over generic scoring/prior risk models.  
- Amendment: specify that score is computed as **Σ wi * feature_i** with defined features and thresholds.

**Estoppel Analysis**

- **Surrendered territory:** other feature sets, different linear/nonlinear models, different thresholds if not disclosed.  
- **Estoppel risk:** HIGH – specific scoring formula becomes the distinguishing feature.  
- **DOE impact:** cannot claim all risk scoring; limited to formulas close to those described.

---

#### Pattern 3: “Do it on the Internet” → Amendment to Particular Technical Context

**Typical Scenario**

- Original: “A method of selling goods, comprising: offering goods for sale; receiving orders; and processing payments.”  
- Rejection: 101/103 over long-standing practice.  
- Amendment: add “via a web server using HTTPS; storing orders in a relational database; performing card authorization via a payment gateway”.

**Estoppel Analysis**

- **Surrendered territory:** offline methods, non-HTTPS methods, non-relational storage if presented as differentiating.  
- **Estoppel risk:** MEDIUM–HIGH – but note: these “technical details” may still be generic.  
- **DOE impact:** expansions beyond the specific technologies used to gain allowance are constrained.

---

### Festo Exception Analysis – Business Systems

In TC 3600 business-method art:

- **Predictability:** Business rules and generic computing environments are usually **predictable**; alternative flows, feature sets, and modeling techniques are often foreseeable.  
- **Tangential exception:** Rare where amendments directly add steps/features to avoid prior art; more plausible for amendments cleaning claim language or aligning to prior spec language without substantive change.  
- **Unforeseeable exception:** Hard to meet; alternative algorithms, machine learning methods, or communication channels are usually foreseeable.  
- **Other-reason exception:** Possible where amendments respond only to 101 **form** issues (e.g., specifying “non-transitory” CRM, adding “computer-implemented”) and can be shown not to have been relied on to overcome 102/103.

Stage 2A should mostly treat **substantive workflow/feature amendments** as generating **strong estoppel**.

---

### DOE Considerations – Business Systems

DOE is heavily constrained in business-method context:

- Structural “way” of performing a business process is usually defined by **sequence of steps, data types, and conditions**.  
- Changes to **inputs/conditions** or **step ordering** often materially change the “way” even if high-level function is “process a transaction”.  
- Where applicant narrowed claims from broad “any scoring” to a particular formula or model, DOE around that boundary is limited.

---

## STAGE 2B: SEARCH & TECHNICAL ADAPTATIONS (TC 3600)

Stage 2B exploits common search gaps in TC 3600: underuse of **commercial practice**, **web archives**, and **non-patent research**.

### Primary Databases & Sources (Priority Order)

**1. Patent Databases**

- USPTO / EPO / WIPO / CNIPA patents on e-commerce, advertising, payments, logistics, scheduling.  
- Use CPC: G06Q (data processing systems for administrative, commercial, financial, managerial), plus G06F for implementation details.

**2. Academic / Research Literature**

- Recommender systems: SIGIR, KDD, WWW, RecSys.  
- Auctions/markets: EC (Electronic Commerce), economics journals, operations research.  
- Logistics & routing: OR/MS conferences & journals (vehicle routing, assignment, scheduling).  
- Fraud/risk scoring: security / machine learning venues.

**3. Commercial Systems & Documentation**

- Major platforms: e-commerce sites, ad networks, payment processors, logistics and ride-sharing platforms.  
- Public technical docs: API references, developer portals, integration guides.  
- Help center docs and FAQs describing workflows for users/merchants.

**4. Web Archives & Screenshots**

- Wayback Machine snapshots of websites showing earlier checkout flows, ad interfaces, recommendation layouts, etc.  
- Archived app store listings and screenshots of apps.

**5. Standard/Guideline Documents**

- Payment industry standards (PCI DSS, EMV specs, ISO message formats).  
- Security/authentication frameworks (OAuth, OpenID Connect, SAML) used in enterprise workflows.

---

### Search Query Structures

**A. E-commerce / Checkout Example**

```text
("online shopping" OR "e-commerce" OR "checkout") AND
("shopping cart" OR "cart" OR "basket") AND
("promotion" OR "coupon" OR "discount" OR "voucher")
```

CPC focus (patents):

```text
CPC: G06Q30/* AND text:("shopping cart" OR "checkout" OR "online order")
```

**B. Advertising / Auction Example**

```text
("online advertising" OR "ad serving" OR "ad auction") AND
("bidding" OR "auction" OR "real-time bidding" OR RTB) AND
("budget" OR "pacing" OR "frequency capping")
```

CPC focus:

```text
CPC: G06Q30/02 AND text:("auction" OR "bidding" OR "sponsored search")
```

**C. Logistics / Routing Example**

```text
("vehicle routing" OR "delivery routing" OR "last-mile delivery") AND
("assignment" OR "matching" OR "scheduling") AND
("constraints" OR "capacity" OR "time window")
```

For non-patent OR literature, emphasize hitting key algorithm names (e.g., “VRP”, “Hungarian algorithm”, “matching market”, “stable matching”, etc.).

---

### NPL Source Priorities (TC 3600 Business)

- **CS / Data Mining / ML / IR:** KDD, WWW, SIGIR, RecSys, NeurIPS/ICML/ICLR for recommendation/ads.  
- **Operations research / logistics:** Transportation Science, Transportation Research B/C, OR, Management Science.  
- **Economics / mechanism design:** EC (ACM Conference on Economics and Computation), econ journals covering auctions, pricing, and matching.  
- **Security / risk:** security venues for fraud detection methods.  
- **Industry:** whitepapers from big platforms (Google Ads, Amazon, Facebook, Uber, etc.).

---

### Expert Witness Recommendations

**Primary Expert Types**

- **Computer scientist / data scientist** – for recommendation, scoring, ranking, and systems aspects.  
- **Economist / operations researcher** – for auctions, pricing, matching, routing, scheduling.  
- **Domain expert** – for specific regulated domains (insurance, payments, securities, national security, licensing).

**Qualifications**

- PhD or extensive industry experience in relevant area (ads, recommender systems, OR, finance).  
- Publications in key conferences/journals or experience at major platforms.  
- Familiarity with **pre-filing practices and systems** in the industry.

**Typical Expert Tasks**

- Explain what was **well-known** at the relevant time (e.g., second-price auctions, collaborative filtering, VRP).  
- Map prior art systems/papers to claim steps.  
- Analyze **predictability** of combining business rules with generic computing.  
- Assess whether claimed benefits (e.g., “better matching”, “fraud reduction”) were expected given known methods.

---

## STAGE 2C: SYNTHESIS ADAPTATIONS (TC 3600)

Stage 2C integrates business-domain context, claim construction, estoppel patterns, and search gaps.

### Technology-Specific Vulnerability Patterns

---

**Vulnerability Pattern 1: “Computerizing” Longstanding Business Practice**

- **Description:** The patent takes a known offline practice (e.g., coupons, layaway, dynamic pricing, auctions, loyalty points, reviews) and implements it using generic computers and networks.  
- **Exploitation:**  
  1. Identify prior art describing offline practice.  
  2. Identify prior art systems showing **generic computerization** of similar practices.  
  3. Use 103 to frame the patent as a predictable combination.

---

**Vulnerability Pattern 2: “Scoring/Recommendation” with Generic Models**

- **Description:** Claims a scoring function or recommendation engine that uses widely-known techniques (weighted sums of features, collaborative filtering, logistic regression) with an application-specific label.  
- **Exploitation:**  
  1. Use ML/IR/recommender literature to show generic nature of the method.  
  2. Show business features are straightforward feature engineering given the domain.  
  3. Argue obviousness in light of generic modeling + domain-specific variables.

---

**Vulnerability Pattern 3: “Platform / Marketplace” with Standard Components**

- **Description:** A “platform” with user interface, merchant interface, inventory, payments, messaging, reviews, recommendations.  
- **Exploitation:**  
  1. Show that these are standard components of online marketplaces.  
  2. Use early e-commerce sites and prior art patents to document each component.  
  3. Argue that the particular combination is a predictable arrangement of standard modules.

---

### Common Prosecution Mistakes (TC 3600)

1. **Overbroad Functional Claims with Sparse Technical Detail**  
   - Result: 112 vulnerabilities and difficulty distinguishing prior art.

2. **Relying on Business Novelty as Technical Novelty**  
   - “Nobody has ever sold X this way before” is not a technical distinction if the computerization is generic.

3. **Narrowing via Specific Rules Without Recognizing Estoppel**  
   - Adding specific rule sets or workflow steps to avoid prior art, but later asserting broad coverage.

---

### Typical Examiner Search Gaps (TC 3600)

**Gap Type 1: Limited Use of Non-Patent Commercial Practice**

- Examiner may not fully explore prior **offline/online business practices**, focusing instead on patents and a few papers.

**Gap Type 2: Underuse of CS/OR/Econ Literature**

- Academic literature on auctions, recommendations, and routing is vast; examiners may sample only superficially.

**Gap Type 3: Weak Web/Archive Searches**

- Historic web UI flows, product features, and platform behaviors are often not systematically used as prior art.

**Search Strategy**

- Use **web archives**, product docs, and academic literature systematically to reconstruct state of practice.  
- Tie those sources to claim elements and business practices.

---

## EXAMPLES (TC 3600)

### Example 1: Claim Construction – “Order” vs “Offer”

**Fact Pattern**

- Claim recites “receiving an order from a user” then “sending an offer to a merchant”.  
- Spec defines “order” as a **firm commitment to purchase** and “offer” as a **request for fulfillment**.

**Analysis**

- “Order” should be construed as a **completed user commitment**, not just a browsing action.  
- “Offer” should be construed as a **downstream request**, not a generic communication.  
- This can narrow scope relative to prior art where “orders” are used loosely.

---

### Example 2: Estoppel – Generic Scoring → Specific Feature Set

**Fact Pattern**

- Original: “determining a risk score based on transaction data”.  
- Amendment: “determining a risk score based on: (i) transaction amount; (ii) merchant MCC; (iii) device fingerprint; and (iv) velocity of recent transactions, using a weighted sum”.  
- Applicant argued that prior art did not use this specific combination.

**Estoppel**

- Surrenders scores using substantially different features/combos if those differences were relied on for patentability.  
- DOE around feature combinations is constrained.

---

### Example 3: Search Gap – Platform Features in Early E-commerce Sites

**Fact Pattern**

- Patent claims: cart + recommendation + saved payment + user review + loyalty points.  
- Examiner cites only patents and one late article.

**Search Plan**

- Use Wayback Machine snapshots of early major e-commerce sites.  
- Identify presence and integration of carts, recommendations (e.g., “Customers who bought this also bought…”), stored cards, reviews, and loyalty programs.  
- Use dated evidence to show all features existed and were combined before priority date.

---

## TECHNOLOGY EVOLUTION CONSIDERATIONS (TC 3600)

- E-commerce and online platforms evolved rapidly from mid-1990s onward. Many patterns (shopping carts, one-click, recommendations, auctions, ratings) emerged early and became standard.  
- Online advertising and RTB evolved with similar patterns: auctions, targeting, budgets, pacing.  
- Logistics and routing have long histories in operations research that predate modern platforms.

Implication: **Rich prior art** often exists in business practice, academic work, and early web systems; TC 3600 patents are frequently incremental overlays.

---

## QUALITY CHECKS

Before relying on this pack for a case:

- Confirm that the patent is **business/e-commerce/system-focused**, not primarily mechanical or deep technical software/networking.  
- Verify Stage 2A has anchored “modules/engines” to concrete algorithms / workflows where possible.  
- Identify any narrowing amendments specifying particular **flows, formulas, feature sets, or technical contexts**; treat them as estoppel patterns.  
- Ensure Stage 2B has included **non-patent commercial, academic, and web/archive sources**, not just patents.  
- Verify expert domains (CS/ML, OR/econ, domain specialists) match the patent’s subject matter.

---

## REFERENCES & RESOURCES (TC 3600)

(Non-exhaustive, for production refinement.)

- CPC G06Q (data processing systems for administrative, commercial, financial, managerial purposes).  
- Academic venues: KDD, WWW, SIGIR, RecSys, EC, OR/Management Science journals.  
- Industry docs: platform whitepapers, API docs, security/payment standards.  
- Web archives: Wayback Machine and similar.

---

## REVISION HISTORY

**Version 0.1 – December 2025**

- Initial draft of **TECH_ECOM_BUSINESS_TC3600.md**.  
- Structured to mirror other tech packs and tuned for TC 3600 business/e-commerce/logistics/licensing systems.  
- Needs 3–5 real-file-wrapper examples and further refinement for Phase 1 “production ready” status.


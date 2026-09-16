# FinSight AI — Graph Readiness Audit (Phase 2, Part 12)

**Status:** structural assessment based on IEEE-CIS's publicly documented
schema. The "Unique count" and "Missing %" columns are **TBD** until
`python -m src.data.profile` runs against the real files — this table
does not invent those numbers.

## Graph readiness table

| Entity | Available? | Unique Count | Missing % | Linkage Potential | Future Graph Use |
|---|---|---|---|---|---|
| card1 (numeric card/account proxy) | Yes | TBD (documented as high-cardinality) | TBD (documented as low) | **High** — most complete, most granular proxy for a recurring "account" | Primary candidate entity-graph key: Transaction → uses → Card1-node |
| card2–card6 | Yes | TBD | TBD (card2/3/5 documented as sometimes missing; card4/6 low-cardinality categorical) | Moderate — useful as card1 co-attributes, not standalone keys | Node/edge FEATURES on the card1 node, not separate node types |
| addr1, addr2 | Yes | TBD | TBD (documented as frequently missing) | **Low-Moderate** — granularity/meaning not confirmed (region code, not a clean geography) | Possible weak Location-node proxy; do not present as a confirmed "geography" dimension without verifying against real data |
| DeviceType | Yes (identity table only) | 2 documented categories (desktop/mobile) | TBD (identity table itself only covers a documented minority of transactions) | Low standalone, but strengthens device-sharing detection combined with DeviceInfo | Device-node coarse category |
| DeviceInfo | Yes (identity table only) | TBD (documented as high-cardinality, messy free text) | TBD | **Moderate-High after normalization** — raw strings need cleaning (e.g. "SM-G935F Build/NRD90M" vs "SM-G935F") before being a reliable join key | Best candidate Device-node key, but ONLY after a normalization step not yet built (flagged for Phase 3/4) |
| P_emaildomain / R_emaildomain | Yes | TBD (documented set of common providers) | TBD (documented as partially missing, R often blank) | Moderate — email PROVIDER is shared by design (many legitimate users share "gmail.com"), so raw domain is a weak node; only useful combined with other identifiers to detect suspicious clustering | Email-domain as an edge attribute, not a strong standalone node |
| TransactionID | Yes | 100% unique by construction (primary key) | 0% | N/A (this IS the transaction node itself) | Transaction node identity |
| A true "customer_id" | **No** | — | — | None — does not exist in IEEE-CIS | Cannot build a Customer node without fabricating one; we do not do this |
| A true "merchant_id" / merchant name | **No** | — | — | None — ProductCD is a product CATEGORY, not a merchant identity | Cannot build a Merchant node without fabricating one; we do not do this |
| A confirmed geolocation (lat/long, city, country) | **No** | — | — | addr1/addr2 are anonymized region codes of undisclosed granularity | Cannot build a reliable Location node beyond a weak addr1/addr2 proxy |

## Graph GO / NO-GO recommendation

**Conditional GO, feature-based first — full GNN deferred pending Experiment 4 evidence.**

Reasoning:
- IEEE-CIS supports a genuine, defensible graph construction using
  **card1** as the primary recurring-entity key and **DeviceInfo**
  (post-normalization) and **P_emaildomain** as secondary linking
  attributes. This directly matches Phase 1 RQ1/RQ7.
- It does **not** support a true multi-entity-type graph (Customer,
  Merchant, Location as clean node types) the way the Phase 1 conceptual
  architecture sketched — those entities don't exist in this dataset with
  confirmed identity, and Phase 2's explicit instruction is not to
  fabricate them. The realistic graph for this dataset is closer to a
  **single-entity-type graph** (Transactions linked via shared card1 /
  device / email attributes) than the full multi-node schema in the
  Phase 1 blueprint.
- Per Phase 1 Part 14's own instruction ("evaluate whether GNN is
  actually justified... if too ambitious, propose a graph-feature-based
  alternative"): Phase 3 should start with **graph-derived tabular
  features** (shared-card1 count, shared-device count, node degree,
  simple community ID via a lightweight algorithm) rather than committing
  to a full GNN implementation up front. A full GNN (Experiment 5 in the
  Phase 1 ML design) should only be attempted if Experiment 4 (graph
  features + GBM) shows a PR-AUC ceiling that graph features alone can't
  reach, AND the real, profiled graph density supports it.

**What must happen before this recommendation is finalized:** run
`src.data.profile` against the real data and confirm card1's actual
unique-count / repeat-transaction-rate is high enough to form a graph
with meaningful edge density (a card1 that appears only once per value
would produce an empty graph, not a sparse one — that distinction matters
and is currently unmeasured).

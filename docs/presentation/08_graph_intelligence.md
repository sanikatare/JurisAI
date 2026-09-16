# Slide 8: Temporal Graph Intelligence

## Relational Entity Graph Features
- **Identifiers**: `card1`, `DeviceInfo`, `P_emaildomain`.
- **Extracted Features**:
  - `graph_card1_prior_degree`: Historical transaction count per card.
  - `graph_shared_device_prior_tx_count`: Distinct card entities sharing the same device prior to transaction execution.
  - `graph_relational_risk_score`: Log-transformed relational risk intensity.
- **Impact**: Provides **+0.0066 PR-AUC lift** and +2.21% Recall boost by identifying multi-account fraud rings.

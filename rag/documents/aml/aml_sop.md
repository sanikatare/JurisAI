# Anti-Money Laundering (AML) & Suspicious Activity Investigation SOP

**Document ID**: `POL-AML-2026-v1`  
**Category**: AML Compliance  
**Source**: Financial Crime Investigation Standard Operating Procedure  
**Effective Date**: January 2026  

## 1. Purpose & Scope
This Standard Operating Procedure outlines the required protocol for investigating transactions exhibiting anti-money laundering (AML) risk indicators, device-sharing anomalies, or rapid velocity patterns.

## 2. Key AML Risk Indicators
1. **Device Sharing**: When a single device identifier (`DeviceInfo`) is linked to 3 or more distinct account/card entities (`card1`) within a 24-hour window, the transaction presents elevated risk of coordinated structuring or bot activity.
2. **Velocity Anomalies**: Multiple high-value transactions originating from the same IP or email domain within short temporal gaps (under 300 seconds) warrant immediate operational investigation.
3. **Email Provider Clustering**: Transactions originating from newly registered or anonymous email domains (`P_emaildomain`) that exhibit zero historical transaction volume must be flagged for secondary review.

## 3. Mandatory Analyst Actions
- **Verification**: Check historical transaction logs for the associated `card1` entity.
- **Relational Mapping**: Inspect connected transactions sharing the same device or email domain.
- **Documentation**: Record all supporting evidence IDs (`EVID-ML-001`, `EVID-GRAPH-001`) in the formal case report.
- **Enforcement Restriction**: Analysts must NOT freeze accounts automatically without secondary compliance sign-off.

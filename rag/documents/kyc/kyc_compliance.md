# Customer Identification & KYC Risk Guidelines

**Document ID**: `POL-KYC-2026-v1`  
**Category**: KYC Compliance  
**Source**: Global Regulatory Compliance Handbook  
**Effective Date**: January 2026  

## 1. Overview
Know Your Customer (KYC) standards require financial institutions to verify customer identity and maintain accurate entity records to prevent identity fraud and synthetic account creation.

## 2. High-Risk Indicators for Unverified Entities
- **Missing Identity Metadata**: Transactions lacking identity attributes (missing `DeviceType` or `DeviceInfo`) combined with high-dollar amounts ($> \$200.00$) require enhanced due diligence.
- **Mismatch in Regional Identifiers**: Discrepancy between billing address region codes (`addr1`) and issuing card country metadata.
- **Product Category Vulnerability**: Product category codes `C` and `R` have historically higher fraud rates during initial account setup.

## 3. Investigation Protocol
1. Evaluate whether the entity has an established transaction history ($> 5$ historical transactions).
2. Assess if the transaction amount deviates by $> 2.0 \times$ standard deviations from the cardholder's prior mean amount.

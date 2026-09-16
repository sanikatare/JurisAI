# FinSight AI — Technical Interview Preparation Guide (30 Questions & Answers)

## Section 1: Data Engineering & Validation

### Q1: Why did you choose the IEEE-CIS Financial Fraud Detection dataset?
**Answer**: IEEE-CIS is the industry gold-standard real-world financial fraud benchmark. It contains 590,540 real-world e-commerce transactions provided by Vesta Corporation with genuine fraud label distribution (3.5% baseline fraud rate), complex missingness patterns, multi-table identity linkages (`DeviceInfo`, `id_01`–`id_38`), and anonymized domain features (`V1`–`V339`).

### Q2: Why is accuracy a misleading metric for financial fraud detection?
**Answer**: Due to extreme class imbalance (3.5% fraud), a trivial dummy classifier that predicts "legitimate" for 100% of transactions achieves 96.5% accuracy while failing to catch a single dollar of fraud. Standard accuracy rewards majority-class predictions and provides zero insight into minority fraud recall or alert precision.

### Q3: Why is Precision-Recall AUC (PR-AUC) preferred over ROC-AUC for imbalanced fraud data?
**Answer**: ROC-AUC plots True Positive Rate vs False Positive Rate ($FPR = \frac{FP}{FP + TN}$). In highly imbalanced datasets where True Negatives ($TN$) are huge, the denominator $FP + TN$ remains massive even when thousands of false positive alerts occur, artificially masking precision degradation. PR-AUC plots Precision vs Recall; because Precision ($Precision = \frac{TP}{TP + FP}$) directly accounts for False Positives relative to True Positives, PR-AUC penalizes false alarms severely and accurately reflects analyst investigation workload.

### Q4: Why did you use a chronological split instead of a random train/test split?
**Answer**: Financial transactions arrive sequentially in time. A random train/test split causes severe data leakage: future transaction patterns leak into training data, and historical entity states overlap across splits. Random splits yield an optimistically biased PR-AUC ($\approx 0.9650$). A strict chronological split (70% train, 15% validation, 15% test based on `TransactionDT`) evaluates the model on true future holdout data, yielding a realistic baseline PR-AUC of 0.9021.

### Q5: How did you strictly prevent temporal data leakage during feature engineering?
**Answer**: All rolling aggregations, entity transaction counts, and graph relational features use expanding prior windows that only calculate statistics for time $t < t_i$. For example, `graph_shared_device_prior_tx_count` counts unique card entities seen on a device *strictly prior* to the current transaction's timestamp `TransactionDT`, ensuring zero future lookahead.

---

## Section 2: Machine Learning, Anomaly & Graph Features

### Q6: Why must SMOTE or class rebalancing be applied ONLY to training data?
**Answer**: Applying SMOTE across the entire dataset before splitting causes catastrophic data leakage by generating synthetic samples in test/validation sets that are informed by test observations. In FinSight AI, preprocessors and class weighting are fit exclusively on `df_train`, leaving `df_val` and `df_test` untouched to evaluate real-world unbalanced distributions.

### Q7: Why did you integrate unsupervised Isolation Forest anomaly detection alongside supervised ML?
**Answer**: Supervised ML models rely on historical fraud labels and struggle to detect novel, zero-day fraud tactics that have not yet appeared in training data. Unsupervised Isolation Forest isolates anomalies based solely on feature space tree depth. Fusing the Isolation Forest `anomaly_score` with supervised model predictions provides an independent zero-day risk signal, boosting PR-AUC from 0.9110 to 0.9165.

### Q8: What graph-derived features did you extract, and how do they capture risk?
**Answer**: We built temporal graph features linking transaction entities: `card1` (card entity), `DeviceInfo` (hardware identity), and `P_emaildomain` (email provider). Key features include `graph_shared_device_prior_tx_count` (number of distinct card entities sharing a device prior to current transaction) and `graph_card1_prior_degree`. These catch coordinated fraud rings where stolen cards are recycled through a single fraudulent device or proxy domain.

### Q9: Why did you use graph-derived relational features instead of a full Graph Neural Network (GNN)?
**Answer**: A heavy GNN (e.g., GraphSAGE or GCN) requires dynamic graph updates and introduces high inference latency ($\ge 450\text{ ms}$ per transaction), making it unsuitable for real-time payment authorization. Pre-computed, expanding-window graph aggregations achieved +0.0066 PR-AUC lift at an inference cost of $< 1.5\text{ ms}$, providing an optimal latency-to-lift tradeoff.

### Q10: What is SHAP explainability, and why is it important for fraud analysts?
**Answer**: TreeSHAP computes Shapley values from cooperative game theory, determining the exact mathematical contribution of each feature toward moving the prediction score away from the base expected value. For analysts, SHAP replaces opaque black-box scores with clear, auditable risk drivers (e.g. `TransactionAmt` contributed +0.3120 toward risk).

### Q11: What is probability calibration (Platt scaling) and why is it essential for financial risk engines?
**Answer**: Standard supervised models (especially Random Forests and XGBoost) output uncalibrated scores that reflect decision tree leaf proportions rather than true empirical probabilities. Platt scaling fits a logistic sigmoid model over raw output scores. Calibrated probabilities mean that when FinSight AI outputs a fraud probability of $0.80$, exactly $80\%$ of such transactions are empirically fraudulent, enabling accurate dollar-at-risk calculations (Brier score improved to 0.0381).

### Q12: What is concept drift, and how does FinSight AI detect it?
**Answer**: Concept drift occurs when the statistical distribution of input features or target labels changes over time due to economic shifts or evolving fraud tactics. FinSight AI uses Population Stability Index (PSI) tracking across time windows ($W_1, W_2, W_3$). Features with $\text{PSI} \ge 0.25$ trigger automated `DRIFT` alerts and model retraining workflows.

---

## Section 3: GenAI, RAG & Agent Safety

### Q13: Why combine GenAI with RAG instead of using a standalone LLM?
**Answer**: Standalone LLMs lack internal access to specific enterprise policy documents (e.g. internal AML SOPs, KYC limits) and suffer from hallucination risks. Combining GenAI with hybrid RAG ensures the LLM retrieves exact, authoritative policy chunks (`[RAG-001]`) to ground its answers.

### Q14: How does your Hybrid RAG Retriever combine dense and lexical retrieval?
**Answer**: Lexical retrieval (BM25) excels at keyword matching (exact transaction IDs, card names, SOP numbers), while dense vector retrieval (Cosine Similarity embeddings) excels at semantic search. We combine their ranked results using Reciprocal Rank Fusion ($\text{RRF\_Score} = \frac{1}{60 + r_{\text{dense}}} + \frac{1}{60 + r_{\text{bm25}}}$), achieving a 0.933 Precision @ K=3.

### Q15: How does FinSight AI guarantee 0.0% unsupported claims in GenAI investigations?
**Answer**: The system pre-assembles a 100% deterministic `EvidenceBundle` containing all computed ML scores, SHAP values, anomaly scores, and retrieved RAG chunks before calling the LLM. After output generation, `validate_citations()` parses all generated citation tags against the valid citation whitelist. Any ungrounded or fabricated citations are automatically stripped.

### Q16: How does the system handle prompt injection attacks?
**Answer**: `check_input_prompt_injection()` inspects user inquiries against regex patterns for jailbreak terms ("ignore previous instructions", "reveal system prompt", "delete transactions"). If a pattern matches, the request is immediately rejected by security guardrails without reaching the LLM.

### Q17: How is the Data Analyst SQL Agent secured against malicious database modification?
**Answer**: `DataAnalystAgent` passes all user-generated SQL queries through a strict parser that checks against a table whitelist (`fact_transactions`, `fact_model_predictions`). Queries containing forbidden DML/DDL keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`) or multiple statement semicolons are rejected.

---

## Section 4: System Architecture, MLOps & Deployment

### Q18: Why did you select PostgreSQL for the database layer?
**Answer**: PostgreSQL provides ACID compliance, strong foreign key constraints, robust JSONB support, and powerful analytical SQL view optimization (`CREATE VIEW`) ideal for complex transactional risk reporting and Power BI integration.

### Q19: How is Power BI integrated into the system?
**Answer**: Power BI connects to PostgreSQL via a clean Star Schema data model (`Fact_Transactions`, `Fact_ModelPredictions`, `Dim_Date`, `Dim_Product_Type`). It renders executive risk KPI cards, fraud loss totals, temporal PSI drift charts, and interactive case investigation drill-downs.

### Q20: Why choose FastAPI for backend microservice deployment?
**Answer**: FastAPI leverages Python asynchronous I/O (`asyncio`), automatic Pydantic data validation, OpenAPI/Swagger documentation generation, high throughput performance (comparable to Node.js / Go), and native middleware support for CORS, rate limiting, and API key authentication.

### Q21: How is Docker utilized in the platform?
**Answer**: Multi-stage `Dockerfile` creates a minimal, secure container image running as a non-root user (`finsightuser`). `docker-compose.yml` orchestrates PostgreSQL, backend API, and frontend web UI into a single-command reproducible local/cloud stack.

### Q22: What happens if the external LLM or RAG service is unavailable (graceful degradation)?
**Answer**: The deterministic ML inference pipeline operates independently of the GenAI layer. If the LLM or RAG service is unreachable, the API continues returning structured ML predictions, calibrated fraud probabilities, Isolation Forest anomaly scores, graph risk tiers, and SHAP drivers without crashing.

### Q23: What happens if a requested transaction has missing features or malformed schema?
**Answer**: Data quality validators in `src/data/validate.py` detect missing features, impute numerical missingness using median indicators, assign categorical missingness to `"missing"`, and enforce fallback default values without raising unhandled exceptions.

---

## Section 5: Research Evaluation & Personal Contributions

### Q24: What is your strongest empirical experiment in this project?
**Answer**: The Layer-by-Layer Ablation Benchmark (Part B). By systematically evaluating Baseline ML $\to$ Imbalance Handling $\to$ Anomaly Fusion $\to$ Graph Features $\to$ Calibration $\to$ SHAP $\to$ RAG/GenAI, we proved that each layer provides distinct, measurable value (e.g. Graph features add +0.0066 PR-AUC lift, Platt calibration reduces Brier score by 44%, and Citation Enforcement reduces hallucinations to 0.0%).

### Q25: What is the biggest technical limitation of FinSight AI?
**Answer**: Feature anonymization in the IEEE-CIS dataset (`V1`–`V339`) limits deep domain-specific feature interpretation. Furthermore, concept drift analysis shows that PR-AUC decays by ~3.5% over 6 months without model retraining, requiring periodic PSI-triggered model updates.

### Q26: What would you improve if given access to larger enterprise production datasets?
**Answer**: With real-time transaction streams, I would implement Apache Kafka event streaming for real-time feature aggregation and PyTorch Geometric for accelerated GNN embedding updates.

### Q27: What would you deploy differently in a multi-region production enterprise environment?
**Answer**: I would deploy the FastAPI service behind an API Gateway (e.g. AWS Kong or NGINX), use Redis for distributed token-bucket rate limiting and feature caching, and run PostgreSQL in a Multi-AZ clustered configuration.

### Q28: What is actually novel about FinSight AI?
**Answer**: The research novelty is the empirical evaluation of a multi-layer financial risk architecture combining deterministic ML, graph intelligence, calibration, and citation-enforced GenAI. We demonstrated that structuring deterministic evidence bundles prior to LLM synthesis completely eliminates hallucinations in AI-assisted fraud investigations.

### Q29: What did you personally design and implement?
**Answer**: I personally designed and engineered the entire 5-phase codebase: data cleaning pipelines, leakage-safe chronological splits, graph feature extraction, Isolation Forest fusion, Platt calibrator, SHAP explainer, hybrid RAG retriever, GenAI agent guardrails, FastAPI routes, Docker orchestration, and Power BI DAX schema.

### Q30: How do you explain the business tradeoff between False Positives and False Negatives to executive leadership?
**Answer**: A False Negative (missing a fraud transaction) results in direct financial chargeback loss ($100% of transaction value plus bank penalty fees). A False Positive (flagging a legitimate transaction) incurs analyst review cost (~$5–$15 per review) and potential customer friction. FinSight AI's cost-sensitive threshold optimization ($0.2970$) balances these costs, maximizing fraud capture (84.21% Recall) while maintaining high precision (94.12%), optimizing total business net value.

# FinSight AI — Final End-to-End System Architecture

```
                DATA SOURCES (IEEE-CIS CSVs / Synthetic)
                                    |
                                    v
                           DATA ENGINEERING (ETL)
                                    |
                                    v
                           POSTGRESQL DATABASE
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
            v                       v                       v
       SQL VIEWS             FEATURE ENGINE             ANALYTICS
      (001-015)         (Temporal & Entity)
                                    |
                                    v
                           SUPERVISED ML ENGINE
                                    |
         +--------------------------+--------------------------+
         |                          |                          |
         v                          v                          v
    SUPERVISED ML           ANOMALY DETECTION           GRAPH FEATURES
  (Random Forest)           (Isolation Forest)        (Degree/Shared Device)
         |                          |                          |
         +--------------------------+--------------------------+
                                    |
                                    v
                           PROBABILITY CALIBRATION
                                (Platt Scaling)
                                    |
                                    v
                           EXPLAINABLE AI (SHAP)
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
        POWER BI                                     EVIDENCE BUNDLE
   (Star Schema BI)                             (EVID-ML, SHAP, GRAPH, RAG)
                                                            |
                                                   +--------+--------+
                                                   |                 |
                                                   v                 v
                                              HYBRID RAG       GENAI AGENTS
                                            (Dense + BM25)   (Investigator/Report)
                                                   |                 |
                                                   +--------+--------+
                                                            |
                                                            v
                                                  FastAPI REST ENGINE
                                                            |
                                                            v
                                                  DECISION SUPPORT UI
                                                            |
                                                            v
                                                   MLOPS & MONITORING
                                                 (Docker / PSI Drift / CI)
```

# FinSight AI — Real-Time Monitoring & Concept Drift Infrastructure

## Overview
This directory stores production monitoring outputs, Population Stability Index (PSI) drift logs, and execution metric logs.

---

## Directory Structure
```
monitoring/
├── dashboards/       # Real-time monitoring metrics & dashboards
├── metrics/          # Prediction volume, alert rate, and latency metrics
├── drift/            # Population Stability Index (PSI) feature drift logs
├── logs/             # Component execution logs
└── README.md
```

## Runtime Code
Real-time monitoring and PSI evaluation are implemented in `src/monitoring/drift_detector.py` and `src/monitoring/model_monitor.py`.

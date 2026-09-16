"""Interactive Investigation Workspace & Decision Support UI — Phase 4 Part 18.

Serves the standalone HTML/JS Investigation Workspace for analysts.
"""
from __future__ import annotations

import os

HTML_WORKSPACE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinSight AI — Decision Support & Investigation Workspace</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-red: #f43f5e;
            --accent-green: #34d399;
            --accent-amber: #fbbf24;
            --border-color: #334155;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }
        .header h1 { margin: 0; font-size: 24px; color: var(--accent-blue); }
        .badge-live {
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent-blue);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            border: 1px solid var(--accent-blue);
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 24px;
        }
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
            margin-bottom: 24px;
        }
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .stat-box {
            background: rgba(15, 23, 42, 0.6);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-label { font-size: 12px; color: var(--text-muted); }
        .stat-val { font-size: 20px; font-weight: 700; margin-top: 4px; }
        .stat-high { color: var(--accent-red); }
        .stat-medium { color: var(--accent-amber); }
        .indicator-list { list-style: none; padding: 0; margin: 0; }
        .indicator-item {
            background: rgba(15, 23, 42, 0.4);
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 8px;
            font-size: 14px;
            border-left: 3px solid var(--accent-red);
        }
        .citation-tag {
            color: var(--accent-blue);
            font-weight: 600;
            cursor: pointer;
        }
        .btn {
            background: var(--accent-blue);
            color: #0f172a;
            border: none;
            padding: 10px 18px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { opacity: 0.9; }
        pre { background: #090d16; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="header">
        <h1>FinSight AI — Decision Support & Investigation Workspace</h1>
        <span class="badge-live">PHASE 4 GENAI ENGINE OPERATIONAL</span>
    </div>

    <div class="grid-2">
        <!-- Sidebar Controls -->
        <div>
            <div class="card">
                <div class="card-title">Case Selector</div>
                <label style="display:block; margin-bottom:8px; font-size:14px;">Select Transaction ID:</label>
                <select id="txSelect" style="width:100%; padding:10px; background:#0f172a; color:#fff; border:1px solid #334155; border-radius:6px;">
                    <option value="2987015">Tx 2987015 (High Risk - $207.24)</option>
                    <option value="2987016">Tx 2987016 (Medium Risk - $140.00)</option>
                    <option value="2987017">Tx 2987017 (Low Risk - $25.50)</option>
                </select>
                <button class="btn" style="width:100%; margin-top:16px;" onclick="loadCase()">Investigate Transaction</button>
            </div>

            <div class="card">
                <div class="card-title">Ask FinSight Q&A</div>
                <input type="text" id="askInput" placeholder="e.g. Why is this transaction high risk?" style="width:90%; padding:10px; background:#0f172a; color:#fff; border:1px solid #334155; border-radius:6px; margin-bottom:12px;">
                <button class="btn" style="width:100%;" onclick="askQuestion()">Submit Question</button>
            </div>
        </div>

        <!-- Main Workspace -->
        <div>
            <div class="card">
                <div class="card-title">Case Risk Overview</div>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-label">Risk Tier</div>
                        <div class="stat-val stat-high" id="riskTier">High Risk</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Calibrated Score</div>
                        <div class="stat-val" id="mlScore">0.8742</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Anomaly Score</div>
                        <div class="stat-val" id="anomScore">0.8250</div>
                    </div>
                </div>

                <div class="card-title">AI Evidence-Backed Assessment</div>
                <p id="caseOverview" style="line-height:1.6;">Loading case synthesis...</p>

                <div class="card-title">Risk Indicators</div>
                <div class="indicator-list" id="indicatorList"></div>
            </div>

            <div class="card">
                <div class="card-title">Policy Guidance & Citations</div>
                <p id="policyGuidance" style="line-height:1.6; color:#cbd5e1;"></p>
                <button class="btn" onclick="generateReport()">Generate Full Investigation Report</button>
            </div>

            <div class="card" id="reportCard" style="display:none;">
                <div class="card-title">Generated Formal Report</div>
                <pre id="reportOutput"></pre>
            </div>
        </div>
    </div>

    <script>
        function loadCase() {
            const txId = document.getElementById('txSelect').value;
            fetch('/api/v1/investigate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({transaction_id: parseInt(txId)})
            })
            .then(res => res.json())
            .then(data => {
                const inv = data.investigation;
                document.getElementById('riskTier').innerText = inv.risk_tier;
                document.getElementById('mlScore').innerText = inv.calibrated_score.toFixed(4);
                document.getElementById('caseOverview').innerText = inv.case_overview;
                document.getElementById('policyGuidance').innerText = inv.policy_guidance;

                const list = document.getElementById('indicatorList');
                list.innerHTML = '';
                inv.risk_indicators.forEach(ind => {
                    const item = document.createElement('div');
                    item.className = 'indicator-item';
                    item.innerHTML = ind;
                    list.appendChild(item);
                });
            })
            .catch(err => {
                console.log('Using offline demo view');
            });
        }

        function askQuestion() {
            const q = document.getElementById('askInput').value;
            if(!q) return;
            alert("Analyst Question Submitted: " + q);
        }

        function generateReport() {
            const txId = document.getElementById('txSelect').value;
            fetch('/api/v1/report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({transaction_id: parseInt(txId)})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('reportCard').style.display = 'block';
                document.getElementById('reportOutput').innerText = data.report.markdown_content;
            });
        }

        // Initial load
        loadCase();
    </script>
</body>
</html>
"""


def get_ui_html() -> str:
    """Return HTML string for Decision Support Workspace."""
    return HTML_WORKSPACE_TEMPLATE

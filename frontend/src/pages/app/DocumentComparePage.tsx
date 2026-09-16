import React, { useState } from 'react';
import { GitCompare, FileText, ArrowRight, ShieldAlert, CheckCircle2, RefreshCw } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { MOCK_LEGAL_DOCUMENTS } from '../../lib/api';

export const DocumentComparePage: React.FC = () => {
  const [docAId, setDocAId] = useState('DOC-2026-8812');
  const [docBId, setDocBId] = useState('DOC-2026-9041');

  const docA = MOCK_LEGAL_DOCUMENTS.find(d => d.id === docAId) || MOCK_LEGAL_DOCUMENTS[0];
  const docB = MOCK_LEGAL_DOCUMENTS.find(d => d.id === docBId) || MOCK_LEGAL_DOCUMENTS[1];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 font-sans">
      {/* Header */}
      <div className="space-y-2">
        <Badge variant="outline">Contract Diff & Redline</Badge>
        <h1 className="font-serif text-3xl font-light text-juris-textPrimary">Document Comparison Workspace</h1>
        <p className="text-sm text-juris-textMuted">
          Compare legal terms side-by-side to identify added obligations, modified liability caps, and material risk shifts.
        </p>
      </div>

      {/* Document Selector Top Bar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-4 border border-juris-border rounded-xl shadow-subtle">
        <div className="space-y-1">
          <label className="block text-xs font-semibold text-juris-textMuted uppercase">Document A (Baseline)</label>
          <select
            value={docAId}
            onChange={(e) => setDocAId(e.target.value)}
            className="w-full bg-juris-bgMuted border border-juris-border rounded p-2 text-xs font-medium text-juris-textPrimary focus:outline-none"
          >
            {MOCK_LEGAL_DOCUMENTS.map((d) => (
              <option key={d.id} value={d.id}>{d.title} ({d.id})</option>
            ))}
          </select>
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-semibold text-juris-textMuted uppercase">Document B (Target / Counter)</label>
          <select
            value={docBId}
            onChange={(e) => setDocBId(e.target.value)}
            className="w-full bg-juris-bgMuted border border-juris-border rounded p-2 text-xs font-medium text-juris-textPrimary focus:outline-none"
          >
            {MOCK_LEGAL_DOCUMENTS.map((d) => (
              <option key={d.id} value={d.id}>{d.title} ({d.id})</option>
            ))}
          </select>
        </div>
      </div>

      {/* JurisAI Material Diff Analysis Banner */}
      <div className="bg-white border border-juris-border rounded-xl p-6 space-y-3 shadow-subtle border-l-4 border-l-juris-riskMod">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-juris-textPrimary text-sm flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-juris-riskMod" /> JurisAI Material Change Delta
          </span>
          <Badge variant="mod">3 Material Term Differences Detected</Badge>
        </div>
        <p className="text-xs text-juris-textMuted leading-relaxed">
          Significant variance detected in <strong>Notice Period Requirements</strong> (180 days vs 30 days standard), <strong>Termination Fee Structure</strong> ($1.2M exposure vs No Penalty), and <strong>Work Product IP Carve-outs</strong>.
        </p>
      </div>

      {/* Side-by-Side Clause Redline */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Document A Pane */}
        <div className="bg-white border border-juris-border rounded-xl p-6 space-y-4 shadow-subtle">
          <div className="flex items-center justify-between border-b border-juris-border pb-3">
            <div>
              <p className="font-semibold text-sm text-juris-textPrimary">{docA.title}</p>
              <p className="text-xs text-juris-textSubtle">{docA.type} • Delaware Law</p>
            </div>
            <Badge variant="outline">Baseline</Badge>
          </div>

          <div className="space-y-4 text-xs font-serif leading-relaxed">
            <div className="p-3 bg-red-50 border-l-4 border-red-500 rounded text-juris-textBody">
              <span className="font-sans font-bold text-red-700 block mb-1">Section 4.2 — Termination Notice</span>
              "Tenant may terminate this Agreement prior to expiration only upon providing 180 days notice AND payment of Early Termination Fee equal to 12 months base rent."
            </div>

            <div className="p-3 bg-juris-bgMuted border-l-4 border-juris-border rounded text-juris-textBody">
              <span className="font-sans font-bold text-juris-textPrimary block mb-1">Section 9.1 — Indemnification</span>
              "Tenant agrees to defend, indemnify, and hold harmless Landlord regardless of comparative negligence."
            </div>
          </div>
        </div>

        {/* Right Document B Pane */}
        <div className="bg-white border border-juris-border rounded-xl p-6 space-y-4 shadow-subtle">
          <div className="flex items-center justify-between border-b border-juris-border pb-3">
            <div>
              <p className="font-semibold text-sm text-juris-textPrimary">{docB.title}</p>
              <p className="text-xs text-juris-textSubtle">{docB.type} • New York Law</p>
            </div>
            <Badge variant="outline">Counter Proposal</Badge>
          </div>

          <div className="space-y-4 text-xs font-serif leading-relaxed">
            <div className="p-3 bg-green-50 border-l-4 border-green-500 rounded text-juris-textBody">
              <span className="font-sans font-bold text-green-700 block mb-1">Section 6.3 — Work Product Ownership</span>
              "All custom models, algorithms, and code developed under any SOW shall be deemed works made for hire and belong solely to Client."
            </div>

            <div className="p-3 bg-juris-bgMuted border-l-4 border-juris-border rounded text-juris-textBody">
              <span className="font-sans font-bold text-juris-textPrimary block mb-1">Section 11.2 — Data Security</span>
              "Provider agrees to implement industry-standard encryption (TLS 1.3/AES-256). Provider shall not use Client Data for LLM training."
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

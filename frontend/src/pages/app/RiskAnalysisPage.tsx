import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShieldAlert, AlertTriangle, CheckCircle2, DollarSign, FileText, ArrowLeft, ExternalLink } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { jurisApi } from '../../lib/api';

export const RiskAnalysisPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const doc = jurisApi.getDocument(id || 'DOC-2026-8812') || jurisApi.getDocuments()[0];

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8 font-sans">
      {/* Top Bar Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-juris-border pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" icon={<ArrowLeft className="w-3.5 h-3.5" />} onClick={() => navigate('/app/documents')}>
              Back
            </Button>
            <Badge variant="outline">Contract Risk Audit</Badge>
          </div>
          <h1 className="font-serif text-3xl font-light text-juris-textPrimary">{doc.title}</h1>
          <p className="text-xs text-juris-textMuted">Document ID: {doc.id} • Governing Law: {doc.governingLaw}</p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={() => navigate(`/app/documents/${doc.id}`)}>
            View Document Text
          </Button>
          <Button variant="primary" size="sm" icon={<ExternalLink className="w-3.5 h-3.5" />} onClick={() => navigate(`/app/assistant?q=Draft renegotiation memo for ${doc.title}`)}>
            Draft Renegotiation Memo
          </Button>
        </div>
      </div>

      {/* Overall Risk Score Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="space-y-3 border-l-4 border-l-juris-riskHigh">
          <p className="text-xs font-semibold text-juris-textSubtle uppercase">Overall Risk Classification</p>
          <div className="flex items-center justify-between">
            <span className="font-serif text-2xl font-bold text-juris-textPrimary">High Risk</span>
            <Badge variant="high">Risk Score: 78/100</Badge>
          </div>
          <p className="text-xs text-juris-textMuted">
            Driven by severe early termination financial penalty ($1.2M) and non-reciprocal tenant indemnity.
          </p>
        </Card>

        <Card className="space-y-3">
          <p className="text-xs font-semibold text-juris-textSubtle uppercase">Quantified Financial Exposure</p>
          <div className="flex items-center justify-between">
            <span className="font-serif text-2xl font-bold text-juris-textPrimary">$1,200,000</span>
            <Badge variant="mod">Est. Penalty</Badge>
          </div>
          <p className="text-xs text-juris-textMuted">
            Early exit fee equal to 12 months base rent + 180 days advance written notice requirement.
          </p>
        </Card>

        <Card className="space-y-3">
          <p className="text-xs font-semibold text-juris-textSubtle uppercase">Audit Findings Summary</p>
          <div className="flex items-center justify-between">
            <span className="font-serif text-2xl font-bold text-juris-textPrimary">4 Flagged Provisions</span>
            <Badge variant="neutral">2 High • 2 Mod</Badge>
          </div>
          <p className="text-xs text-juris-textMuted">
            Includes asymmetric liability capping ($10k landlord cap) and auto-renewal notice lock-in.
          </p>
        </Card>
      </div>

      {/* High Risk Clauses Detailed Breakdown */}
      <div className="space-y-4">
        <h3 className="font-serif text-xl font-semibold text-juris-textPrimary">High Risk Provisions & Recommended Actions</h3>

        <div className="space-y-4">
          {doc.clauses.map((clause) => (
            <div
              key={clause.id}
              className="bg-white border border-juris-border rounded-xl p-6 space-y-4 shadow-subtle hover:border-juris-borderDark transition-all"
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-juris-border pb-3">
                <div className="flex items-center gap-2">
                  <ShieldAlert className={`w-4 h-4 ${clause.riskLevel === 'High' ? 'text-juris-riskHigh' : 'text-juris-riskMod'}`} />
                  <span className="font-semibold text-sm text-juris-textPrimary">{clause.sectionNumber} — {clause.title}</span>
                </div>
                <Badge variant={clause.riskLevel === 'High' ? 'high' : 'mod'} size="sm">
                  {clause.riskLevel} Risk Severity
                </Badge>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                <div className="space-y-2">
                  <p className="font-semibold text-juris-textMuted uppercase tracking-wider text-[11px]">Verbatim Contract Excerpt</p>
                  <div className="p-3 bg-juris-bgMuted border border-juris-border rounded font-serif text-juris-textBody leading-relaxed italic">
                    "{clause.text}"
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="font-semibold text-juris-textMuted uppercase tracking-wider text-[11px]">JurisAI Exposure Analysis</p>
                  <p className="text-juris-textMuted leading-relaxed">{clause.explanation}</p>

                  <div className="pt-2">
                    <p className="font-semibold text-juris-textPrimary mb-1">Actionable Counsel Recommendation:</p>
                    <div className="p-2.5 bg-juris-riskLowBg border border-juris-riskLowBorder rounded text-juris-riskLow font-medium">
                      {clause.recommendation}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Decision Support Guardrail Footer */}
      <div className="p-4 bg-juris-bgMuted border border-juris-border rounded-xl text-xs text-juris-textMuted flex items-center gap-3">
        <CheckCircle2 className="w-5 h-5 text-juris-textPrimary shrink-0" />
        <div>
          <p className="font-semibold text-juris-textPrimary">JurisAI Decision Support Architecture</p>
          <p className="text-[11px]">This risk evaluation is generated as analytical decision-support for corporate legal teams and does not constitute formal legal representation.</p>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  FileText, ShieldAlert, Sparkles, ZoomIn, ZoomOut, Search,
  Download, ArrowLeft, CheckCircle2, ChevronRight, AlertTriangle
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { jurisApi } from '../../lib/api';

export const DocumentViewerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const doc = jurisApi.getDocument(id || 'DOC-2026-8812') || jurisApi.getDocuments()[0];

  const [activeTab, setActiveTab] = useState<'overview' | 'clauses' | 'risk'>('overview');
  const [zoomLevel, setZoomLevel] = useState(100);
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col overflow-hidden bg-juris-bgSecondary font-sans">
      {/* Viewer Header */}
      <div className="h-14 bg-white border-b border-juris-border px-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" icon={<ArrowLeft className="w-4 h-4" />} onClick={() => navigate('/app/documents')}>
            Back
          </Button>
          <div className="h-4 w-[1px] bg-juris-border"></div>
          <FileText className="w-4 h-4 text-juris-textMuted" />
          <span className="font-semibold text-sm text-juris-textPrimary truncate">{doc.title}</span>
          <Badge variant={doc.riskLevel === 'High' ? 'high' : 'mod'} size="sm">
            {doc.riskLevel} Risk
          </Badge>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <div className="flex items-center gap-1 border border-juris-border rounded px-2 py-1 bg-juris-bgMuted">
            <button onClick={() => setZoomLevel(Math.max(80, zoomLevel - 10))} className="p-0.5 hover:text-juris-textPrimary">
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="text-[11px] font-mono text-juris-textSubtle">{zoomLevel}%</span>
            <button onClick={() => setZoomLevel(Math.min(140, zoomLevel + 10))} className="p-0.5 hover:text-juris-textPrimary">
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
          </div>

          <Button variant="outline" size="sm" icon={<Download className="w-3.5 h-3.5" />}>
            Export Brief
          </Button>
          <Button variant="primary" size="sm" icon={<ShieldAlert className="w-3.5 h-3.5" />} onClick={() => navigate(`/app/analysis/${doc.id}`)}>
            Risk Report
          </Button>
        </div>
      </div>

      {/* Main Split-Pane Workspace */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-12 min-h-0 overflow-hidden">
        {/* LEFT PANE: Document Viewer (7 cols) */}
        <div className="md:col-span-7 bg-white border-r border-juris-border flex flex-col min-h-0">
          {/* Internal Doc Toolbar */}
          <div className="h-10 px-4 bg-juris-bgMuted border-b border-juris-border flex items-center justify-between text-xs text-juris-textSubtle">
            <div className="flex items-center gap-2">
              <span>Signatories: <strong className="text-juris-textBody">{doc.signatories.join(', ')}</strong></span>
            </div>
            <span>Governing Law: <strong className="text-juris-textBody">{doc.governingLaw}</strong></span>
          </div>

          {/* Document Content Canvas */}
          <div className="flex-1 overflow-y-auto p-8 space-y-6 font-serif text-sm text-juris-textBody leading-relaxed bg-white">
            <div style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top left' }} className="space-y-6 transition-transform">
              <div className="border-b border-juris-border pb-4">
                <h1 className="font-serif text-2xl font-bold text-juris-textPrimary uppercase tracking-wide">{doc.title}</h1>
                <p className="text-xs font-sans text-juris-textSubtle mt-1">Document ID: {doc.id} • Page 1 of {doc.pageCount}</p>
              </div>

              <div className="prose prose-sm max-w-none space-y-4">
                <div className="p-4 bg-juris-bgMuted border border-juris-border rounded font-sans text-xs text-juris-textMuted leading-normal">
                  <strong className="text-juris-textPrimary block mb-1 font-serif text-sm">Executive Summary</strong>
                  {doc.summary}
                </div>

                <div className="space-y-3 font-serif">
                  <h3 className="font-bold text-base text-juris-textPrimary border-b border-juris-border pb-1">CLAUSE EXTRACTS & HIGHLIGHTED PROVISIONS</h3>

                  {doc.clauses.map((clause) => (
                    <div
                      key={clause.id}
                      className={`p-4 rounded border transition-all ${
                        clause.riskLevel === 'High'
                          ? 'clause-highlight-high border-juris-riskHighBorder'
                          : clause.riskLevel === 'Moderate'
                          ? 'clause-highlight-mod border-juris-riskModBorder'
                          : 'clause-highlight-low border-juris-riskLowBorder'
                      }`}
                    >
                      <div className="flex items-center justify-between font-sans text-xs mb-1.5">
                        <span className="font-bold text-juris-textPrimary">{clause.sectionNumber} — {clause.title}</span>
                        <Badge variant={clause.riskLevel === 'High' ? 'high' : 'mod'} size="sm">
                          {clause.riskLevel} Risk
                        </Badge>
                      </div>
                      <p className="font-serif text-xs text-juris-textBody leading-relaxed">
                        "{clause.text}"
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT PANE: JurisAI Intelligence Panel (5 cols) */}
        <div className="md:col-span-5 bg-juris-bgSecondary flex flex-col min-h-0 overflow-y-auto p-6 space-y-6 font-sans text-xs">
          {/* Tab Navigation */}
          <div className="flex items-center gap-1 bg-white p-1 border border-juris-border rounded-lg shrink-0">
            <button
              onClick={() => setActiveTab('overview')}
              className={`flex-1 py-1.5 rounded text-xs font-medium transition-colors ${
                activeTab === 'overview' ? 'bg-juris-textPrimary text-white' : 'text-juris-textMuted hover:text-juris-textPrimary'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('clauses')}
              className={`flex-1 py-1.5 rounded text-xs font-medium transition-colors ${
                activeTab === 'clauses' ? 'bg-juris-textPrimary text-white' : 'text-juris-textMuted hover:text-juris-textPrimary'
              }`}
            >
              Clauses ({doc.clauses.length})
            </button>
            <button
              onClick={() => setActiveTab('risk')}
              className={`flex-1 py-1.5 rounded text-xs font-medium transition-colors ${
                activeTab === 'risk' ? 'bg-juris-textPrimary text-white' : 'text-juris-textMuted hover:text-juris-textPrimary'
              }`}
            >
              Risk Summary
            </button>
          </div>

          {/* Tab Content */}
          {activeTab === 'overview' && (
            <div className="space-y-4">
              <div className="bg-white border border-juris-border rounded-xl p-5 space-y-3 shadow-subtle">
                <div className="flex items-center justify-between border-b border-juris-border pb-3">
                  <span className="font-semibold text-juris-textPrimary text-sm flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-juris-textPrimary" /> JurisAI Executive Brief
                  </span>
                  <Badge variant="outline">Verified</Badge>
                </div>
                <p className="text-juris-textMuted leading-relaxed">{doc.summary}</p>
                <div className="pt-2 flex items-center justify-between text-[11px] text-juris-textSubtle">
                  <span>Signatories: {doc.signatories.length} Parties</span>
                  <span>Jurisdiction: {doc.governingLaw}</span>
                </div>
              </div>

              <div className="bg-white border border-juris-border rounded-xl p-5 space-y-3 shadow-subtle">
                <h4 className="font-semibold text-juris-textPrimary text-sm">Key Legal Obligations</h4>
                <ul className="space-y-2 text-juris-textBody">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-juris-riskLow shrink-0 mt-0.5" />
                    <span><strong>180-Day Termination Window:</strong> Early exit requires 6 months prior written notice.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-juris-riskLow shrink-0 mt-0.5" />
                    <span><strong>8% Annual Rent Escalation:</strong> Mandatory compound increase during renewal periods.</span>
                  </li>
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'clauses' && (
            <div className="space-y-3">
              {doc.clauses.map((clause) => (
                <div key={clause.id} className="bg-white border border-juris-border rounded-xl p-4 space-y-2 shadow-subtle">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-juris-textPrimary">{clause.sectionNumber} — {clause.title}</span>
                    <Badge variant={clause.riskLevel === 'High' ? 'high' : 'mod'} size="sm">
                      {clause.riskLevel}
                    </Badge>
                  </div>
                  <p className="text-juris-textMuted leading-relaxed">{clause.explanation}</p>
                  {clause.financialImpact && (
                    <div className="p-2 bg-juris-riskHighBg border border-juris-riskHighBorder rounded text-[11px] text-juris-riskHigh font-medium">
                      Financial Exposure: {clause.financialImpact}
                    </div>
                  )}
                  <div className="pt-2 border-t border-juris-border flex items-center justify-between">
                    <span className="text-[11px] text-juris-textSubtle">Recommendation</span>
                    <Button variant="ghost" size="sm" onClick={() => navigate(`/app/assistant?q=Explain ${clause.sectionNumber}`)}>
                      Ask JurisAI
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'risk' && (
            <div className="space-y-4">
              <div className="bg-white border border-juris-border rounded-xl p-5 space-y-3 shadow-subtle">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-juris-textPrimary text-sm">Overall Document Risk</span>
                  <Badge variant="high" size="sm">High Exposure</Badge>
                </div>
                <div className="w-full bg-juris-bgMuted h-2 rounded-full overflow-hidden">
                  <div className="bg-juris-riskHigh h-full w-[78%]"></div>
                </div>
                <p className="text-juris-textMuted text-xs">
                  Risk score calculated from 2 High risk clauses (termination fee & broad indemnity) and asymmetric liability capping.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

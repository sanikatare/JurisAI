import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles, Search, FileText, ShieldAlert, GitCompare, ArrowRight,
  Plus, CheckCircle2, ChevronRight, Eye, ShieldCheck, HelpCircle, FileCheck
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { MOCK_LEGAL_DOCUMENTS } from '../../lib/api';

export const DashboardPage: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const navigate = useNavigate();

  const handleAskSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    navigate(`/app/assistant?q=${encodeURIComponent(prompt)}`);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-10 font-sans">
      {/* Header Greeting */}
      <div className="space-y-6 max-w-4xl">
        <div className="space-y-1">
          <Badge variant="outline">Enterprise Legal Intelligence Workspace</Badge>
          <h1 className="font-serif text-3xl md:text-4xl font-light text-juris-textPrimary mt-1">
            Good morning, Counselor.
          </h1>
          <p className="text-sm text-juris-textMuted">Your legal workspace activity overview and document risk summary.</p>
        </div>

        {/* Search / AI Query Box */}
        <form onSubmit={handleAskSubmit} className="relative">
          <div className="bg-white border border-juris-border rounded-xl p-2.5 shadow-subtle hover:border-juris-borderDark transition-all flex items-center gap-3">
            <div className="p-2.5 bg-juris-bgMuted rounded-lg text-juris-textPrimary shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask JurisAI anything about your legal agreements, obligations, or risks..."
              className="w-full text-base bg-transparent text-juris-textPrimary placeholder:text-juris-textSubtle focus:outline-none"
            />
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!prompt.trim()}
              icon={<ArrowRight className="w-4 h-4" />}
            >
              Ask JurisAI
            </Button>
          </div>
        </form>
      </div>

      {/* KPI Editorial Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card className="space-y-3 border-l-2 border-l-juris-textPrimary">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-juris-textSubtle uppercase tracking-wider">Documents Analyzed</span>
            <FileText className="w-4 h-4 text-juris-textMuted" />
          </div>
          <div className="flex items-baseline justify-between">
            <span className="font-serif text-3xl font-bold text-juris-textPrimary">24</span>
            <span className="text-[11px] text-juris-riskLow font-medium">+3 this week</span>
          </div>
          <p className="text-[11px] text-juris-textMuted">Commercial leases, MSAs & M&A drafts</p>
        </Card>

        <Card className="space-y-3 border-l-2 border-l-juris-riskHigh">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-juris-textSubtle uppercase tracking-wider">High-Risk Clauses</span>
            <ShieldAlert className="w-4 h-4 text-juris-riskHigh" />
          </div>
          <div className="flex items-baseline justify-between">
            <span className="font-serif text-3xl font-bold text-juris-textPrimary">7</span>
            <Badge variant="high" size="sm">Requires Action</Badge>
          </div>
          <p className="text-[11px] text-juris-textMuted">Early termination & broad indemnities</p>
        </Card>

        <Card className="space-y-3 border-l-2 border-l-juris-textMuted">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-juris-textSubtle uppercase tracking-wider">Documents Reviewed</span>
            <FileCheck className="w-4 h-4 text-juris-textMuted" />
          </div>
          <div className="flex items-baseline justify-between">
            <span className="font-serif text-3xl font-bold text-juris-textPrimary">18</span>
            <span className="text-[11px] text-juris-textSubtle font-medium">75% Audited</span>
          </div>
          <p className="text-[11px] text-juris-textMuted">Signed off by counsel</p>
        </Card>

        <Card className="space-y-3 border-l-2 border-l-juris-riskMod">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-juris-textSubtle uppercase tracking-wider">Open Questions</span>
            <HelpCircle className="w-4 h-4 text-juris-riskMod" />
          </div>
          <div className="flex items-baseline justify-between">
            <span className="font-serif text-3xl font-bold text-juris-textPrimary">12</span>
            <Badge variant="mod" size="sm">Pending RAG</Badge>
          </div>
          <p className="text-[11px] text-juris-textMuted">Clause explanations & precedent checks</p>
        </Card>
      </div>

      {/* Recent Legal Documents Table */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-serif text-xl font-semibold text-juris-textPrimary">Recent Legal Documents</h3>
            <p className="text-xs text-juris-textMuted">Document vault analysis status and risk highlights</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => navigate('/app/documents')}>
            View Vault ({MOCK_LEGAL_DOCUMENTS.length})
          </Button>
        </div>

        <div className="bg-white border border-juris-border rounded-xl shadow-subtle overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-juris-bgMuted border-b border-juris-border font-medium text-juris-textSubtle uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4">Document Title</th>
                  <th className="py-3.5 px-4">Type</th>
                  <th className="py-3.5 px-4">Risk Status</th>
                  <th className="py-3.5 px-4">Governing Law</th>
                  <th className="py-3.5 px-4">Last Modified</th>
                  <th className="py-3.5 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-juris-border text-juris-textBody">
                {MOCK_LEGAL_DOCUMENTS.map((doc) => (
                  <tr key={doc.id} className="hover:bg-juris-bgSecondary transition-colors group">
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-3">
                        <FileText className="w-4 h-4 text-juris-textMuted shrink-0" />
                        <div>
                          <p className="font-medium text-juris-textPrimary group-hover:text-black">{doc.title}</p>
                          <p className="text-[11px] text-juris-textSubtle">{doc.id} • {doc.pageCount} pages</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 font-medium text-juris-textMuted">{doc.category}</td>
                    <td className="py-3.5 px-4">
                      <Badge
                        variant={doc.riskLevel === 'High' ? 'high' : doc.riskLevel === 'Moderate' ? 'mod' : 'low'}
                        size="sm"
                      >
                        {doc.riskLevel} Risk
                      </Badge>
                    </td>
                    <td className="py-3.5 px-4 text-juris-textMuted">{doc.governingLaw}</td>
                    <td className="py-3.5 px-4 text-juris-textSubtle">{doc.lastModified}</td>
                    <td className="py-3.5 px-4 text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        icon={<Eye className="w-3.5 h-3.5" />}
                        onClick={() => navigate(`/app/documents/${doc.id}`)}
                      >
                        Open
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles, Search, FileText, ShieldAlert, GitCompare, ArrowRight,
  Upload, Clock, Filter, Eye, ChevronRight
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { MOCK_LEGAL_DOCUMENTS, jurisApi } from '../../lib/api';

export const WorkspaceHome: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleAskSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    navigate(`/app/assistant?q=${encodeURIComponent(prompt)}`);
  };

  const handleSuggestedPrompt = (text: string) => {
    navigate(`/app/assistant?q=${encodeURIComponent(text)}`);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-10 font-sans">
      {/* Header Greeting & Prompt */}
      <div className="space-y-6 max-w-4xl">
        <div className="space-y-1">
          <p className="text-xs font-medium text-juris-textMuted uppercase tracking-wider">Apex Holdings Legal Workspace</p>
          <h1 className="font-serif text-3xl md:text-4xl font-light text-juris-textPrimary">
            Good morning, Counselor.
          </h1>
          <p className="text-sm text-juris-textMuted">What would you like to work on today?</p>
        </div>

        {/* Large AI Prompt Box */}
        <form onSubmit={handleAskSubmit} className="relative">
          <div className="bg-white border border-juris-border rounded-xl p-2.5 shadow-subtle hover:border-juris-borderDark transition-all flex items-center gap-3">
            <div className="p-2.5 bg-juris-bgMuted rounded-lg text-juris-textPrimary shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask JurisAI anything about your legal documents, clauses, or risks..."
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

        {/* Suggested Quick Prompts */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="text-juris-textSubtle font-medium mr-1">Suggested:</span>
          {[
            'Identify unusual termination obligations in recent lease',
            'Summarize liability caps across master agreements',
            'Which agreements auto-renew in the next 90 days?'
          ].map((sp, idx) => (
            <button
              key={idx}
              onClick={() => handleSuggestedPrompt(sp)}
              className="px-3 py-1.5 bg-white border border-juris-border rounded-full text-juris-textBody hover:border-juris-textPrimary hover:shadow-subtle transition-all"
            >
              "{sp}"
            </button>
          ))}
        </div>
      </div>

      {/* Primary Action Modules Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card hover padding="sm" className="flex flex-col justify-between space-y-4" onClick={() => navigate('/app/documents')}>
          <div className="flex items-center justify-between">
            <div className="p-2 rounded bg-juris-bgMuted text-juris-textPrimary">
              <FileText className="w-4 h-4" />
            </div>
            <ChevronRight className="w-4 h-4 text-juris-textSubtle" />
          </div>
          <div>
            <h4 className="font-serif text-base font-semibold text-juris-textPrimary">Analyze Document</h4>
            <p className="text-xs text-juris-textMuted mt-0.5">Parse clauses & legal obligations</p>
          </div>
        </Card>

        <Card hover padding="sm" className="flex flex-col justify-between space-y-4" onClick={() => navigate('/app/analysis/DOC-2026-8812')}>
          <div className="flex items-center justify-between">
            <div className="p-2 rounded bg-juris-bgMuted text-juris-textPrimary">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <ChevronRight className="w-4 h-4 text-juris-textSubtle" />
          </div>
          <div>
            <h4 className="font-serif text-base font-semibold text-juris-textPrimary">Review Contract Risks</h4>
            <p className="text-xs text-juris-textMuted mt-0.5">Audit financial exposure & penalties</p>
          </div>
        </Card>

        <Card hover padding="sm" className="flex flex-col justify-between space-y-4" onClick={() => navigate('/app/compare')}>
          <div className="flex items-center justify-between">
            <div className="p-2 rounded bg-juris-bgMuted text-juris-textPrimary">
              <GitCompare className="w-4 h-4" />
            </div>
            <ChevronRight className="w-4 h-4 text-juris-textSubtle" />
          </div>
          <div>
            <h4 className="font-serif text-base font-semibold text-juris-textPrimary">Compare Agreements</h4>
            <p className="text-xs text-juris-textMuted mt-0.5">Side-by-side material diff</p>
          </div>
        </Card>

        <Card hover padding="sm" className="flex flex-col justify-between space-y-4" onClick={() => navigate('/app/ask')}>
          <div className="flex items-center justify-between">
            <div className="p-2 rounded bg-juris-bgMuted text-juris-textPrimary">
              <Search className="w-4 h-4" />
            </div>
            <ChevronRight className="w-4 h-4 text-juris-textSubtle" />
          </div>
          <div>
            <h4 className="font-serif text-base font-semibold text-juris-textPrimary">Ask My Docs (RAG)</h4>
            <p className="text-xs text-juris-textMuted mt-0.5">Search across connected repository</p>
          </div>
        </Card>
      </div>

      {/* Recent Documents Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-serif text-xl font-semibold text-juris-textPrimary">Recent Legal Documents</h3>
            <p className="text-xs text-juris-textMuted">Document vault analysis status and risk highlights</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => navigate('/app/documents')}>
            View All Documents ({MOCK_LEGAL_DOCUMENTS.length})
          </Button>
        </div>

        <div className="bg-white border border-juris-border rounded-xl shadow-subtle overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-juris-bgMuted border-b border-juris-border font-medium text-juris-textSubtle uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">Document Title</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Risk Status</th>
                  <th className="py-3 px-4">Governing Law</th>
                  <th className="py-3 px-4">Last Modified</th>
                  <th className="py-3 px-4 text-right">Action</th>
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

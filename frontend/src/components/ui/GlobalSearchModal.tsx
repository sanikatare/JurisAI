import React, { useState, useEffect } from 'react';
import { Search, FileText, Bot, AlertTriangle, ShieldCheck, ArrowRight, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { MOCK_LEGAL_DOCUMENTS, MOCK_AGENTS } from '../../lib/api';

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          setQuery('');
          // Parent handles opening if triggered globally
        }
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filteredDocs = MOCK_LEGAL_DOCUMENTS.filter(
    d => d.title.toLowerCase().includes(query.toLowerCase()) || d.summary.toLowerCase().includes(query.toLowerCase())
  );

  const filteredAgents = MOCK_AGENTS.filter(
    a => a.name.toLowerCase().includes(query.toLowerCase()) || a.description.toLowerCase().includes(query.toLowerCase())
  );

  const handleSelectDoc = (id: string) => {
    onClose();
    navigate(`/app/documents/${id}`);
  };

  const handleSelectAgent = () => {
    onClose();
    navigate('/app/agents');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/40 backdrop-blur-sm transition-opacity">
      <div className="w-full max-w-2xl bg-white border border-juris-border rounded-xl shadow-dropdown overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-150">
        {/* Header / Input */}
        <div className="flex items-center px-4 py-3.5 border-b border-juris-border gap-3">
          <Search className="w-5 h-5 text-juris-textSubtle shrink-0" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search legal documents, clauses, agents, or RAG policies... (⌘K)"
            className="w-full text-base bg-transparent text-juris-textPrimary placeholder:text-juris-textSubtle focus:outline-none"
          />
          <button
            onClick={onClose}
            className="p-1 text-juris-textSubtle hover:text-juris-textPrimary rounded-md hover:bg-juris-bgMuted"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-[380px] overflow-y-auto p-2 space-y-4">
          {/* Quick Shortcuts */}
          {!query && (
            <div className="px-2 py-1">
              <p className="text-[11px] font-medium text-juris-textSubtle uppercase tracking-wider mb-2">Quick Navigation</p>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <button
                  onClick={() => { onClose(); navigate('/app/documents'); }}
                  className="flex items-center gap-2 p-2 rounded-md hover:bg-juris-bgMuted text-juris-textBody text-left border border-juris-border/60"
                >
                  <FileText className="w-4 h-4 text-juris-textSubtle" /> Document Vault
                </button>
                <button
                  onClick={() => { onClose(); navigate('/app/ask'); }}
                  className="flex items-center gap-2 p-2 rounded-md hover:bg-juris-bgMuted text-juris-textBody text-left border border-juris-border/60"
                >
                  <ShieldCheck className="w-4 h-4 text-juris-textSubtle" /> Ask My Docs (RAG)
                </button>
              </div>
            </div>
          )}

          {/* Document Matches */}
          {filteredDocs.length > 0 && (
            <div>
              <p className="px-2 text-[11px] font-medium text-juris-textSubtle uppercase tracking-wider mb-1.5">Documents</p>
              <div className="space-y-1">
                {filteredDocs.map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => handleSelectDoc(doc.id)}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-juris-bgMuted cursor-pointer transition-colors group"
                  >
                    <div className="flex items-start gap-3">
                      <FileText className="w-4 h-4 text-juris-textMuted mt-0.5 shrink-0" />
                      <div>
                        <p className="text-sm font-medium text-juris-textPrimary group-hover:text-black">{doc.title}</p>
                        <p className="text-xs text-juris-textMuted line-clamp-1">{doc.summary}</p>
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-juris-textSubtle opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agent Matches */}
          {filteredAgents.length > 0 && (
            <div>
              <p className="px-2 text-[11px] font-medium text-juris-textSubtle uppercase tracking-wider mb-1.5">JurisAI Agents</p>
              <div className="space-y-1">
                {filteredAgents.map((agent) => (
                  <div
                    key={agent.id}
                    onClick={handleSelectAgent}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-juris-bgMuted cursor-pointer transition-colors group"
                  >
                    <div className="flex items-start gap-3">
                      <Bot className="w-4 h-4 text-juris-textMuted mt-0.5 shrink-0" />
                      <div>
                        <p className="text-sm font-medium text-juris-textPrimary">{agent.name}</p>
                        <p className="text-xs text-juris-textMuted">{agent.description}</p>
                      </div>
                    </div>
                    <span className="text-[11px] text-juris-textSubtle border border-juris-border px-2 py-0.5 rounded">Run Agent</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {filteredDocs.length === 0 && filteredAgents.length === 0 && query && (
            <div className="p-8 text-center text-juris-textMuted text-sm">
              No legal documents or agents matched "<span className="font-medium text-juris-textPrimary">{query}</span>".
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 bg-juris-bgMuted border-t border-juris-border flex items-center justify-between text-[11px] text-juris-textSubtle">
          <span>Tip: Press <kbd className="px-1.5 py-0.5 bg-white border border-juris-border rounded font-mono">ESC</kbd> to exit</span>
          <span>JurisAI Intelligence Workspace</span>
        </div>
      </div>
    </div>
  );
};

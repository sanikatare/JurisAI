import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Sparkles, Send, FileText, ExternalLink, ShieldCheck, ChevronRight,
  Clock, Plus, MessageSquare, AlertCircle, Copy, Check
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { jurisApi, RAGSearchResult } from '../../lib/api';

interface Message {
  id: string;
  sender: 'user' | 'juris';
  text: string;
  sources?: RAGSearchResult[];
  timestamp: string;
}

export const AssistantPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedSource, setSelectedSource] = useState<RAGSearchResult | null>(null);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'm-1',
      sender: 'juris',
      text: `Good morning. I am your **JurisAI Legal Intelligence Assistant**. I can help you analyze contracts, locate risk clauses, evaluate financial exposure, and answer questions across your connected legal documents.

How can I assist your legal team today?`,
      timestamp: '9:00 AM'
    }
  ]);

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  const handleSend = async (queryText: string = input) => {
    if (!queryText.trim() || loading) return;

    const userMsg: Message = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await jurisApi.askJurisAI(queryText);
      const ragSources = await jurisApi.searchRag(queryText, 3);

      const aiMsg: Message = {
        id: `j-${Date.now()}`,
        sender: 'juris',
        text: res.answer || 'Analysis complete based on connected legal documents.',
        sources: ragSources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, aiMsg]);
      if (ragSources.length > 0) {
        setSelectedSource(ragSources[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 1500);
  };

  return (
    <div className="h-[calc(100vh-4rem)] flex overflow-hidden bg-juris-bgSecondary font-sans">
      {/* LEFT COLUMN: Conversation Threads */}
      <div className="w-64 bg-white border-r border-juris-border flex flex-col shrink-0 hidden md:flex">
        <div className="p-3 border-b border-juris-border flex items-center justify-between">
          <span className="text-xs font-semibold text-juris-textPrimary">Conversations</span>
          <Button variant="ghost" size="sm" icon={<Plus className="w-3.5 h-3.5" />} onClick={() => setMessages([messages[0]])}>
            New Thread
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1 text-xs">
          <div className="p-2.5 bg-juris-bgMuted border border-juris-border rounded-lg text-juris-textPrimary font-medium flex items-center gap-2">
            <MessageSquare className="w-3.5 h-3.5 text-juris-textMuted shrink-0" />
            <span className="truncate">Current Session</span>
          </div>
          <div className="p-2.5 hover:bg-juris-bgMuted rounded-lg text-juris-textMuted cursor-pointer transition-colors truncate">
            Termination Notice & Penalty Review
          </div>
          <div className="p-2.5 hover:bg-juris-bgMuted rounded-lg text-juris-textMuted cursor-pointer transition-colors truncate">
            Indemnification Exemption Audit
          </div>
        </div>
      </div>

      {/* CENTER COLUMN: Main Chat Canvas */}
      <div className="flex-1 flex flex-col min-w-0 bg-white border-r border-juris-border">
        {/* Thread Header */}
        <div className="h-12 px-6 border-b border-juris-border flex items-center justify-between text-xs bg-white shrink-0">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-juris-textPrimary" />
            <span className="font-semibold text-juris-textPrimary">JurisAI Legal Copilot</span>
            <Badge variant="outline" size="sm">Evidence Grounded</Badge>
          </div>
          <span className="text-juris-textSubtle text-[11px]">Powered by RAG & Decision Support</span>
        </div>

        {/* Chat Message List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div className="flex items-center gap-2 mb-1 text-[11px] text-juris-textSubtle">
                <span className="font-medium">{msg.sender === 'user' ? 'Counsel' : 'JurisAI Intelligence'}</span>
                <span>• {msg.timestamp}</span>
              </div>

              <div
                className={`max-w-2xl p-4 rounded-xl text-xs leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-juris-card text-white border border-juris-surfaceBorder'
                    : 'bg-juris-bgMuted text-juris-textPrimary border border-juris-border'
                }`}
              >
                <div className="prose prose-xs max-w-none space-y-2 whitespace-pre-wrap">
                  {msg.text}
                </div>

                {/* Evidence & Citation Chips for AI Messages */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-juris-border space-y-2">
                    <p className="text-[11px] font-semibold text-juris-textMuted uppercase tracking-wider flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-juris-riskLow" /> Verified Citations ({msg.sources.length})
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {msg.sources.map((src) => (
                        <button
                          key={src.citationId}
                          onClick={() => setSelectedSource(src)}
                          className="flex items-center gap-1.5 px-2.5 py-1 bg-white border border-juris-border rounded hover:border-juris-textPrimary text-[11px] text-juris-textBody transition-all"
                        >
                          <FileText className="w-3 h-3 text-juris-textMuted" />
                          <span className="font-medium">{src.citationId}</span>
                          <span className="text-juris-textSubtle truncate max-w-[120px]">({src.section})</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {msg.sender === 'juris' && (
                <div className="flex items-center gap-3 mt-1.5 text-[11px] text-juris-textSubtle">
                  <button
                    onClick={() => handleCopy(msg.id, msg.text)}
                    className="flex items-center gap-1 hover:text-juris-textPrimary"
                  >
                    {copiedId === msg.id ? <Check className="w-3 h-3 text-juris-riskLow" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedId === msg.id ? 'Copied' : 'Copy Response'}</span>
                  </button>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-3 p-4 bg-juris-bgMuted border border-juris-border rounded-xl text-xs text-juris-textMuted">
              <Sparkles className="w-4 h-4 animate-spin text-juris-textPrimary" />
              <span>JurisAI is analyzing document clauses and performing vector retrieval...</span>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-juris-border bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2 bg-juris-bgMuted border border-juris-border rounded-xl p-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask JurisAI about your legal documents..."
              className="flex-1 bg-transparent px-2 text-xs text-juris-textPrimary placeholder:text-juris-textSubtle focus:outline-none"
            />
            <Button
              type="submit"
              variant="primary"
              size="sm"
              disabled={!input.trim() || loading}
              icon={<Send className="w-3.5 h-3.5" />}
            >
              Send
            </Button>
          </form>
          <div className="mt-2 text-[10px] text-juris-textSubtle flex items-center justify-between px-1">
            <span>JurisAI outputs are decision-support insights and do not constitute formal legal advice.</span>
            <span>Keyboard shortcut: ↵ Enter</span>
          </div>
        </div>
      </div>

      {/* RIGHT COLUMN: Interactive Evidence & Document Context Panel */}
      <div className="w-80 bg-juris-bgSecondary border-l border-juris-border flex flex-col shrink-0 hidden lg:flex">
        <div className="h-12 px-4 border-b border-juris-border flex items-center justify-between text-xs font-semibold text-juris-textPrimary bg-white">
          <span>Evidence & Citation Panel</span>
          <Badge variant="neutral" size="sm">Inspect</Badge>
        </div>

        <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
          {selectedSource ? (
            <div className="bg-white border border-juris-border rounded-xl p-4 space-y-3 shadow-subtle">
              <div className="flex items-center justify-between border-b border-juris-border pb-2">
                <span className="font-semibold text-juris-textPrimary">{selectedSource.citationId}</span>
                <Badge variant="low" size="sm">{(selectedSource.confidence * 100).toFixed(0)}% Match</Badge>
              </div>

              <div>
                <p className="text-[11px] font-medium text-juris-textSubtle uppercase">Document Title</p>
                <p className="font-medium text-juris-textPrimary mt-0.5">{selectedSource.documentTitle}</p>
              </div>

              <div>
                <p className="text-[11px] font-medium text-juris-textSubtle uppercase">Clause Section</p>
                <p className="font-medium text-juris-textPrimary mt-0.5">{selectedSource.section}</p>
              </div>

              <div>
                <p className="text-[11px] font-medium text-juris-textSubtle uppercase mb-1">Verbatim Excerpt</p>
                <div className="p-3 bg-juris-bgMuted border border-juris-border rounded text-juris-textBody font-serif leading-relaxed italic">
                  "{selectedSource.excerpt}"
                </div>
              </div>

              <Button
                variant="outline"
                size="sm"
                className="w-full justify-center"
                icon={<ExternalLink className="w-3.5 h-3.5" />}
                onClick={() => window.open(`/app/documents/${selectedSource.documentId}`, '_blank')}
              >
                Open Full Document
              </Button>
            </div>
          ) : (
            <div className="p-6 text-center text-juris-textSubtle space-y-2 border border-dashed border-juris-border rounded-xl">
              <FileText className="w-8 h-8 mx-auto text-juris-textSubtle opacity-50" />
              <p className="font-medium">No Citation Selected</p>
              <p className="text-[11px]">Click any citation chip in the conversation to inspect verbatim excerpt & confidence score.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

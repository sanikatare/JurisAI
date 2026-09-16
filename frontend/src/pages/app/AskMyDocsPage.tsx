import React, { useState } from 'react';
import { Search, FileText, Filter, Sparkles, ExternalLink, ShieldCheck, ArrowRight } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { jurisApi, RAGSearchResult } from '../../lib/api';
import { useNavigate } from 'react-router-dom';

export const AskMyDocsPage: React.FC = () => {
  const [query, setQuery] = useState('termination penalties and notice periods');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<RAGSearchResult[]>([]);
  const navigate = useNavigate();

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await jurisApi.searchRag(query, 5);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    handleSearch();
  }, []);

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8 font-sans">
      {/* Heading */}
      <div className="space-y-2">
        <Badge variant="outline">Flagship RAG Search</Badge>
        <h1 className="font-serif text-3xl font-light text-juris-textPrimary">Ask My Docs</h1>
        <p className="text-sm text-juris-textMuted">
          Perform cross-repository semantic and lexical search across all connected legal agreements.
        </p>
      </div>

      {/* RAG Search Form */}
      <form onSubmit={handleSearch} className="bg-white border border-juris-border rounded-xl p-3 shadow-subtle flex flex-col md:flex-row items-center gap-3">
        <div className="flex-1 flex items-center gap-3 px-2 w-full">
          <Search className="w-5 h-5 text-juris-textSubtle shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask questions across your legal documents (e.g. Which agreements auto-renew?)..."
            className="w-full text-base bg-transparent text-juris-textPrimary placeholder:text-juris-textSubtle focus:outline-none"
          />
        </div>
        <Button type="submit" variant="primary" size="md" disabled={loading} icon={<Sparkles className="w-4 h-4" />}>
          Search Repository
        </Button>
      </form>

      {/* Suggested RAG Queries */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-juris-textSubtle font-medium">Quick Queries:</span>
        {[
          'Which agreements contain automatic renewal clauses?',
          'What are our maximum liability caps across contracts?',
          'Show all Delaware governing law leases',
          'Data encryption and SOC2 security commitments'
        ].map((q, idx) => (
          <button
            key={idx}
            onClick={() => { setQuery(q); handleSearch(); }}
            className="px-3 py-1 bg-white border border-juris-border rounded-full text-juris-textBody hover:border-juris-textPrimary transition-colors"
          >
            "{q}"
          </button>
        ))}
      </div>

      {/* Results Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-juris-border pb-3">
          <p className="text-xs font-semibold text-juris-textMuted uppercase tracking-wider">
            Verified RAG Excerpts ({results.length})
          </p>
          <span className="text-xs text-juris-textSubtle">Reciprocal Rank Fusion (RRF) Ranking</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-juris-textMuted text-xs space-y-3">
            <Sparkles className="w-6 h-6 animate-spin mx-auto text-juris-textPrimary" />
            <p>Scanning vector embeddings and dense passage indices...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {results.map((res) => (
              <Card key={res.citationId} hover className="space-y-3">
                <div className="flex items-center justify-between border-b border-juris-border pb-2.5 text-xs">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-juris-textMuted" />
                    <span className="font-semibold text-juris-textPrimary">{res.documentTitle}</span>
                    <span className="text-juris-textSubtle">• {res.section}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="low" size="sm">{(res.confidence * 100).toFixed(0)}% Confidence</Badge>
                    <Badge variant="outline" size="sm">{res.citationId}</Badge>
                  </div>
                </div>

                <div className="p-3 bg-juris-bgMuted border border-juris-border rounded font-serif text-xs text-juris-textBody leading-relaxed">
                  "{res.excerpt}"
                </div>

                <div className="flex items-center justify-between text-xs pt-1">
                  <span className="text-juris-textSubtle">Category: {res.category}</span>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => navigate(`/app/assistant?q=Explain ${res.citationId} from ${res.documentTitle}`)}
                    >
                      Ask Copilot
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      icon={<ExternalLink className="w-3.5 h-3.5" />}
                      onClick={() => navigate(`/app/documents/${res.documentId}`)}
                    >
                      Inspect Source
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

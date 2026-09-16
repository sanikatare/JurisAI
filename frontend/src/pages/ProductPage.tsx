import React from 'react';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';
import { useNavigate } from 'react-router-dom';
import { FileSearch, ShieldAlert, GitCompare, SearchCode, Bot, FolderKanban, ArrowRight } from 'lucide-react';

export const ProductPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-juris-bg text-juris-textPrimary font-sans">
      <Navbar />

      <section className="pt-32 pb-16 max-w-7xl mx-auto px-6 text-center space-y-6">
        <Badge variant="outline">JurisAI Capabilities</Badge>
        <h1 className="font-serif text-4xl md:text-5xl font-light max-w-3xl mx-auto">
          Purpose-Built Capabilities for Enterprise Legal Teams.
        </h1>
        <p className="text-juris-textMuted text-base max-w-xl mx-auto">
          From rapid contract review to multi-document due diligence, discover the full suite of legal AI intelligence tools.
        </p>
      </section>

      <section className="max-w-7xl mx-auto px-6 pb-24 grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="space-y-4">
          <div className="w-10 h-10 rounded bg-juris-bgMuted flex items-center justify-center text-juris-textPrimary">
            <FileSearch className="w-5 h-5" />
          </div>
          <h3 className="font-serif text-xl font-semibold">Document Intelligence & Clause Breakdown</h3>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Extract key obligations, governing laws, effective dates, auto-renewal windows, and payment triggers automatically.
          </p>
          <ul className="text-xs text-juris-textBody space-y-1.5 list-disc pl-4">
            <li>Automatic clause classification</li>
            <li>Section hierarchy parsing</li>
            <li>Signatory & party identification</li>
          </ul>
        </Card>

        <Card className="space-y-4">
          <div className="w-10 h-10 rounded bg-juris-bgMuted flex items-center justify-center text-juris-textPrimary">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <h3 className="font-serif text-xl font-semibold">Contract Risk Analysis & Exposure Audit</h3>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Identify high-risk terms including unilateral indemnities, early termination fees, and uncapped liability provisions.
          </p>
          <ul className="text-xs text-juris-textBody space-y-1.5 list-disc pl-4">
            <li>Financial penalty quantification</li>
            <li>Asymmetric term highlighting</li>
            <li>Market baseline comparison</li>
          </ul>
        </Card>

        <Card className="space-y-4">
          <div className="w-10 h-10 rounded bg-juris-bgMuted flex items-center justify-center text-juris-textPrimary">
            <SearchCode className="w-5 h-5" />
          </div>
          <h3 className="font-serif text-xl font-semibold">Ask My Docs (RAG Knowledge Engine)</h3>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Query across your entire document repository using natural language with reciprocal rank fusion retrieval.
          </p>
          <ul className="text-xs text-juris-textBody space-y-1.5 list-disc pl-4">
            <li>Hybrid vector + BM25 search</li>
            <li>Verified RAG citations</li>
            <li>Category & risk filtering</li>
          </ul>
        </Card>

        <Card className="space-y-4">
          <div className="w-10 h-10 rounded bg-juris-bgMuted flex items-center justify-center text-juris-textPrimary">
            <GitCompare className="w-5 h-5" />
          </div>
          <h3 className="font-serif text-xl font-semibold">Contract Comparison & Material Diff</h3>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Compare two versions of an agreement side-by-side to highlight added, modified, or omitted obligations.
          </p>
          <ul className="text-xs text-juris-textBody space-y-1.5 list-disc pl-4">
            <li>Side-by-side redline preview</li>
            <li>Risk delta commentary</li>
            <li>Material term tracking</li>
          </ul>
        </Card>
      </section>

      <section className="py-16 bg-juris-bgMuted border-t border-juris-border text-center">
        <Button variant="primary" size="lg" onClick={() => navigate('/app')} icon={<ArrowRight className="w-4 h-4" />}>
          Try Capabilities in Workspace
        </Button>
      </section>

      <Footer />
    </div>
  );
};

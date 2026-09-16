import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowRight, ShieldCheck, FileText, Scale, Sparkles, CheckCircle2,
  Lock, Search, GitCompare, Bot, FileSearch, ArrowUpRight, ShieldAlert, Cpu
} from 'lucide-react';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';

export const LandingPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'clauses' | 'risk'>('overview');
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-juris-bg text-juris-textPrimary font-sans">
      <Navbar />

      {/* Hero Section */}
      <section className="pt-32 pb-20 md:pt-40 md:pb-28 max-w-7xl mx-auto px-6 text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-juris-border bg-juris-bgMuted text-xs font-medium text-juris-textMuted tracking-wider uppercase">
          <Sparkles className="w-3.5 h-3.5 text-juris-textPrimary" />
          <span>LEGAL AI, REIMAGINED</span>
        </div>

        <h1 className="font-serif text-4xl md:text-6xl lg:text-7xl font-light text-juris-textPrimary tracking-tight max-w-4xl mx-auto leading-[1.1]">
          Understand Every Legal Document With Intelligence.
        </h1>

        <p className="text-base md:text-lg text-juris-textMuted max-w-2xl mx-auto font-normal leading-relaxed">
          JurisAI transforms complex legal documents into clear, evidence-grounded insights—helping you understand obligations, risks, clauses, and decisions with confidence.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Button
            variant="primary"
            size="lg"
            onClick={() => navigate('/app')}
            icon={<ArrowRight className="w-4 h-4" />}
          >
            Explore JurisAI
          </Button>
          <a href="#product-visualization">
            <Button variant="outline" size="lg">
              See How It Works
            </Button>
          </a>
        </div>

        <div className="pt-4 flex items-center justify-center gap-8 text-xs text-juris-textSubtle">
          <span className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> Zero Model Data Retention</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> Grounded Source Citations</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> Decision-Support Architecture</span>
        </div>
      </section>

      {/* Hero Product Interactive Preview Section */}
      <section id="product-visualization" className="max-w-6xl mx-auto px-6 pb-24">
        <div className="bg-white border border-juris-border rounded-xl shadow-elevated overflow-hidden">
          {/* Top Bar of Product Screen */}
          <div className="bg-juris-bgMuted border-b border-juris-border px-5 py-3 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-amber-400"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-green-400"></div>
              </div>
              <span className="ml-3 font-medium text-juris-textMuted flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5" /> Commercial Lease Agreement (Wilmington HQ).pdf
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="high" size="sm">Overall Risk: High</Badge>
              <span className="text-[11px] text-juris-textSubtle">Analyzed 12 mins ago</span>
            </div>
          </div>

          {/* Main Product Screen Split-Pane */}
          <div className="grid grid-cols-1 md:grid-cols-12 min-h-[440px]">
            {/* Left Document View (7 cols) */}
            <div className="md:col-span-7 border-b md:border-b-0 md:border-r border-juris-border p-6 font-serif text-sm text-juris-textBody leading-relaxed space-y-4 bg-white overflow-y-auto max-h-[440px]">
              <div className="border-b border-juris-border pb-3">
                <p className="text-xs uppercase tracking-widest font-sans font-semibold text-juris-textSubtle">SECTION 4 — TERMINATION & DEFAULT</p>
                <h3 className="text-lg font-semibold text-juris-textPrimary mt-0.5">4.2 Notice of Termination and Penalty</h3>
              </div>
              <p className="clause-highlight-high p-3 rounded text-xs leading-relaxed font-sans">
                <span className="font-semibold text-juris-riskHigh block mb-1">High Risk Penalty Detected:</span>
                "Tenant may terminate this Agreement prior to the expiration of the initial term only upon providing one hundred eighty (180) days prior written notice to Landlord AND payment of an Early Termination Fee equal to twelve (12) months of base rent."
              </p>
              <div className="border-b border-juris-border pb-3 pt-2">
                <p className="text-xs uppercase tracking-widest font-sans font-semibold text-juris-textSubtle">SECTION 9 — INDEMNIFICATION</p>
                <h3 className="text-lg font-semibold text-juris-textPrimary mt-0.5">9.1 Tenant Indemnity Obligations</h3>
              </div>
              <p className="clause-highlight-high p-3 rounded text-xs leading-relaxed font-sans">
                "Tenant agrees to defend, indemnify, and hold harmless Landlord from and against any and all claims, damages, liabilities... regardless of Landlord's comparative negligence."
              </p>
            </div>

            {/* Right JurisAI Intelligence Panel (5 cols) */}
            <div className="md:col-span-5 bg-juris-bgSecondary p-6 flex flex-col justify-between space-y-4 font-sans text-xs">
              <div className="space-y-3">
                <div className="flex items-center justify-between border-b border-juris-border pb-3">
                  <div className="flex items-center gap-1.5 font-semibold text-juris-textPrimary text-sm">
                    <Sparkles className="w-4 h-4 text-juris-textPrimary" /> JurisAI Intelligence Analysis
                  </div>
                  <Badge variant="outline">Decision Support</Badge>
                </div>

                <div className="bg-white p-3.5 rounded-lg border border-juris-border space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-juris-textPrimary">Key Finding #1 — Termination Exposure</span>
                    <Badge variant="high" size="sm">High Risk</Badge>
                  </div>
                  <p className="text-juris-textMuted leading-normal">
                    Requires 180 days notice + 12 months base rent penalty. Total estimated financial exposure: <strong className="text-juris-textPrimary">$1,200,000</strong>.
                  </p>
                </div>

                <div className="bg-white p-3.5 rounded-lg border border-juris-border space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-juris-textPrimary">Key Finding #2 — Unilateral Indemnity</span>
                    <Badge variant="high" size="sm">High Risk</Badge>
                  </div>
                  <p className="text-juris-textMuted leading-normal">
                    Tenant indemnifies Landlord even for Landlord's comparative negligence. Violates standard market terms.
                  </p>
                </div>
              </div>

              <div className="pt-2 border-t border-juris-border flex items-center justify-between">
                <span className="text-[11px] text-juris-textSubtle">Citation: Section 4.2 & 9.1</span>
                <Button variant="primary" size="sm" onClick={() => navigate('/app/documents/DOC-2026-8812')}>
                  Open Interactive Viewer
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* One Workspace Section */}
      <section className="py-20 bg-white border-t border-juris-border">
        <div className="max-w-7xl mx-auto px-6 space-y-12">
          <div className="text-center space-y-3 max-w-2xl mx-auto">
            <h2 className="font-serif text-3xl md:text-4xl font-light text-juris-textPrimary">
              One Unified Workspace for Legal Intelligence.
            </h2>
            <p className="text-juris-textMuted text-sm leading-relaxed">
              JurisAI unifies contract review, risk analysis, cross-document RAG search, and agent orchestration into a singular editorial environment.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card hover className="space-y-3">
              <div className="w-9 h-9 rounded bg-juris-bgMuted border border-juris-border flex items-center justify-center text-juris-textPrimary">
                <FileSearch className="w-4 h-4" />
              </div>
              <h3 className="font-serif text-lg font-semibold text-juris-textPrimary">Document Intelligence</h3>
              <p className="text-xs text-juris-textMuted leading-relaxed">
                Parse complex agreements into key obligations, automatic renewals, termination windows, and liability limits instantly.
              </p>
            </Card>

            <Card hover className="space-y-3">
              <div className="w-9 h-9 rounded bg-juris-bgMuted border border-juris-border flex items-center justify-center text-juris-textPrimary">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <h3 className="font-serif text-lg font-semibold text-juris-textPrimary">Risk Analysis</h3>
              <p className="text-xs text-juris-textMuted leading-relaxed">
                Identify unfavorable governing laws, asymmetric indemnities, and hidden financial penalties with exact clause citations.
              </p>
            </Card>

            <Card hover className="space-y-3">
              <div className="w-9 h-9 rounded bg-juris-bgMuted border border-juris-border flex items-center justify-center text-juris-textPrimary">
                <Search className="w-4 h-4" />
              </div>
              <h3 className="font-serif text-lg font-semibold text-juris-textPrimary">Ask My Docs (RAG)</h3>
              <p className="text-xs text-juris-textMuted leading-relaxed">
                Perform cross-repository natural language search with reciprocal rank fusion (RRF) and verifiable evidence citations.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Security & Trust Section */}
      <section className="py-20 bg-juris-bgSecondary border-t border-juris-border">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-5">
            <Badge variant="outline">Enterprise Security</Badge>
            <h2 className="font-serif text-3xl md:text-4xl font-light text-juris-textPrimary leading-tight">
              Designed for Confidentiality & Legal Compliance.
            </h2>
            <p className="text-sm text-juris-textMuted leading-relaxed">
              Your legal agreements contain critical corporate IP and strategic terms. JurisAI enforces evidence-grounded outputs with strict data isolation.
            </p>
            <ul className="space-y-3 text-xs text-juris-textBody">
              <li className="flex items-center gap-2.5">
                <Lock className="w-4 h-4 text-juris-textPrimary shrink-0" />
                <span><strong>Private by Design:</strong> Zero retention for public model training.</span>
              </li>
              <li className="flex items-center gap-2.5">
                <ShieldCheck className="w-4 h-4 text-juris-textPrimary shrink-0" />
                <span><strong>Evidence Grounding:</strong> Every AI response links directly to verified clause text.</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Cpu className="w-4 h-4 text-juris-textPrimary shrink-0" />
                <span><strong>Audit-Ready Activity:</strong> Chronological logging for compliance verification.</span>
              </li>
            </ul>
            <div className="pt-2">
              <Link to="/security">
                <Button variant="outline" size="sm" icon={<ArrowUpRight className="w-3.5 h-3.5" />}>
                  Read Security Whitepaper
                </Button>
              </Link>
            </div>
          </div>

          <div className="bg-white border border-juris-border rounded-xl p-8 space-y-6 shadow-subtle">
            <div className="border-b border-juris-border pb-4">
              <h4 className="font-serif text-base font-semibold text-juris-textPrimary">Decision Support Guarantee</h4>
              <p className="text-xs text-juris-textMuted mt-1">
                JurisAI provides evidence synthesis to empower qualified legal counsel, maintaining strict human-in-the-loop control.
              </p>
            </div>
            <div className="space-y-3 text-xs text-juris-textMuted">
              <div className="p-3 bg-juris-bgMuted rounded border border-juris-border">
                <p className="font-medium text-juris-textPrimary mb-1">Transparent Confidence Scoring</p>
                <p>Retrieval similarity scores and source section links accompanying every answer.</p>
              </div>
              <div className="p-3 bg-juris-bgMuted rounded border border-juris-border">
                <p className="font-medium text-juris-textPrimary mb-1">Deterministic Pre-processing</p>
                <p>Structured parsing prevents hallucinated clause text or invalid citations.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-juris-card text-white border-t border-juris-surfaceBorder text-center space-y-6">
        <h2 className="font-serif text-3xl md:text-5xl font-light max-w-3xl mx-auto leading-tight">
          Ready to Reimagine Your Legal Document Intelligence?
        </h2>
        <p className="text-juris-textSubtle text-sm max-w-xl mx-auto">
          Explore how JurisAI accelerates contract review, risk audits, and due diligence workflows.
        </p>
        <div className="pt-2">
          <Button
            variant="primary"
            size="lg"
            className="bg-white text-juris-dark hover:bg-juris-bgMuted"
            onClick={() => navigate('/app')}
            icon={<ArrowRight className="w-4 h-4" />}
          >
            Launch JurisAI Workspace
          </Button>
        </div>
      </section>

      <Footer />
    </div>
  );
};

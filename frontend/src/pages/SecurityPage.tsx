import React from 'react';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Badge } from '../components/ui/Badge';
import { ShieldCheck, Lock, EyeOff, FileCode, CheckCircle2 } from 'lucide-react';

export const SecurityPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-juris-bg text-juris-textPrimary font-sans">
      <Navbar />

      <section className="pt-32 pb-16 max-w-5xl mx-auto px-6 text-center space-y-6">
        <Badge variant="outline">Security & Data Governance</Badge>
        <h1 className="font-serif text-4xl md:text-5xl font-light">
          Built for Legal Confidentiality.
        </h1>
        <p className="text-juris-textMuted text-base max-w-xl mx-auto">
          JurisAI maintains strict boundaries to protect attorney-client privilege, corporate IP, and sensitive financial terms.
        </p>
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-24 space-y-10">
        <div className="bg-white border border-juris-border rounded-xl p-8 space-y-4 shadow-subtle">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-juris-bgMuted border border-juris-border rounded-lg text-juris-textPrimary">
              <EyeOff className="w-5 h-5" />
            </div>
            <h3 className="font-serif text-xl font-semibold">Zero Public Model Training Guarantee</h3>
          </div>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Your uploaded agreements, contract text, and query history are never used to train public or foundational LLM models. All vector embeddings and cache indices remain strictly isolated within your organization's dedicated workspace container.
          </p>
        </div>

        <div className="bg-white border border-juris-border rounded-xl p-8 space-y-4 shadow-subtle">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-juris-bgMuted border border-juris-border rounded-lg text-juris-textPrimary">
              <FileCode className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-xl font-semibold">Deterministic Citation Architecture</h3>
          </div>
          <p className="text-xs text-juris-textMuted leading-relaxed">
            Unlike unconstrained generative chatbots, JurisAI utilizes deterministic document parsing and hybrid reciprocal rank fusion retrieval. Every AI insight requires explicit section citations and verifiable text excerpts.
          </p>
        </div>

        <div className="bg-white border border-juris-border rounded-xl p-8 space-y-4 shadow-subtle">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-juris-bgMuted border border-juris-border rounded-lg text-juris-textPrimary">
              <Lock className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-xl font-semibold">Encryption & Access Controls</h3>
          </div>
          <ul className="text-xs text-juris-textBody space-y-2">
            <li className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> TLS 1.3 encryption in transit & AES-256 encryption at rest
            </li>
            <li className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> Role-based access control (RBAC) per matter/workspace
            </li>
            <li className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-juris-riskLow" /> Chronological audit trails for document access & AI inquiries
            </li>
          </ul>
        </div>
      </section>

      <Footer />
    </div>
  );
};

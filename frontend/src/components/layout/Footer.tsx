import React from 'react';
import { Scale, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-juris-border py-16 text-juris-textMuted text-xs">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-5 gap-10">
        {/* Brand Column */}
        <div className="col-span-2 space-y-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-juris-textPrimary flex items-center justify-center text-white">
              <Scale className="w-3.5 h-3.5" />
            </div>
            <span className="font-serif text-lg font-bold text-juris-textPrimary tracking-tight">JurisAI</span>
          </div>
          <p className="text-juris-textMuted text-xs leading-relaxed max-w-sm">
            AI-Powered Legal Document Intelligence Platform. Grounded evidence analysis, clause identification, and contract risk evaluation for corporate legal teams and counsel.
          </p>
          <div className="flex items-center gap-2 text-juris-textSubtle text-[11px]">
            <ShieldCheck className="w-4 h-4 text-juris-riskLow" />
            <span>Evidence-Grounded Intelligence • Decision Support Architecture</span>
          </div>
        </div>

        {/* Product Links */}
        <div className="space-y-3">
          <p className="font-semibold text-juris-textPrimary uppercase tracking-wider text-[11px]">Product</p>
          <ul className="space-y-2 text-juris-textMuted">
            <li><Link to="/app/assistant" className="hover:text-juris-textPrimary">Legal Assistant</Link></li>
            <li><Link to="/app/documents" className="hover:text-juris-textPrimary">Document Vault</Link></li>
            <li><Link to="/app/ask" className="hover:text-juris-textPrimary">Ask My Docs (RAG)</Link></li>
            <li><Link to="/app/compare" className="hover:text-juris-textPrimary">Contract Diff</Link></li>
            <li><Link to="/app/agents" className="hover:text-juris-textPrimary">Legal Agents</Link></li>
          </ul>
        </div>

        {/* Solutions Links */}
        <div className="space-y-3">
          <p className="font-semibold text-juris-textPrimary uppercase tracking-wider text-[11px]">Solutions</p>
          <ul className="space-y-2 text-juris-textMuted">
            <li><a href="#solutions" className="hover:text-juris-textPrimary">Corporate Counsel</a></li>
            <li><a href="#solutions" className="hover:text-juris-textPrimary">Law Firms</a></li>
            <li><a href="#solutions" className="hover:text-juris-textPrimary">Compliance & AML</a></li>
            <li><a href="#solutions" className="hover:text-juris-textPrimary">M&A Due Diligence</a></li>
            <li><a href="#solutions" className="hover:text-juris-textPrimary">Lease Audit</a></li>
          </ul>
        </div>

        {/* Company & Legal */}
        <div className="space-y-3">
          <p className="font-semibold text-juris-textPrimary uppercase tracking-wider text-[11px]">Legal & Trust</p>
          <ul className="space-y-2 text-juris-textMuted">
            <li><Link to="/security" className="hover:text-juris-textPrimary">Security Architecture</Link></li>
            <li><a href="#" className="hover:text-juris-textPrimary">Privacy Notice</a></li>
            <li><a href="#" className="hover:text-juris-textPrimary">Terms of Service</a></li>
            <li><a href="#" className="hover:text-juris-textPrimary">Decision Support Notice</a></li>
            <li><a href="#" className="hover:text-juris-textPrimary">Security Whitepaper</a></li>
          </ul>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 mt-12 pt-6 border-t border-juris-border flex flex-col md:flex-row items-center justify-between text-juris-textSubtle gap-4">
        <p>© 2026 JurisAI Technologies Corp. All rights reserved.</p>
        <p>JurisAI is designed as an AI decision-support platform for legal professionals and does not replace qualified legal counsel.</p>
      </div>
    </footer>
  );
};

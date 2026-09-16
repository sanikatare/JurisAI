import React, { useState } from 'react';
import { User, Shield, Lock, Bell, Sliders, CheckCircle2, Key } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Badge } from '../../components/ui/Badge';

export const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'ai'>('profile');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 font-sans">
      <div className="space-y-1 border-b border-juris-border pb-4">
        <Badge variant="outline">Workspace Admin</Badge>
        <h1 className="font-serif text-3xl font-light text-juris-textPrimary">Settings & Preferences</h1>
        <p className="text-xs text-juris-textMuted">Manage counsel profile, security governance, and JurisAI model preferences.</p>
      </div>

      <div className="flex items-center gap-2 border-b border-juris-border pb-1">
        <button
          onClick={() => setActiveTab('profile')}
          className={`px-4 py-2 text-xs font-medium border-b-2 transition-colors ${
            activeTab === 'profile' ? 'border-juris-textPrimary text-juris-textPrimary font-semibold' : 'border-transparent text-juris-textMuted hover:text-juris-textPrimary'
          }`}
        >
          Profile & Organization
        </button>
        <button
          onClick={() => setActiveTab('security')}
          className={`px-4 py-2 text-xs font-medium border-b-2 transition-colors ${
            activeTab === 'security' ? 'border-juris-textPrimary text-juris-textPrimary font-semibold' : 'border-transparent text-juris-textMuted hover:text-juris-textPrimary'
          }`}
        >
          Security & Privacy
        </button>
        <button
          onClick={() => setActiveTab('ai')}
          className={`px-4 py-2 text-xs font-medium border-b-2 transition-colors ${
            activeTab === 'ai' ? 'border-juris-textPrimary text-juris-textPrimary font-semibold' : 'border-transparent text-juris-textMuted hover:text-juris-textPrimary'
          }`}
        >
          AI Copilot Parameters
        </button>
      </div>

      {saved && (
        <div className="p-3 bg-juris-riskLowBg border border-juris-riskLowBorder text-juris-riskLow rounded text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> Preferences updated cleanly.
        </div>
      )}

      {activeTab === 'profile' && (
        <div className="bg-white border border-juris-border rounded-xl p-6 space-y-6 shadow-subtle max-w-2xl">
          <div className="space-y-4">
            <h3 className="font-serif text-base font-semibold">Counsel Profile</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium mb-1">Full Name</label>
                <Input defaultValue="Jane Doe, Esq." />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">Title</label>
                <Input defaultValue="Senior Legal Counsel" />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium mb-1">Organization / Law Firm</label>
              <Input defaultValue="Apex Holdings LLC — Legal Department" />
            </div>
          </div>
          <Button variant="primary" size="sm" onClick={handleSave}>Save Profile</Button>
        </div>
      )}

      {activeTab === 'security' && (
        <div className="bg-white border border-juris-border rounded-xl p-6 space-y-6 shadow-subtle max-w-2xl">
          <div className="space-y-3">
            <h3 className="font-serif text-base font-semibold">Privacy Controls</h3>
            <div className="flex items-center justify-between p-3 bg-juris-bgMuted border border-juris-border rounded text-xs">
              <div>
                <p className="font-semibold text-juris-textPrimary">Zero Public Model Training</p>
                <p className="text-juris-textMuted">Prevent document text from being retained for foundation model fine-tuning.</p>
              </div>
              <Badge variant="low">Enforced</Badge>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'ai' && (
        <div className="bg-white border border-juris-border rounded-xl p-6 space-y-6 shadow-subtle max-w-2xl">
          <div className="space-y-3">
            <h3 className="font-serif text-base font-semibold">RAG Retrieval Sensitivity</h3>
            <div className="space-y-2 text-xs">
              <label className="block font-medium">Reciprocal Rank Fusion (RRF) Top K Passages</label>
              <select className="w-full bg-juris-bgMuted border border-juris-border rounded p-2 text-xs">
                <option>Top 5 Passages (High Precision)</option>
                <option>Top 10 Passages (Balanced Context)</option>
                <option>Top 15 Passages (Exhaustive Survey)</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

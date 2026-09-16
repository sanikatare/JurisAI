import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Scale, ArrowRight, Lock } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('counsel@apexholdings.com');
  const [password, setPassword] = useState('••••••••••••');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/app');
  };

  return (
    <div className="min-h-screen bg-juris-bgSecondary flex flex-col justify-between font-sans">
      {/* Top Header */}
      <div className="p-6">
        <Link to="/" className="inline-flex items-center gap-2.5">
          <div className="w-8 h-8 rounded bg-juris-textPrimary flex items-center justify-center text-white font-bold">
            <Scale className="w-4 h-4" />
          </div>
          <span className="font-serif text-xl font-bold tracking-tight text-juris-textPrimary">JurisAI</span>
        </Link>
      </div>

      {/* Center Auth Card */}
      <div className="max-w-md w-full mx-auto px-6 py-12">
        <div className="bg-white border border-juris-border rounded-xl p-8 shadow-dropdown space-y-6">
          <div className="space-y-1">
            <h2 className="font-serif text-2xl font-semibold text-juris-textPrimary">Sign In to JurisAI</h2>
            <p className="text-xs text-juris-textMuted">Access your legal workspace & document repository</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-juris-textBody mb-1.5">Work Email</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="counsel@firm.com"
                required
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-medium text-juris-textBody">Password</label>
                <a href="#" className="text-xs text-juris-textMuted hover:text-juris-textPrimary">Forgot password?</a>
              </div>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <Button type="submit" variant="primary" className="w-full" icon={<ArrowRight className="w-4 h-4" />}>
              Sign In to Workspace
            </Button>
          </form>

          <div className="pt-4 border-t border-juris-border text-center text-xs text-juris-textMuted flex items-center justify-center gap-1.5">
            <Lock className="w-3.5 h-3.5" /> Single Sign-On (SSO) Enforced for Enterprise
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-6 text-center text-xs text-juris-textSubtle">
        © 2026 JurisAI Technologies Corp. Privacy • Terms • Security
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { Bot, Play, Plus, CheckCircle2, Sliders, ShieldCheck, Sparkles, X } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { jurisApi, AgentWorkflow } from '../../lib/api';

export const AgentsPage: React.FC = () => {
  const agents = jurisApi.getAgents();
  const [activeAgent, setActiveAgent] = useState<AgentWorkflow | null>(null);
  const [builderOpen, setBuilderOpen] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [runLog, setRunLog] = useState<string | null>(null);

  const handleRunAgent = (agent: AgentWorkflow) => {
    setActiveAgent(agent);
    setIsRunning(true);
    setRunLog(null);
    setTimeout(() => {
      setIsRunning(false);
      setRunLog(`Agent '${agent.name}' completed audit across 3 connected documents. Found 0 critical policy violations.`);
    }, 1500);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-juris-border pb-6">
        <div className="space-y-1">
          <Badge variant="outline">Enterprise AI Workflows</Badge>
          <h1 className="font-serif text-3xl font-light text-juris-textPrimary">JurisAI Autonomous Agents</h1>
          <p className="text-sm text-juris-textMuted">
            Purpose-built legal AI workflows for automated document auditing, clause isolation, and compliance verification.
          </p>
        </div>

        <Button variant="primary" size="md" icon={<Plus className="w-4 h-4" />} onClick={() => setBuilderOpen(true)}>
          Build Custom Agent
        </Button>
      </div>

      {/* Execution Status Banner if running */}
      {isRunning && (
        <div className="p-4 bg-juris-bgMuted border border-juris-border rounded-xl flex items-center gap-3 text-xs text-juris-textPrimary">
          <Sparkles className="w-5 h-5 animate-spin text-juris-textPrimary shrink-0" />
          <div>
            <p className="font-semibold">Running Agent: {activeAgent?.name}...</p>
            <p className="text-juris-textMuted">Parsing document ASTs and evaluating compliance rules against company policy.</p>
          </div>
        </div>
      )}

      {runLog && (
        <div className="p-4 bg-juris-riskLowBg border border-juris-riskLowBorder rounded-xl flex items-center justify-between text-xs text-juris-riskLow">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span className="font-medium">{runLog}</span>
          </div>
          <button onClick={() => setRunLog(null)} className="text-juris-textSubtle hover:text-juris-textPrimary">
            Dismiss
          </button>
        </div>
      )}

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <Card key={agent.id} hover className="flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 bg-juris-bgMuted border border-juris-border rounded-lg text-juris-textPrimary">
                  <Bot className="w-5 h-5" />
                </div>
                <Badge variant={agent.status === 'Active' ? 'low' : 'neutral'} size="sm">
                  {agent.status}
                </Badge>
              </div>

              <div>
                <h3 className="font-serif text-lg font-semibold text-juris-textPrimary">{agent.name}</h3>
                <p className="text-[11px] font-medium text-juris-textSubtle uppercase tracking-wider">{agent.role}</p>
              </div>

              <p className="text-xs text-juris-textMuted leading-relaxed">{agent.description}</p>

              <div className="space-y-1.5 pt-1">
                <p className="text-[10px] uppercase font-semibold text-juris-textSubtle">Capabilities</p>
                <div className="flex flex-wrap gap-1">
                  {agent.capabilities.map((cap, idx) => (
                    <span key={idx} className="text-[10px] px-2 py-0.5 bg-juris-bgMuted border border-juris-border rounded text-juris-textBody">
                      {cap}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-juris-border flex items-center justify-between text-xs">
              <span className="text-juris-textSubtle text-[11px]">Last used: {agent.lastUsed}</span>
              <Button
                variant="secondary"
                size="sm"
                icon={<Play className="w-3.5 h-3.5" />}
                onClick={() => handleRunAgent(agent)}
              >
                Run Agent
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Build an Agent Modal Drawer */}
      {builderOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
          <div className="w-full max-w-lg bg-white border border-juris-border rounded-xl shadow-dropdown overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b border-juris-border">
              <h3 className="font-serif text-lg font-semibold text-juris-textPrimary">Build Custom JurisAI Agent</h3>
              <button onClick={() => setBuilderOpen(false)} className="p-1 text-juris-textSubtle hover:text-juris-textPrimary">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-4 text-xs">
              <div className="space-y-1">
                <label className="font-medium text-juris-textPrimary">Agent Name</label>
                <input
                  type="text"
                  placeholder="e.g. M&A Indemnity Auditor"
                  className="w-full p-2 border border-juris-border rounded text-xs focus:outline-none focus:border-juris-textPrimary"
                />
              </div>

              <div className="space-y-1">
                <label className="font-medium text-juris-textPrimary">Instructions & System Prompt</label>
                <textarea
                  rows={3}
                  placeholder="Scans target agreements for missing mutual indemnification and flags any exposure exceeding $500k..."
                  className="w-full p-2 border border-juris-border rounded text-xs focus:outline-none focus:border-juris-textPrimary font-sans"
                />
              </div>

              <div className="space-y-1">
                <label className="font-medium text-juris-textPrimary">Knowledge Sources</label>
                <select className="w-full p-2 border border-juris-border rounded text-xs bg-juris-bgMuted">
                  <option>All Vault Documents (Full Repository)</option>
                  <option>Commercial Leases Category Only</option>
                  <option>Master Services Agreements Only</option>
                </select>
              </div>
            </div>

            <div className="p-4 bg-juris-bgMuted border-t border-juris-border flex justify-end gap-2">
              <Button variant="outline" size="sm" onClick={() => setBuilderOpen(false)}>Cancel</Button>
              <Button variant="primary" size="sm" onClick={() => setBuilderOpen(false)}>Save Agent Workflow</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

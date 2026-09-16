import React from 'react';
import { History, FileText, Search, ShieldAlert, Bot, Clock } from 'lucide-react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const HistoryPage: React.FC = () => {
  const historyItems = [
    { id: '1', type: 'Document Ingestion', title: 'Commercial Lease Agreement (Wilmington HQ)', time: '10 mins ago', category: 'Today' },
    { id: '2', type: 'Risk Analysis', title: 'Quantified $1.2M termination exposure in DOC-2026-8812', time: '1 hour ago', category: 'Today' },
    { id: '3', type: 'RAG Search', title: 'Cross-document query: "automatic renewal notice periods"', time: '3 hours ago', category: 'Today' },
    { id: '4', type: 'Agent Run', title: 'Contract Reviewer executed across 3 master agreements', time: 'Yesterday', category: 'Yesterday' },
    { id: '5', type: 'Document Diff', title: 'Compared Lease Version 1 vs Version 2 Counter-proposal', time: '3 days ago', category: 'Previous 7 Days' },
  ];

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6 font-sans">
      <div className="space-y-1 border-b border-juris-border pb-4">
        <Badge variant="outline">Chronological Audit Log</Badge>
        <h1 className="font-serif text-3xl font-light text-juris-textPrimary">Activity & Query History</h1>
        <p className="text-xs text-juris-textMuted">Complete audit record of document inspections, AI copilot queries, and agent runs.</p>
      </div>

      <div className="space-y-6">
        {['Today', 'Yesterday', 'Previous 7 Days'].map((cat) => {
          const items = historyItems.filter(i => i.category === cat);
          if (items.length === 0) return null;

          return (
            <div key={cat} className="space-y-3">
              <p className="text-xs font-semibold text-juris-textSubtle uppercase tracking-wider">{cat}</p>
              <div className="space-y-2">
                {items.map((item) => (
                  <Card key={item.id} padding="sm" className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-juris-bgMuted border border-juris-border rounded text-juris-textPrimary">
                        <Clock className="w-3.5 h-3.5" />
                      </div>
                      <div>
                        <p className="font-medium text-juris-textPrimary">{item.title}</p>
                        <p className="text-[11px] text-juris-textSubtle">{item.type} • {item.time}</p>
                      </div>
                    </div>
                    <Badge variant="neutral" size="sm">Audited</Badge>
                  </Card>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

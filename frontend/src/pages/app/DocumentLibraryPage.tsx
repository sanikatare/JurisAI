import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Search, Plus, Filter, Eye, ShieldAlert, Download, Trash2 } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { MOCK_LEGAL_DOCUMENTS } from '../../lib/api';

export const DocumentLibraryPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const navigate = useNavigate();

  const filteredDocs = MOCK_LEGAL_DOCUMENTS.filter(doc => {
    const matchesSearch = doc.title.toLowerCase().includes(query.toLowerCase()) || doc.id.toLowerCase().includes(query.toLowerCase());
    const matchesCat = selectedCategory === 'All' || doc.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-juris-border pb-6">
        <div>
          <Badge variant="outline">Enterprise Vault</Badge>
          <h1 className="font-serif text-3xl font-light text-juris-textPrimary mt-1">Document Library</h1>
          <p className="text-xs text-juris-textMuted">Centralized repository for contracts, commercial leases, and regulatory filings</p>
        </div>

        <Button variant="primary" size="md" icon={<Plus className="w-4 h-4" />} onClick={() => navigate('/app')}>
          Ingest Document
        </Button>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-3 border border-juris-border rounded-xl shadow-subtle">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-juris-bgMuted border border-juris-border rounded-lg text-xs w-full sm:w-80">
          <Search className="w-3.5 h-3.5 text-juris-textSubtle shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Filter by title, ID, or keyword..."
            className="w-full bg-transparent text-juris-textPrimary placeholder:text-juris-textSubtle focus:outline-none"
          />
        </div>

        <div className="flex items-center gap-2 text-xs w-full sm:w-auto">
          <span className="text-juris-textSubtle font-medium">Category:</span>
          {['All', 'Lease', 'Contract', 'M&A'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-md font-medium transition-colors ${
                selectedCategory === cat
                  ? 'bg-juris-textPrimary text-white'
                  : 'bg-juris-bgMuted text-juris-textMuted hover:text-juris-textPrimary border border-juris-border'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Documents Enterprise Table */}
      <div className="bg-white border border-juris-border rounded-xl shadow-subtle overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-juris-bgMuted border-b border-juris-border font-medium text-juris-textSubtle uppercase tracking-wider">
              <tr>
                <th className="py-3.5 px-4">Document Details</th>
                <th className="py-3.5 px-4">Type</th>
                <th className="py-3.5 px-4">Risk Status</th>
                <th className="py-3.5 px-4">Signatories</th>
                <th className="py-3.5 px-4">Governing Law</th>
                <th className="py-3.5 px-4">Last Modified</th>
                <th className="py-3.5 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-juris-border text-juris-textBody">
              {filteredDocs.map((doc) => (
                <tr key={doc.id} className="hover:bg-juris-bgSecondary transition-colors group">
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-3">
                      <FileText className="w-4 h-4 text-juris-textMuted shrink-0" />
                      <div>
                        <p className="font-medium text-juris-textPrimary group-hover:text-black">{doc.title}</p>
                        <p className="text-[11px] text-juris-textSubtle">{doc.id} • {doc.fileSize} • {doc.pageCount} pages</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 font-medium text-juris-textMuted">{doc.type}</td>
                  <td className="py-3.5 px-4">
                    <Badge variant={doc.riskLevel === 'High' ? 'high' : doc.riskLevel === 'Moderate' ? 'mod' : 'low'} size="sm">
                      {doc.riskLevel} Risk
                    </Badge>
                  </td>
                  <td className="py-3.5 px-4 text-juris-textMuted truncate max-w-[140px]">{doc.signatories.join(', ')}</td>
                  <td className="py-3.5 px-4 text-juris-textMuted">{doc.governingLaw}</td>
                  <td className="py-3.5 px-4 text-juris-textSubtle">{doc.lastModified}</td>
                  <td className="py-3.5 px-4 text-right">
                    <div className="flex items-center justify-end gap-1">
                      <Button variant="ghost" size="sm" icon={<Eye className="w-3.5 h-3.5" />} onClick={() => navigate(`/app/documents/${doc.id}`)}>
                        Inspect
                      </Button>
                      <Button variant="ghost" size="sm" icon={<ShieldAlert className="w-3.5 h-3.5" />} onClick={() => navigate(`/app/analysis/${doc.id}`)}>
                        Audit
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { Upload, X, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from './Button';
import { Badge } from './Badge';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess?: () => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({ isOpen, onClose, onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isSuccess, setIsSuccess] = useState(false);

  if (!isOpen) return null;

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleSelectFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleStartAnalysis = () => {
    if (!file) return;
    setIsUploading(true);
    let p = 0;
    const interval = setInterval(() => {
      p += 25;
      setProgress(p);
      if (p >= 100) {
        clearInterval(interval);
        setIsUploading(false);
        setIsSuccess(true);
        setTimeout(() => {
          setIsSuccess(false);
          setFile(null);
          setProgress(0);
          if (onUploadSuccess) onUploadSuccess();
          onClose();
        }, 1200);
      }
    }, 300);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div className="w-full max-w-lg bg-white border border-juris-border rounded-xl shadow-dropdown overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between px-6 py-4 border-b border-juris-border">
          <div>
            <h3 className="text-base font-semibold text-juris-textPrimary">Ingest Legal Document</h3>
            <p className="text-xs text-juris-textMuted">Upload PDF, DOCX, or Markdown for JurisAI analysis</p>
          </div>
          <button onClick={onClose} className="p-1 text-juris-textSubtle hover:text-juris-textPrimary rounded-md">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          {!isUploading && !isSuccess && (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleFileDrop}
              className="border-2 border-dashed border-juris-border hover:border-juris-textPrimary/50 rounded-xl p-8 text-center bg-juris-bgSecondary transition-colors cursor-pointer"
            >
              <input
                type="file"
                accept=".pdf,.docx,.md,.txt"
                onChange={handleSelectFile}
                className="hidden"
                id="doc-file-input"
              />
              <label htmlFor="doc-file-input" className="cursor-pointer flex flex-col items-center">
                <div className="p-3 bg-white border border-juris-border rounded-full shadow-subtle mb-3 text-juris-textPrimary">
                  <Upload className="w-6 h-6" />
                </div>
                <p className="text-sm font-medium text-juris-textPrimary">
                  {file ? file.name : 'Click to select or drag document here'}
                </p>
                <p className="text-xs text-juris-textSubtle mt-1">
                  Supports Commercial Leases, MSAs, M&A SPAs, Employment Contracts, and Regulatory Guidelines up to 50MB
                </p>
              </label>
            </div>
          )}

          {file && !isUploading && !isSuccess && (
            <div className="flex items-center justify-between p-3 bg-juris-bgMuted border border-juris-border rounded-lg text-xs">
              <div className="flex items-center gap-2.5">
                <FileText className="w-4 h-4 text-juris-textMuted" />
                <span className="font-medium text-juris-textPrimary">{file.name}</span>
                <span className="text-juris-textSubtle">({(file.size / (1024 * 1024)).toFixed(2)} MB)</span>
              </div>
              <Badge variant="neutral">Ready for AI Ingestion</Badge>
            </div>
          )}

          {isUploading && (
            <div className="space-y-3 py-6 text-center">
              <div className="w-full bg-juris-bgMuted h-2 rounded-full overflow-hidden">
                <div
                  className="bg-juris-textPrimary h-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-xs font-medium text-juris-textPrimary">
                JurisAI is parsing document hierarchy, extracting clauses, and running vector embeddings ({progress}%)...
              </p>
            </div>
          )}

          {isSuccess && (
            <div className="py-6 text-center space-y-2">
              <CheckCircle2 className="w-10 h-10 text-juris-riskLow mx-auto animate-bounce" />
              <p className="text-sm font-semibold text-juris-textPrimary">Document Ingested & Analyzed</p>
              <p className="text-xs text-juris-textMuted">Document index & risk summary generated cleanly.</p>
            </div>
          )}
        </div>

        <div className="px-6 py-3.5 bg-juris-bgMuted border-t border-juris-border flex items-center justify-between">
          <span className="text-[11px] text-juris-textSubtle flex items-center gap-1">
            <AlertCircle className="w-3.5 h-3.5" /> Private by design — Zero external model training
          </span>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={onClose}>Cancel</Button>
            <Button
              variant="primary"
              size="sm"
              disabled={!file || isUploading}
              onClick={handleStartAnalysis}
            >
              Start JurisAI Analysis
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

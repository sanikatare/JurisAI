import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Scale, LayoutDashboard, MessageSquareText, FolderKanban, ShieldAlert,
  GitCompare, SearchCode, Bot, History, Settings, Search, Plus, Bell, ChevronDown, User, LogOut
} from 'lucide-react';
import { GlobalSearchModal } from '../ui/GlobalSearchModal';
import { UploadModal } from '../ui/UploadModal';
import { Button } from '../ui/Button';

export const AppShell: React.FC = () => {
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { label: 'Home', path: '/app', icon: LayoutDashboard, exact: true },
    { label: 'Assistant', path: '/app/assistant', icon: MessageSquareText },
    { label: 'Documents', path: '/app/documents', icon: FolderKanban },
    { label: 'Risk Analysis', path: '/app/analysis', icon: ShieldAlert },
    { label: 'Compare', path: '/app/compare', icon: GitCompare },
    { label: 'Ask My Docs', path: '/app/ask', icon: SearchCode },
    { label: 'Agents', path: '/app/agents', icon: Bot },
    { label: 'History', path: '/app/history', icon: History },
    { label: 'Settings', path: '/app/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-juris-bg flex overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-juris-card text-white border-r border-juris-surfaceBorder flex flex-col shrink-0 z-30">
        {/* Brand */}
        <div className="h-16 px-5 flex items-center justify-between border-b border-juris-surfaceBorder">
          <NavLink to="/" className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded bg-white text-juris-dark flex items-center justify-center font-bold">
              <Scale className="w-4 h-4" />
            </div>
            <span className="font-serif text-lg font-bold tracking-tight text-white">JurisAI</span>
          </NavLink>
          <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-juris-surfaceLight text-juris-textSubtle border border-juris-surfaceBorder">
            PRO
          </span>
        </div>

        {/* Workspace Switcher */}
        <div className="p-3 border-b border-juris-surfaceBorder">
          <button className="w-full flex items-center justify-between p-2 rounded-md bg-juris-surface text-left text-xs hover:bg-juris-surfaceLight transition-colors">
            <div className="truncate">
              <p className="font-medium text-white truncate">Apex Holdings Legal</p>
              <p className="text-[11px] text-juris-textSubtle">Corporate Workspace</p>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-juris-textSubtle shrink-0" />
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = item.exact
              ? location.pathname === item.path
              : location.pathname.startsWith(item.path);

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-md text-xs font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-white text-juris-dark font-semibold shadow-subtle'
                      : 'text-juris-textSubtle hover:text-white hover:bg-juris-surfaceLight'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Upload Action */}
        <div className="p-3 border-t border-juris-surfaceBorder">
          <Button
            variant="secondary"
            size="sm"
            className="w-full justify-start text-xs bg-juris-surface text-white border-juris-surfaceBorder hover:bg-juris-surfaceLight"
            icon={<Plus className="w-3.5 h-3.5" />}
            onClick={() => setUploadModalOpen(true)}
          >
            Ingest Document
          </Button>
        </div>
      </aside>

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-juris-bgSecondary">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-juris-border px-6 flex items-center justify-between shrink-0 z-20">
          {/* Global Search Button */}
          <button
            onClick={() => setSearchModalOpen(true)}
            className="flex items-center gap-3 px-3.5 py-1.5 bg-juris-bgMuted border border-juris-border rounded-lg text-xs text-juris-textSubtle hover:text-juris-textPrimary hover:border-juris-borderDark transition-all w-80"
          >
            <Search className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Search documents, clauses, RAG...</span>
            <kbd className="ml-auto text-[10px] font-mono px-1.5 py-0.5 bg-white border border-juris-border rounded text-juris-textMuted">
              ⌘K
            </kbd>
          </button>

          {/* Right Header Controls */}
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              icon={<Plus className="w-3.5 h-3.5" />}
              onClick={() => setUploadModalOpen(true)}
            >
              Upload Document
            </Button>

            <button className="p-2 text-juris-textSubtle hover:text-juris-textPrimary rounded-md hover:bg-juris-bgMuted relative">
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-juris-riskLow rounded-full"></span>
            </button>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="flex items-center gap-2 pl-2 pr-1 py-1 rounded-md hover:bg-juris-bgMuted"
              >
                <div className="w-7 h-7 rounded-full bg-juris-card text-white flex items-center justify-center text-xs font-semibold">
                  JD
                </div>
                <span className="text-xs font-medium text-juris-textPrimary hidden sm:inline">Counsel</span>
                <ChevronDown className="w-3.5 h-3.5 text-juris-textSubtle" />
              </button>

              {userDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white border border-juris-border rounded-lg shadow-dropdown p-1 z-50 text-xs animate-in fade-in zoom-in-95 duration-100">
                  <div className="px-3 py-2 border-b border-juris-border">
                    <p className="font-semibold text-juris-textPrimary">Jane Doe, Esq.</p>
                    <p className="text-juris-textSubtle text-[11px]">Senior Legal Counsel</p>
                  </div>
                  <button
                    onClick={() => { setUserDropdownOpen(false); navigate('/app/settings'); }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-juris-textBody hover:bg-juris-bgMuted rounded"
                  >
                    <User className="w-3.5 h-3.5 text-juris-textSubtle" /> Workspace Settings
                  </button>
                  <button
                    onClick={() => { setUserDropdownOpen(false); navigate('/login'); }}
                    className="w-full flex items-center gap-2 px-3 py-2 text-juris-riskHigh hover:bg-juris-riskHighBg rounded"
                  >
                    <LogOut className="w-3.5 h-3.5" /> Sign Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Viewport Content */}
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* Global Modals */}
      <GlobalSearchModal isOpen={searchModalOpen} onClose={() => setSearchModalOpen(false)} />
      <UploadModal isOpen={uploadModalOpen} onClose={() => setUploadModalOpen(false)} />
    </div>
  );
};

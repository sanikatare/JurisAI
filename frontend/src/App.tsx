import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { ProductPage } from './pages/ProductPage';
import { SecurityPage } from './pages/SecurityPage';
import { LoginPage } from './pages/LoginPage';
import { AppShell } from './components/layout/AppShell';
import { DashboardPage } from './pages/app/DashboardPage';
import { AssistantPage } from './pages/app/AssistantPage';
import { DocumentViewerPage } from './pages/app/DocumentViewerPage';
import { RiskAnalysisPage } from './pages/app/RiskAnalysisPage';
import { AskMyDocsPage } from './pages/app/AskMyDocsPage';
import { DocumentComparePage } from './pages/app/DocumentComparePage';
import { AgentsPage } from './pages/app/AgentsPage';
import { DocumentLibraryPage } from './pages/app/DocumentLibraryPage';
import { HistoryPage } from './pages/app/HistoryPage';
import { SettingsPage } from './pages/app/SettingsPage';

export const App: React.FC = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/product" element={<ProductPage />} />
      <Route path="/features" element={<ProductPage />} />
      <Route path="/solutions" element={<ProductPage />} />
      <Route path="/security" element={<SecurityPage />} />
      <Route path="/about" element={<SecurityPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/sign-in" element={<LoginPage />} />
      <Route path="/signup" element={<LoginPage />} />
      <Route path="/get-started" element={<LoginPage />} />

      {/* Authenticated Application Workspace Shell */}
      <Route path="/app" element={<AppShell />}>
        <Route index element={<DashboardPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="assistant" element={<AssistantPage />} />
        <Route path="documents" element={<DocumentLibraryPage />} />
        <Route path="documents/:id" element={<DocumentViewerPage />} />
        <Route path="analysis" element={<RiskAnalysisPage />} />
        <Route path="analysis/:id" element={<RiskAnalysisPage />} />
        <Route path="compare" element={<DocumentComparePage />} />
        <Route path="ask" element={<AskMyDocsPage />} />
        <Route path="agents" element={<AgentsPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>

      {/* Catch-all fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;

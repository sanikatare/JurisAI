import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Scale, Menu, X, ArrowRight, ChevronDown } from 'lucide-react';
import { Button } from '../ui/Button';

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-200 ${
        isScrolled
          ? 'bg-white/90 backdrop-blur-md border-b border-juris-border py-3 shadow-subtle'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded bg-juris-textPrimary flex items-center justify-center text-white transition-transform group-hover:scale-105">
            <Scale className="w-4 h-4" />
          </div>
          <div className="flex flex-col">
            <span className="font-serif text-xl font-bold tracking-tight text-juris-textPrimary leading-none">
              Juris<span className="font-sans font-medium text-xs ml-0.5 uppercase tracking-widest text-juris-textMuted">AI</span>
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-juris-textMuted">
          <Link to="/product" className="hover:text-juris-textPrimary transition-colors flex items-center gap-1">
            Product <ChevronDown className="w-3.5 h-3.5 opacity-60" />
          </Link>
          <Link to="/solutions" className="hover:text-juris-textPrimary transition-colors">
            Solutions
          </Link>
          <Link to="/security" className="hover:text-juris-textPrimary transition-colors">
            Security & Trust
          </Link>
          <a href="#resources" className="hover:text-juris-textPrimary transition-colors">
            Resources
          </a>
        </nav>

        {/* Right CTA Actions */}
        <div className="hidden md:flex items-center gap-3">
          <Link to="/login">
            <Button variant="ghost" size="sm">Sign In</Button>
          </Link>
          <Link to="/app">
            <Button variant="primary" size="sm" icon={<ArrowRight className="w-3.5 h-3.5" />}>
              Open Workspace
            </Button>
          </Link>
        </div>

        {/* Mobile Hamburger Toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-juris-textPrimary rounded-md hover:bg-juris-bgMuted"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-b border-juris-border px-6 py-6 space-y-4 animate-in slide-in-from-top-4 duration-200">
          <div className="flex flex-col space-y-3 text-base font-medium text-juris-textBody">
            <Link to="/product" onClick={() => setMobileMenuOpen(false)}>Product</Link>
            <Link to="/solutions" onClick={() => setMobileMenuOpen(false)}>Solutions</Link>
            <Link to="/security" onClick={() => setMobileMenuOpen(false)}>Security & Trust</Link>
            <a href="#resources" onClick={() => setMobileMenuOpen(false)}>Resources</a>
          </div>
          <div className="pt-4 border-t border-juris-border flex flex-col gap-2.5">
            <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="outline" className="w-full">Sign In</Button>
            </Link>
            <Link to="/app" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="primary" className="w-full">Open Workspace</Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

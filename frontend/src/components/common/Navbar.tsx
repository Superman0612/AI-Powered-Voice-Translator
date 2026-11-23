import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Languages, 
  Mic, 
  History, 
  BarChart3, 
  Info, 
  LogOut, 
  Menu,
  X
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../services/api';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await api.health.check();
        setBackendHealthy(res.status === 'operational');
      } catch (e) {
        setBackendHealthy(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const navLinks = [
    { name: 'Translator', path: '/translate', icon: Mic },
    { name: 'History', path: '/history', icon: History },
    { name: 'ML Performance', path: '/performance', icon: BarChart3 },
    { name: 'About & Docs', path: '/about', icon: Info },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-rose-500 to-indigo-600 p-[2px] shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Languages className="w-5 h-5 text-indigo-400 group-hover:text-indigo-300" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xl font-bold tracking-tight text-white">Bhasha<span className="text-indigo-400">AI</span></span>
                <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                  IN-10
                </span>
              </div>
              <p className="text-[10px] text-slate-400 hidden sm:block tracking-wide">AI-Powered Voice Translator</p>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                    active
                      ? 'bg-slate-800 text-white shadow-inner'
                      : 'text-slate-300 hover:text-white hover:bg-slate-850'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${active ? 'text-indigo-400' : 'text-slate-400'}`} />
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Right Status & Auth Actions */}
          <div className="hidden md:flex items-center gap-4">
            {/* System Health Pill */}
            <div 
              className="flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-900 border border-slate-800"
              title={backendHealthy ? "FastAPI Backend: Operational (Port 8000)" : "Backend is offline! Start it with: python -m uvicorn app.main:app --port 8000"}
            >
              <span className="relative flex h-2 w-2">
                {backendHealthy && (
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                )}
                <span className={`relative inline-flex rounded-full h-2 w-2 ${backendHealthy ? 'bg-emerald-500' : backendHealthy === false ? 'bg-rose-500' : 'bg-amber-500'}`}></span>
              </span>
              <span className="text-slate-400 font-mono text-[11px]">
                {backendHealthy ? 'System Active' : backendHealthy === false ? 'API Offline' : 'Connecting'}
              </span>
            </div>

            {/* Auth Buttons / Profile */}
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-850">
                  <div className="w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-xs font-semibold uppercase">
                    {user?.username ? user.username[0] : 'U'}
                  </div>
                  <span className="text-xs font-medium text-slate-200 max-w-[120px] truncate">
                    {user?.full_name || user?.username}
                  </span>
                </div>
                <button
                  onClick={logout}
                  className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-900 transition-colors"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-850 transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-md shadow-indigo-600/20 transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu trigger */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-800 bg-slate-950 px-4 pt-2 pb-4 space-y-2">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium ${
                  active ? 'bg-slate-800 text-white' : 'text-slate-300 hover:bg-slate-850'
                }`}
              >
                <Icon className="w-5 h-5 text-indigo-400" />
                {link.name}
              </Link>
            );
          })}
          <div className="pt-3 border-t border-slate-850 flex flex-col gap-2">
            {isAuthenticated ? (
              <div className="flex items-center justify-between px-3 py-2">
                <span className="text-sm text-slate-300 font-medium">{user?.username}</span>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="text-xs text-rose-400 flex items-center gap-1 font-semibold"
                >
                  <LogOut className="w-4 h-4" /> Sign Out
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2 pt-2">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center px-4 py-2 rounded-lg bg-slate-900 border border-slate-800 text-sm font-semibold text-slate-200"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center px-4 py-2 rounded-lg bg-indigo-600 text-sm font-semibold text-white"
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

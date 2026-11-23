import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Languages, LogIn, Lock, Mail, AlertCircle, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const from = (location.state as any)?.from?.pathname || '/translate';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err: any) {
      console.error("Login failed:", err);
      const detail = err.response?.data?.detail;
      const errorMsg = typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ')
          : err.message || "Invalid credentials. Please try again.";
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[75vh] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md p-8 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-2xl space-y-6">
        {/* Brand */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center mx-auto border border-indigo-500/20 shadow-lg shadow-indigo-600/10">
            <Languages className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Sign in to BhashaAI</h2>
          <p className="text-xs text-slate-400">Access your personalized voice translation workspace</p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Email or Username
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@domain.com or admin"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Sign In</span>
              </>
            )}
          </button>
        </form>

        {/* Quick Admin Helper */}
        <div className="pt-2 border-t border-slate-800/80 space-y-2.5">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button
              type="button"
              onClick={() => {
                setEmail('shubhamdevatwal2121@gmail.com');
                setPassword('Shubham@404');
              }}
              className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-indigo-500/50 text-slate-300 text-center font-medium transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
            >
              <Lock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Master Admin</span>
            </button>
            <button
              type="button"
              onClick={() => {
                setEmail('admin');
                setPassword('Shubham@404');
              }}
              className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 hover:border-indigo-500/50 text-slate-300 text-center font-medium transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
            >
              <Lock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Quick Admin</span>
            </button>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/60 text-[11px] text-slate-400 text-center space-y-0.5">
            <p><span className="text-slate-500">Email:</span> <span className="text-indigo-300 font-mono">shubhamdevatwal2121@gmail.com</span></p>
            <p><span className="text-slate-500">Username:</span> <span className="text-indigo-300 font-mono">shubhamdevatwal</span> or <span className="text-indigo-300 font-mono">admin</span></p>
            <p><span className="text-slate-500">Password:</span> <span className="text-indigo-300 font-mono">Shubham@404</span></p>
          </div>
        </div>

        <p className="text-center text-xs text-slate-400 pt-2 border-t border-slate-800/80">
          New Student or Researcher?{' '}
          <Link to="/register" className="font-semibold text-indigo-400 hover:text-indigo-300 underline underline-offset-2">
            Create your Profile
          </Link>
        </p>
      </div>
    </div>
  );
};

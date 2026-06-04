import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Lock, Mail, Loader2, Sparkles, ChevronRight } from 'lucide-react';
import { authService } from '../services/auth';

const Login = () => {
    const [identifier, setIdentifier] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await authService.login(identifier, password);
            navigate('/dashboard');
        } catch (err) {
            console.error("Login failed:", err);
            const status = err.response?.status;
            if (status === 401) {
                setError('Invalid username/email or password.');
            } else if (status === 422) {
                setError('Please enter a valid username and password.');
            } else if (err.code === 'ERR_NETWORK' || !err.response) {
                setError('Cannot reach server. Make sure the backend is running on port 8000.');
            } else {
                setError(err.response?.data?.detail || 'Login failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-6 selection:bg-purple-500/30"
             style={{ backgroundColor: 'var(--bg-primary)' }}>
            {/* Background decorative blobs */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full blur-[120px]"
                     style={{ backgroundColor: 'rgba(var(--accent-rgb), 0.08)' }} />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full blur-[120px]"
                     style={{ backgroundColor: 'rgba(var(--accent-rgb), 0.06)' }} />
            </div>

            <div className="w-full max-w-md relative z-10 animate-fade-in">
                <div className="backdrop-blur-2xl rounded-[2rem] p-10 relative overflow-hidden group"
                     style={{
                         backgroundColor: 'var(--card-bg)',
                         border: '1px solid var(--border-color)',
                         boxShadow: 'var(--shadow-xl)'
                     }}>
                    {/* Subtle hover shine */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none" />

                    <div className="flex flex-col items-center mb-10">
                        <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5 shadow-lg group-hover:scale-105 transition-transform duration-500"
                             style={{ background: 'var(--btn-gradient)' }}>
                            <Sparkles className="w-8 h-8 text-white" />
                        </div>
                        <h1 className="text-3xl font-black tracking-tight mb-2" style={{ color: 'var(--text-primary)' }}>
                            AI Analyst
                        </h1>
                        <p className="text-sm font-medium tracking-wide" style={{ color: 'var(--text-secondary)' }}>
                            Enter your credentials to continue
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <div className="px-1 -mb-3">
                                <p className="text-[11px] font-bold text-red-500 uppercase tracking-widest leading-relaxed">
                                    {error}
                                </p>
                            </div>
                        )}

                        <div className="space-y-2">
                            <label className="text-[11px] font-bold uppercase tracking-[0.2em] ml-1"
                                   style={{ color: 'var(--text-secondary)' }}>Enter your username or Email address</label>
                            <div className="relative group/input">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors"
                                     style={{ color: 'var(--text-secondary)' }} />
                                <input
                                    type="text"
                                    value={identifier}
                                    onChange={(e) => { setIdentifier(e.target.value); setError(''); }}
                                    className="w-full h-14 pl-12 pr-4 rounded-2xl text-sm font-medium focus:outline-none focus:ring-2 transition-all"
                                    style={{
                                        backgroundColor: 'var(--bg-primary)',
                                        color: 'var(--text-primary)',
                                        border: '1px solid var(--border-color)',
                                        '--tw-ring-color': 'rgba(var(--accent-rgb), 0.2)',
                                    }}
                                    placeholder="Username or Email"
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between items-center px-1">
                                <label className="text-[11px] font-bold uppercase tracking-[0.2em]"
                                       style={{ color: 'var(--text-secondary)' }}>Password</label>
                                <a href="#" className="text-[11px] font-bold uppercase tracking-widest transition-colors hover:opacity-80"
                                   style={{ color: 'var(--accent-color)' }}>Forgot?</a>
                            </div>
                            <div className="relative group/input">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors"
                                     style={{ color: 'var(--text-secondary)' }} />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => { setPassword(e.target.value); setError(''); }}
                                    className="w-full h-14 pl-12 pr-4 rounded-2xl text-sm font-medium focus:outline-none focus:ring-2 transition-all"
                                    style={{
                                        backgroundColor: 'var(--bg-primary)',
                                        color: 'var(--text-primary)',
                                        border: '1px solid var(--border-color)',
                                        '--tw-ring-color': 'rgba(var(--accent-rgb), 0.2)',
                                    }}
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        <div className="flex items-center gap-3 px-1">
                            <div className="relative flex items-center justify-center">
                                <input type="checkbox" id="remember" className="peer w-5 h-5 opacity-0 absolute cursor-pointer" />
                                <div className="w-5 h-5 border-2 rounded-md transition-all peer-checked:border-[var(--accent-color)]"
                                     style={{ borderColor: 'var(--border-color)', backgroundColor: 'var(--bg-primary)' }} />
                                <div className="absolute text-white scale-0 peer-checked:scale-100 transition-transform pointer-events-none">
                                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="4">
                                        <path d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                            </div>
                            <label htmlFor="remember" className="text-xs font-bold cursor-pointer select-none"
                                   style={{ color: 'var(--text-secondary)' }}>Stay logged in</label>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full h-14 text-white rounded-2xl font-black text-sm uppercase tracking-widest transition-all flex items-center justify-center gap-3 active:scale-[0.97] mt-2 disabled:opacity-50 hover:brightness-110"
                            style={{
                                background: 'var(--btn-gradient)',
                                boxShadow: '0 8px 24px rgba(var(--accent-rgb), 0.3)'
                            }}
                        >
                            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                                <>
                                    <span>SIGN IN</span>
                                    <ChevronRight className="w-4 h-4" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-10 text-center">
                        <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                            New to the system?{' '}
                            <Link to="/signup" className="font-black ml-1 hover:underline underline-offset-4 transition-colors"
                                  style={{ color: 'var(--accent-color)' }}>
                                Create Account
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;

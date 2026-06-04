import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Info, Sparkles, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import ThemeToggle from './ThemeToggle';

const Layout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  return (
    <div className="flex flex-col h-screen w-full font-sans overflow-hidden transition-colors duration-300"
         style={{ backgroundColor: 'var(--bg-primary)', color: 'var(--text-primary)' }}>

      {/* ── Top Navigation Bar ── */}
      <nav style={{ backgroundColor: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-color)' }}
           className="px-8 py-3.5 flex items-center justify-between backdrop-blur-xl z-50 shrink-0 sticky top-0 shadow-sm">

        {/* Left: Brand */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="p-2.5 rounded-xl" style={{ background: 'var(--btn-gradient)' }}>
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col leading-tight">
            <h1 className="font-bold text-[15px] tracking-tight" style={{ color: 'var(--text-primary)' }}>
              HR Analytics
            </h1>
            <p className="text-[10px] font-semibold uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>
              Data‑Driven Hiring
            </p>
          </div>
        </div>

        {/* Center: Nav Tabs */}
        <div className="flex flex-1 items-center justify-center gap-8">
          {[
            { to: '/dashboard',              icon: LayoutDashboard, label: 'Dashboard' },
            { to: '/dashboard/ai-assistant', icon: MessageSquare,   label: 'AI Assistant' },
            { to: '/about',                  icon: Info,            label: 'About' },
          ].map((nav, i) => (
            <NavLink
              key={i}
              to={nav.to}
              end={nav.to === '/dashboard'}
              className={({ isActive }) =>
                `flex items-center gap-2 px-1 pb-1 text-sm font-semibold tracking-tight transition-all duration-200 border-b-2 ${
                  isActive
                    ? 'border-[var(--accent-color)] text-[var(--accent-color)]'
                    : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                }`
              }
            >
              <nav.icon className="w-4 h-4" />
              <span>{nav.label}</span>
            </NavLink>
          ))}
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-4 shrink-0">
          <ThemeToggle />
          <div className="w-px h-5 rounded-full" style={{ backgroundColor: 'var(--border-color)' }} />
          <button
            onClick={handleLogout}
            title="Sign Out"
            className="flex items-center gap-1.5 text-sm font-semibold rounded-xl px-3 py-2 transition-all duration-200 hover:text-red-500 hover:bg-red-500/5"
            style={{ color: 'var(--text-secondary)' }}
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </nav>

      {/* ── Page Content ── */}
      <main className="flex-1 overflow-hidden relative">
        <div className="h-full w-full overflow-y-auto px-6 py-6 custom-scroll">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;

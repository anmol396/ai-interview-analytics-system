import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import {
  Users,
  RefreshCw,
  Trophy, 
  CheckCircle, 
  Clock, 
  XCircle, 
  Activity, 
  Search,
  Loader2,
  Database
} from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [topPerformers, setTopPerformers] = useState([]);
  const [allCandidates, setAllCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [toast, setToast] = useState({ type: '', message: '' });
  const [searchQuery, setSearchQuery] = useState('');
  const [dbStatus, setDbStatus] = useState({ connected: false, name: '' });

  const fetchDashboardData = async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      // Check health
      try {
        const health = await analyticsAPI.getHealth();
        setDbStatus({ connected: true, name: health.data.database });
      } catch (e) {
        setDbStatus({ connected: false, name: '' });
      }

      const response = await analyticsAPI.getStats();
      if (response.data) {
        setStats(response.data.stats || { total_candidates: 0, passed: 0, pending: 0, failed: 0, today_evaluated: 0 });
        setTopPerformers(response.data.top_performers || []);
        setAllCandidates(response.data.all_candidates || []);
      }
      setError('');
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      if (err.response?.status === 401) {
        window.location.href = '/login';
      } else if (err.response?.status !== 404) {
        setError('Connection error. Ensure backend is running.');
      }
    } finally {
      if (!silent) setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const getScoreClass = (score) => {
    if (score >= 80) return 'badge-score-high';
    if (score >= 60) return 'badge-score-med';
    return 'badge-score-low';
  };

  const filteredCandidates = searchQuery.trim()
    ? allCandidates.filter(c =>
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.status.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : allCandidates;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-full w-full space-y-4 animate-in fade-in duration-500">
        <Loader2 className="w-10 h-10 animate-spin text-[var(--accent-color)] opacity-50" />
        <p className="text-sm font-medium text-[var(--text-secondary)] tracking-tight">Syncing HR Analytics Intelligence...</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full relative p-6">
      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 text-xs font-bold flex items-center gap-3 animate-in fade-in slide-in-from-top-2">
          <XCircle className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* Header Actions */}
      <div className="flex flex-row justify-between items-center mb-10 gap-4">
        <div className="flex items-center gap-4">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-2xl shadow-sm border transition-all duration-500 ${
            dbStatus.connected 
              ? 'bg-emerald-500/5 border-emerald-500/20' 
              : 'bg-red-500/5 border-red-500/20'
          }`}>
            <Database className={`w-3.5 h-3.5 ${dbStatus.connected ? 'text-emerald-500' : 'text-red-500'}`} />
            <span className={`text-[10px] font-bold uppercase tracking-widest ${dbStatus.connected ? 'text-emerald-600' : 'text-red-600'}`}>
              {dbStatus.connected ? 'MySQL Connected' : 'Disconnected'}
            </span>
            <span className={`w-1.5 h-1.5 rounded-full ${dbStatus.connected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-secondary)]" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search talent database..."
              className="h-10 pl-9 pr-4 rounded-xl border border-[var(--border-color)] bg-[var(--card-bg)] text-[var(--text-primary)] text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[var(--accent-color)]/20 focus:border-[var(--accent-color)] transition-all w-64 placeholder:text-[var(--text-secondary)]/50"
            />
          </div>
          <button
            onClick={() => fetchDashboardData()}
            className="h-10 w-10 flex items-center justify-center rounded-xl border border-[var(--border-color)] bg-[var(--card-bg)] text-[var(--text-secondary)] hover:text-[var(--accent-color)] transition-all duration-300 shadow-sm active:scale-95"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-6 pb-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { label: 'Total Candidates', val: stats?.total_candidates, icon: Users, color: 'text-purple-500' },
            { label: 'Passed Interviews', val: stats?.passed, icon: CheckCircle, color: 'text-emerald-500' },
            { label: 'Pending Reviews', val: stats?.pending, icon: Clock, color: 'text-amber-500' },
            { label: 'Failed', val: stats?.failed, icon: XCircle, color: 'text-red-500' }
          ].map((stat, i) => (
            <div key={i} className="glass-card p-6 flex flex-col w-full">
              <div className="flex items-center justify-between w-full mb-2">
                <p className="text-[10px] font-bold text-[var(--text-secondary)] uppercase tracking-widest">{stat.label}</p>
                <div className="flex items-center justify-center w-10 h-10 rounded-2xl bg-[var(--bg-primary)] border border-[var(--border-color)]">
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
              </div>
              <div className="min-w-0 mt-1">
                <p className="text-2xl font-bold text-[var(--text-primary)] tracking-tight tabular-nums">
                  {stat.val || 0}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6 items-start">
          <div className="glass-card flex flex-col overflow-hidden min-h-[600px]">
            <div className="overflow-x-auto flex-1 custom-scroll">
              <table className="dashboard-table">
                <thead>
                  <tr>
                    <th className="text-left font-bold">Candidate</th>
                    <th className="text-left font-bold text-[10px]">Role</th>
                    <th className="text-center font-bold">Score</th>
                    <th className="text-right font-bold">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-color)]">
                  {filteredCandidates.map((c, i) => (
                    <tr key={i} className="group transition-colors hover:bg-[var(--hover-color)]">
                      <td className="text-left py-5">
                        <span className="font-bold text-sm text-[var(--text-primary)] tracking-tight block truncate group-hover:text-[var(--accent-color)]">{c.name}</span>
                      </td>
                      <td className="text-left py-5">
                        <span className="text-[var(--text-secondary)] text-[10px] font-bold uppercase tracking-wide block truncate opacity-70">{c.role}</span>
                      </td>
                      <td className="text-center py-5">
                        <span className={`${getScoreClass(c.total_score)} badge-score text-[10px] font-black`}>
                          {c.total_score}
                        </span>
                      </td>
                      <td className="text-right py-5 pr-6">
                        <span className={`px-2.5 py-1 rounded-lg text-[10px] font-black tracking-tight border ${c.status === 'Passed' ? 'bg-emerald-500/5 text-emerald-600 border-emerald-500/10' :
                            c.status === 'Failed' ? 'bg-red-500/5 text-red-600 border-red-500/10' :
                              'bg-amber-500/5 text-amber-600 border-amber-500/10'
                          }`}>
                          {c.status.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {filteredCandidates.length === 0 && (
                    <tr>
                      <td colSpan={4} className="text-center py-20">
                        <p className="text-sm text-[var(--text-secondary)] opacity-50 font-medium">
                          {searchQuery ? 'No matching candidates found' : 'No candidates in database'}
                        </p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex flex-col gap-6">
            <div className="glass-card p-6 flex flex-col min-h-[600px]" style={{ background: 'var(--card-bg)' }}>
              <div className="flex items-center justify-between mb-8">
                <h3 className="font-bold text-xl text-[var(--text-primary)] flex items-center gap-2">
                  <Trophy className="w-5 h-5 text-amber-500" />
                  Top Rankings
                </h3>
              </div>
              <div className="space-y-3 overflow-y-auto flex-1 pr-1 custom-scroll">
                {topPerformers.map((performer, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 rounded-2xl border border-[var(--border-color)] hover:border-[var(--accent-color)]/20 transition-all duration-300 group bg-[var(--bg-primary)]/30">
                    <div className="flex items-center gap-4 min-w-0">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center font-black text-xs shrink-0 bg-[var(--card-bg)] border border-[var(--border-color)] text-[var(--text-secondary)] group-hover:text-[var(--accent-color)] group-hover:border-[var(--accent-color)]/20 transition-all">
                        {idx + 1}
                      </div>
                      <div className="truncate">
                        <p className="font-bold text-sm text-[var(--text-primary)] tracking-tight truncate group-hover:text-[var(--accent-color)] transition-colors">{performer.name}</p>
                        <p className="text-[10px] text-[var(--text-secondary)] font-bold uppercase tracking-widest truncate opacity-60">{performer.role}</p>
                      </div>
                    </div>
                    <div className="font-black text-xs tabular-nums px-3 py-1 rounded-xl text-white" style={{ background: 'var(--btn-gradient)', boxShadow: '0 4px 12px rgba(var(--accent-rgb), 0.3)' }}>
                      {performer.total_score}
                    </div>
                  </div>
                ))}
                {topPerformers.length === 0 && (
                  <div className="flex flex-col items-center justify-center py-20 text-center opacity-40">
                    <Trophy className="w-10 h-10 mb-2" />
                    <p className="text-xs font-bold uppercase tracking-widest">No rankings yet</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

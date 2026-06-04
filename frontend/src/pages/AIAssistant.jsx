import React, { useState, useEffect, useRef } from 'react';
import { 
  BarChart as ReBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell 
} from 'recharts';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { aiAPI } from '../services/api';
import { 
  Send, Bot, User, Loader2, Plus, Trash2, 
  MessageSquare, Trophy, AlertCircle, CheckCircle2, 
  BarChart2, UserCheck, TrendingUp, TrendingDown, Activity 
} from 'lucide-react';

const Markdown = ({ content, className = "text-sm font-medium leading-relaxed" }) => (
  <ReactMarkdown 
    remarkPlugins={[remarkGfm]}
    components={{
      p: ({node, ...props}) => <p className={className} {...props} />,
      strong: ({node, ...props}) => <strong className="text-[var(--accent-color)] font-black" {...props} />,
      li: ({node, ...props}) => <li className="ml-5 list-disc text-sm font-medium text-[var(--text-secondary)] py-1" {...props} />,
      ul: ({node, ...props}) => <ul className="space-y-1 my-2" {...props} />,
      h1: ({node, ...props}) => <h1 className="text-xl font-black mb-4" {...props} />,
      h2: ({node, ...props}) => <h2 className="text-lg font-black mb-3" {...props} />,
      h3: ({node, ...props}) => <h3 className="text-sm font-black uppercase tracking-wider mb-2 text-[var(--text-secondary)]" {...props} />,
      h4: ({node, ...props}) => <h4 className="text-[11px] font-black uppercase tracking-[0.15em] text-[var(--text-secondary)] mb-2 mt-4 flex items-center gap-2.5" {...props} />,
    }}
  >
    {content}
  </ReactMarkdown>
);

const DataTable = ({ headers, rows, compact = false }) => (
  <div className="overflow-hidden rounded-2xl border border-[var(--border-color)] bg-[var(--bg-primary)]/50 my-4 shadow-sm">
    <table className="w-full text-left border-collapse">
      <thead>
        <tr className="bg-[var(--card-bg)]">
          {headers.map((h, i) => (
            <th key={i} className={`px-4 ${compact ? 'py-2' : 'py-3'} text-[10px] font-bold uppercase tracking-widest text-[var(--text-secondary)] border-b border-[var(--border-color)]`}>
              {h}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i} className="border-b border-[var(--border-color)] last:border-0 hover:bg-[var(--hover-color)]/30 transition-colors">
            {row.map((cell, j) => {
              const isStatus = cell.toLowerCase() === 'passed' || cell.toLowerCase() === 'failed' || cell.toLowerCase() === 'pending';
              const isScore = !isNaN(cell) && cell !== "" && (headers[j]?.toLowerCase().includes('score') || headers[j]?.toLowerCase().includes('assessment') || headers[j]?.toLowerCase().includes('test'));
              
              return (
                <td key={j} className={`px-4 ${compact ? 'py-2' : 'py-3'} text-sm font-medium`}>
                  {isStatus ? (
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-black tracking-tight ${
                      cell.toLowerCase() === 'passed' ? 'bg-emerald-500/10 text-emerald-600' :
                      cell.toLowerCase() === 'failed' ? 'bg-red-500/10 text-red-600' :
                      'bg-amber-500/10 text-amber-600'
                    }`}>
                      {cell.toUpperCase()}
                    </span>
                  ) : isScore ? (
                    <span className={`font-bold tabular-nums ${Number(cell) >= 20 || Number(cell) >= 80 ? 'text-emerald-500' : Number(cell) >= 15 || Number(cell) >= 60 ? 'text-amber-500' : 'text-red-500'}`}>
                      {cell}
                    </span>
                  ) : (
                    <span className="text-[var(--text-primary)]">{cell}</span>
                  )}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);



const SummaryFooter = ({ rates }) => (
  <div className="grid grid-cols-2 gap-4 my-4">
    {rates.map((rate, i) => (
      <div key={i} className="p-4 rounded-2xl border border-[var(--border-color)] bg-[var(--card-bg)] flex items-center justify-between">
        <div>
          <p className="text-[10px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">{rate.label}</p>
          <p className="text-xl font-black text-[var(--text-primary)] tabular-nums">{rate.value}</p>
        </div>
        <div className={`p-2 rounded-xl ${rate.label.toLowerCase().includes('pass') ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-500'}`}>
          {rate.label.toLowerCase().includes('pass') ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
        </div>
      </div>
    ))}
  </div>
);

const AnalyticsChart = ({ data }) => {
  if (!data || data.length === 0) return null;
  const COLORS = ['#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95'];

  return (
    <div className="h-[280px] w-full mt-6 mb-8 p-6 rounded-3xl border border-[var(--border-color)] bg-[var(--bg-primary)]/40 shadow-xl backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-lg bg-[var(--accent-color)]/10 text-[var(--accent-color)]">
          <BarChart2 className="w-4 h-4" />
        </div>
        <h4 className="text-[11px] font-black uppercase tracking-[0.15em] text-[var(--text-secondary)]">Distribution Visualization</h4>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <ReBarChart data={data} layout="vertical" margin={{ left: 0, right: 40, top: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border-color)" opacity={0.2} />
          <XAxis type="number" hide />
          <YAxis 
            dataKey="role" 
            type="category" 
            width={120} 
            stroke="var(--text-secondary)" 
            fontSize={11} 
            fontWeight="700"
            axisLine={false}
            tickLine={false}
          />
          <Tooltip 
            cursor={{fill: 'var(--accent-color)', opacity: 0.05}}
            contentStyle={{ 
              backgroundColor: 'var(--card-bg)', 
              border: '1px solid var(--border-color)', 
              borderRadius: '16px',
              boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'
            }}
            itemStyle={{ color: 'var(--text-primary)', fontWeight: 'bold' }}
          />
          <Bar dataKey="count" radius={[0, 8, 8, 0]} barSize={24}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </ReBarChart>
      </ResponsiveContainer>
    </div>
  );
};

const FullListButton = ({ filterKey, total, hasMore, onAction, isEmbedded = false }) => {
  if (!filterKey) return null;
  
  return (
    <div className={`flex flex-col items-start gap-3 ${isEmbedded ? '' : 'mt-6 pt-4 border-t border-[var(--border-color)]/50'}`}>
       <p className="text-[13px] font-medium text-[var(--text-secondary)]">
          {hasMore ? `Showing partial results. ${total || ''} total matches found.` : `Showing all ${total || ''} results.`}
       </p>
       <button
         onClick={() => onAction && onAction(`__FULL_LIST__:${filterKey}`)}
         disabled={!hasMore}
         className={`px-4 py-2 border border-[var(--accent-color)] bg-[var(--bg-primary)] text-[var(--accent-color)] rounded-xl font-bold text-[11px] hover:bg-[var(--accent-color)] hover:text-white transition-all ${
           !hasMore ? 'opacity-40 cursor-not-allowed grayscale border-[var(--text-secondary)]/30 text-[var(--text-secondary)] hover:bg-transparent hover:text-[var(--text-secondary)]' : ''
         }`}
       >
         {hasMore ? `Show full list ${total ? `(${total})` : ''}` : 'All results shown'}
       </button>
    </div>
  );
};

const StructuredResponse = ({ content, onAction, filterKey, total, hasMore }) => {
  if (!content) return null;

  const sections = content.trim().split(/\n(?=(?:#+\s+)?(?:[\w\s]+\s+)?(?:Summary|Performers|Candidates|Breakdown|Insight|Full List|Analytics|Distribution|Comparison|Profile|Analysis):)/g);
  let buttonRendered = false;

  return (
    <div className="space-y-6">
      {sections.map((section, sIdx) => {
        const lines = section.trim().split('\n').map(l => l.trim());
        if (lines.length === 0) return null;

        const firstLine = lines[0].toLowerCase();
        const tableStartIdx = lines.findIndex(l => l.startsWith('|'));
        
        const isSummary = firstLine.includes('summary');
        const isBreakdown = firstLine.includes('breakdown');
        const isAnalytics = firstLine.includes('analytics') || firstLine.includes('distribution') || firstLine.includes('analysis');
        const isPerformers = firstLine.includes('performers') || firstLine.includes('candidates') || firstLine.includes('recommended') || firstLine.includes('full list') || firstLine.includes('comparison');

        const preambleLines = lines.slice(0, tableStartIdx === -1 ? lines.length : tableStartIdx).filter(l => l && !l.includes('---'));
        const postambleLines = tableStartIdx === -1 ? [] : lines.slice(tableStartIdx).filter(l => !l.startsWith('|') && l && !l.includes('---'));

        let tableHeaders = [];
        let tableRows = [];
        if (tableStartIdx !== -1) {
          const tableLines = lines.filter(l => l.startsWith('|'));
          if (tableLines.length >= 2) {
            tableHeaders = tableLines[0].split('|').filter(s => s.trim()).map(s => s.trim());
            tableRows = tableLines.slice(2).map(l => l.split('|').filter(s => s.trim()).map(s => s.trim()));
          }
        }

        return (
          <div key={sIdx} className="animate-in fade-in slide-in-from-bottom-2 duration-500 space-y-3">
            {preambleLines.map((p, i) => {
              const isHeading = p.startsWith('#');
              if (isHeading) {
                return (
                  <h4 key={i} className="text-[11px] font-black uppercase tracking-[0.15em] text-[var(--text-secondary)] mb-2 mt-4 first:mt-0 flex items-center gap-2.5">
                    <span className="p-1.5 rounded-lg bg-[var(--accent-color)]/10 text-[var(--accent-color)]">
                      {isAnalytics ? <BarChart2 className="w-3.5 h-3.5" /> : 
                       isPerformers || isSummary ? <Trophy className="w-3.5 h-3.5" /> : 
                       isBreakdown ? <Activity className="w-3.5 h-3.5" /> : <MessageSquare className="w-3.5 h-3.5" />}
                    </span>
                    <Markdown content={p.replace(/^#+\s+/, '').replace(/:$/, '')} />
                  </h4>
                );
              }
              return <div key={i} className="mb-1"><Markdown content={p} /></div>;
            })}

            {isAnalytics && tableRows.length > 0 && (
              <AnalyticsChart data={tableRows.map(r => ({ role: r[0], count: parseInt(r[1]) }))} />
            )}

            {tableRows.length > 0 && (
              <DataTable headers={tableHeaders} rows={tableRows} compact={isSummary || isBreakdown} />
            )}

            {postambleLines.length > 0 && (
              <div className="space-y-2 mt-3">
                {postambleLines.map((p, i) => {
                  if (p.includes(':') && !p.startsWith('#') && !p.includes('|')) {
                    const parts = p.split(':');
                    const label = parts[0].trim();
                    const value = parts[1].trim();
                    
                    // Only render as card if value looks like a number or status
                    if (!isNaN(value.replace(/[,. ]/g, '')) || value.length < 15) {
                      return (
                        <div key={i} className="my-4 p-6 rounded-3xl bg-gradient-to-br from-[var(--accent-color)]/10 to-[var(--accent-color)]/5 border border-[var(--accent-color)]/20 shadow-sm animate-in zoom-in-95 duration-500">
                           <div className="flex items-center gap-2 mb-1.5">
                              <Activity className="w-3.5 h-3.5 text-[var(--accent-color)] opacity-70" />
                              <span className="text-[10px] font-black uppercase tracking-[0.2em] text-[var(--accent-color)] leading-none">{label}</span>
                           </div>
                           <p className="text-4xl font-black text-[var(--text-primary)] tabular-nums tracking-tighter leading-none py-1">{value}</p>
                        </div>
                      );
                    }
                  }
                  
                  if (p.includes('Showing') && p.includes('of') && p.includes('results')) {
                     buttonRendered = true;
                     return (
                       <FullListButton 
                         key={i}
                         filterKey={filterKey}
                         total={total}
                         hasMore={hasMore}
                         onAction={onAction}
                         isEmbedded={true}
                       />
                     );
                  }
                  return <Markdown key={i} content={p} className="text-[13px] font-medium text-[var(--text-secondary)]" />;
                })}
              </div>
            )}
          </div>
        );
      })}
      
      {filterKey && !buttonRendered && (
        <FullListButton 
          filterKey={filterKey}
          total={total}
          hasMore={hasMore}
          onAction={onAction}
        />
      )}
    </div>
  );
};


const SafeContent = ({ content, isUser, onAction, filterKey, total, hasMore }) => {
  if (!content) return null;
  if (isUser) return <div className="whitespace-pre-wrap font-semibold text-sm">{content}</div>;
  if (content.includes('|') || content.includes('Insight:') || content.includes('#') || content.includes('Total:')) {
    return (
      <StructuredResponse 
        content={content} 
        onAction={onAction} 
        filterKey={filterKey} 
        total={total}
        hasMore={hasMore}
      />
    );
  }
  
  return (
    <div className="space-y-3">
      <Markdown content={content} />
    </div>
  );
};

const AIAssistant = () => {
  const WELCOME_MESSAGE = {
    role: 'system',
    content: "👋 Hi! I'm your HR AI Assistant. Ask me anything about candidates, interviews, and scores.\n\nTry:\n* Who scored the best?\n* Give me summary\n* Show failed candidates"
  };

  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const SUGGESTIONS = [
    "Show top 5 performers",
    "Top 5 ML engineers",
    "Top 5 Backend Developers",
    "How many candidates are pending review?",
    "Show candidates who failed",
    "Recommend best candidates for hiring"
  ];

  useEffect(() => {
    const savedSessions = localStorage.getItem('chat_sessions');
    if (savedSessions) {
      try {
        const parsed = JSON.parse(savedSessions);
        if (parsed && parsed.length > 0) {
          setSessions(parsed);
          // Load most recent session
          const latest = parsed.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0];
          setCurrentSessionId(latest.id);
          setMessages(latest.messages || [WELCOME_MESSAGE]);
          return;
        }
      } catch (e) {
        console.error('Error loading chat sessions', e);
      }
    }
    
    const newId = Date.now().toString();
    const newSession = {
      id: newId,
      title: 'New Chat',
      timestamp: new Date().toISOString(),
      messages: [WELCOME_MESSAGE]
    };
    setSessions([newSession]);
    setCurrentSessionId(newId);
    setMessages([WELCOME_MESSAGE]);
  }, []);

  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('chat_sessions', JSON.stringify(sessions));
    }
  }, [sessions]);

  const createNewSession = () => {
    const newId = Date.now().toString();
    const newSession = {
      id: newId,
      title: 'New Chat',
      timestamp: new Date().toISOString(),
      messages: [WELCOME_MESSAGE]
    };
    setSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(newId);
    setMessages([WELCOME_MESSAGE]);
  };

  const loadSession = (id) => {
    const session = sessions.find(s => s.id === id);
    if (session) {
      setCurrentSessionId(id);
      setMessages(session.messages || [WELCOME_MESSAGE]);
    }
  };

  const deleteSession = (id, e) => {
    e.stopPropagation();
    const updatedSessions = sessions.filter(s => s.id !== id);
    setSessions(updatedSessions);
    if (currentSessionId === id) {
      if (updatedSessions.length > 0) {
        loadSession(updatedSessions[0].id);
      } else {
        createNewSession();
      }
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchFullList = async (filterKey) => {
    if (!filterKey || loading) return;
    setLoading(true);
    try {
      const response = await aiAPI.getFullList(filterKey);
      const candidates = response.data.candidates || [];
      const total = response.data.total || 0;

      // Build markdown table
      let table = `**Full List (${total} candidates)**\n\n`;
      table += "| Rank | Name | Role | Status | Score |\n| --- | --- | --- | --- | --- |\n";
      candidates.forEach((c, i) => {
        table += `| ${i+1} | ${c.name} | ${c.role} | ${c.status} | ${c.total_score} |\n`;
      });

      const newMsg = { role: 'system', content: table, timestamp: new Date().toISOString() };
      setMessages(prev => {
        const updated = [...prev, newMsg];
        setSessions(s => s.map(sess => sess.id === currentSessionId ? { ...sess, messages: updated } : sess));
        return updated;
      });
    } catch (err) {
      setMessages(prev => [...prev, { role: 'system', content: 'Failed to load full list.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e, textOverride = null) => {
    if (e) e.preventDefault();
    const query = (textOverride || input).trim();
    if (!query || loading) return;

    // Handle "Show full list" action from button
    if (query.startsWith('__FULL_LIST__:')) {
      const filterKey = query.replace('__FULL_LIST__:', '');
      await fetchFullList(filterKey);
      return;
    }

    setInput('');
    const newUserMessage = { role: 'user', content: query };
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const response = await aiAPI.chat({ 
        query: query,
        history: messages.map(m => ({ role: m.role, content: m.content }))
      });
      
      let aiResponse = response.data.response || "I couldn't process that request.";
      const metadata = response.data.metadata || {};
      const hasMore = metadata.has_more;
      const total = metadata.total;
      const filterKey = metadata.filter_key;

      const newAiMessage = { 
        role: 'system', 
        content: aiResponse, 
        timestamp: new Date().toISOString(),
        hasMore: hasMore,
        total: total,
        filterKey: filterKey,
      };

      const finalMessages = [...updatedMessages, newAiMessage];
      
      setMessages(finalMessages);
      setSessions(prev => prev.map(s => s.id === currentSessionId ? {
        ...s,
        title: s.title === 'New Chat' ? query.substring(0, 30) : s.title,
        messages: finalMessages
      } : s));
    } catch (error) {
      if (error.response?.status === 401) {
        window.location.href = '/login';
        return;
      }
      const errorMsg = error.response?.data?.detail || error.message || "Unknown error";
      setMessages(prev => [...prev, { role: 'system', content: `⚠️ **AI Error:** ${errorMsg}\n\nPlease try again shortly, or rephrase your query.` }]);
    } finally {
      setLoading(false);
    }
  };



  return (
    <div className="flex h-full w-full bg-[var(--bg-primary)] overflow-hidden rounded-3xl border border-[var(--border-color)] shadow-2xl">
      {/* Sidebar */}
      <div className="w-64 border-r border-[var(--border-color)] bg-[var(--card-bg)] flex flex-col shrink-0">
        <div className="p-4 border-b border-[var(--border-color)]">
          <button 
            onClick={createNewSession}
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-[var(--accent-color)] text-white font-black text-[10px] uppercase tracking-wider shadow-lg hover:opacity-90 active:scale-95 transition-all"
          >
            <Plus className="w-4 h-4" />
            New Session
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2 custom-scroll">
          {sessions.map(session => (
            <div 
              key={session.id}
              onClick={() => loadSession(session.id)}
              className={`group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all ${
                currentSessionId === session.id ? 'bg-[var(--accent-color)]/10 text-[var(--accent-color)]' : 'text-[var(--text-secondary)] hover:bg-[var(--hover-color)]'
              }`}
            >
              <div className="flex items-center gap-2 truncate">
                <MessageSquare className="w-3.5 h-3.5 shrink-0 opacity-50" />
                <span className="text-xs font-bold truncate tracking-tight">{session.title}</span>
              </div>
              <button onClick={(e) => deleteSession(session.id, e)} className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-500">
                 <Trash2 className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Space */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scroll">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] rounded-2xl p-4 flex gap-4 ${
                msg.role === 'user' ? 'bg-[var(--accent-color)] text-white shadow-lg' : 'bg-[var(--card-bg)] border border-[var(--border-color)] text-[var(--text-primary)]'
              }`}>
                <div className="mt-1 shrink-0">
                  {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5 text-[var(--accent-color)]" />}
                </div>
                <div className="flex-1 min-w-0">
                   <SafeContent 
                     content={msg.content} 
                     isUser={msg.role === 'user'} 
                     onAction={(cmd) => handleSubmit(null, cmd)} 
                     filterKey={msg.filterKey}
                     total={msg.total}
                     hasMore={msg.hasMore}
                   />

                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-2xl p-4 flex items-center gap-3">
                <Loader2 className="w-4 h-4 animate-spin text-[var(--accent-color)]" />
                <span className="text-[10px] font-black opacity-40 uppercase tracking-widest">Analysing Data...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-6 border-t border-[var(--border-color)] bg-[var(--card-bg)]/50 backdrop-blur-xl">
          {messages.length <= 1 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {SUGGESTIONS.map((s, i) => (
                <button 
                  key={i}
                  onClick={() => handleSubmit(null, s)}
                  className="px-3 py-1.5 rounded-lg border border-[var(--border-color)] bg-[var(--bg-primary)] text-[11px] font-bold text-[var(--text-secondary)] hover:border-[var(--accent-color)]/50 transition-all active:scale-95"
                >
                  {s}
                </button>
              ))}
            </div>
          )}
          <form onSubmit={handleSubmit} className="flex items-center gap-2 bg-[var(--bg-primary)] border border-[var(--border-color)] rounded-2xl p-2 focus-within:border-[var(--accent-color)] shadow-xl">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              className="flex-1 bg-transparent px-4 py-3 text-sm font-medium focus:outline-none"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-3 bg-[var(--accent-color)] text-white rounded-xl disabled:opacity-20 active:scale-95 transition-all shadow-md"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;

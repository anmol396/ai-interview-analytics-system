// About.jsx
import React from 'react';
import {
  BarChart, Bot, Trophy, ArrowDown, ArrowRight, Activity,
  Github, Linkedin, Mail, Database, Code, Cpu, Workflow,
  Brain, MessageSquare, Server, Layers, Globe, Cloud, FileJson, Monitor
} from 'lucide-react';

const gradients = {
  violetIndigo: {
    bg: "bg-gradient-to-br from-violet-500/10 to-indigo-500/10 dark:from-[#2a1744]/90 dark:to-[#1a1744]/90",
    border: "border-violet-500/25 dark:border-violet-500/30 hover:border-violet-500/50",
    text: "text-violet-700 dark:text-violet-400",
    icon: "text-violet-600 dark:text-violet-400",
    badge: "bg-gradient-to-r from-violet-500/20 to-indigo-500/20 text-violet-700 dark:bg-violet-500/20 dark:text-violet-300",
    shadow: "shadow-[0_4px_20px_rgba(139,92,246,0.1)] dark:shadow-[0_4px_20px_rgba(139,92,246,0.15)]",
    arrow: "text-violet-500 dark:text-violet-500/70"
  },
  blueCyan: {
    bg: "bg-gradient-to-br from-blue-500/10 to-cyan-500/10 dark:from-[#1b264b]/90 dark:to-[#103444]/90",
    border: "border-blue-500/25 dark:border-blue-500/30 hover:border-blue-500/50",
    text: "text-blue-700 dark:text-blue-400",
    icon: "text-blue-600 dark:text-blue-400",
    badge: "bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-700 dark:bg-blue-500/20 dark:text-blue-300",
    shadow: "shadow-[0_4px_20px_rgba(59,130,246,0.1)] dark:shadow-[0_4px_20px_rgba(59,130,246,0.15)]",
    arrow: "text-blue-500 dark:text-blue-500/70"
  },
  cyanTeal: {
    bg: "bg-gradient-to-br from-cyan-500/10 to-teal-500/10 dark:from-[#103444]/90 dark:to-[#0a312f]/90",
    border: "border-cyan-500/25 dark:border-cyan-500/30 hover:border-cyan-500/50",
    text: "text-cyan-700 dark:text-cyan-400",
    icon: "text-cyan-600 dark:text-cyan-400",
    badge: "bg-gradient-to-r from-cyan-500/20 to-teal-500/20 text-cyan-700 dark:bg-cyan-500/20 dark:text-cyan-300",
    shadow: "shadow-[0_4px_20px_rgba(6,182,212,0.1)] dark:shadow-[0_4px_20px_rgba(6,182,212,0.15)]",
    arrow: "text-cyan-500 dark:text-cyan-500/70"
  },
  purplePink: {
    bg: "bg-gradient-to-br from-purple-500/10 to-pink-500/10 dark:from-[#2d1144]/90 dark:to-[#3a1024]/90",
    border: "border-purple-500/25 dark:border-purple-500/30 hover:border-purple-500/50",
    text: "text-purple-700 dark:text-purple-400",
    icon: "text-purple-600 dark:text-purple-400",
    badge: "bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-700 dark:bg-purple-500/20 dark:text-purple-300",
    shadow: "shadow-[0_4px_20px_rgba(168,85,247,0.1)] dark:shadow-[0_4px_20px_rgba(168,85,247,0.15)]",
    arrow: "text-purple-500 dark:text-purple-500/70"
  },
  tealBlue: {
    bg: "bg-gradient-to-br from-teal-500/10 to-blue-500/10 dark:from-[#0a312f]/90 dark:to-[#1b264b]/90",
    border: "border-teal-500/25 dark:border-teal-500/30 hover:border-teal-500/50",
    text: "text-teal-700 dark:text-teal-400",
    icon: "text-teal-600 dark:text-teal-400",
    badge: "bg-gradient-to-r from-teal-500/20 to-blue-500/20 text-teal-700 dark:bg-teal-500/20 dark:text-teal-300",
    shadow: "shadow-[0_4px_20px_rgba(20,184,166,0.1)] dark:shadow-[0_4px_20px_rgba(20,184,166,0.15)]",
    arrow: "text-teal-500 dark:text-teal-500/70"
  },
  orangeMagenta: {
    bg: "bg-gradient-to-br from-orange-500/10 to-fuchsia-500/10 dark:from-[#3a2010]/90 dark:to-[#3a1030]/90",
    border: "border-orange-500/25 dark:border-orange-500/30 hover:border-orange-500/50",
    text: "text-orange-700 dark:text-orange-400",
    icon: "text-orange-600 dark:text-orange-400",
    badge: "bg-gradient-to-r from-orange-500/20 to-fuchsia-500/20 text-orange-700 dark:bg-orange-500/20 dark:text-orange-300",
    shadow: "shadow-[0_4px_20px_rgba(249,115,22,0.1)] dark:shadow-[0_4px_20px_rgba(249,115,22,0.15)]",
    arrow: "text-orange-500 dark:text-orange-500/70"
  },
  pinkViolet: {
    bg: "bg-gradient-to-br from-pink-500/10 to-violet-500/10 dark:from-[#3a1024]/90 dark:to-[#2a1744]/90",
    border: "border-pink-500/25 dark:border-pink-500/30 hover:border-pink-500/50",
    text: "text-pink-700 dark:text-pink-400",
    icon: "text-pink-600 dark:text-pink-400",
    badge: "bg-gradient-to-r from-pink-500/20 to-violet-500/20 text-pink-700 dark:bg-pink-500/20 dark:text-pink-300",
    shadow: "shadow-[0_4px_20px_rgba(236,72,153,0.1)] dark:shadow-[0_4px_20px_rgba(236,72,153,0.15)]",
    arrow: "text-pink-500 dark:text-pink-500/70"
  },
  indigoBlue: {
    bg: "bg-gradient-to-br from-indigo-500/10 to-blue-500/10 dark:from-[#1c1844]/90 dark:to-[#1b264b]/90",
    border: "border-indigo-500/25 dark:border-indigo-500/30 hover:border-indigo-500/50",
    text: "text-indigo-700 dark:text-indigo-400",
    icon: "text-indigo-600 dark:text-indigo-400",
    badge: "bg-gradient-to-r from-indigo-500/20 to-blue-500/20 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-300",
    shadow: "shadow-[0_4px_20px_rgba(99,102,241,0.1)] dark:shadow-[0_4px_20px_rgba(99,102,241,0.15)]",
    arrow: "text-indigo-500 dark:text-indigo-500/70"
  },
  emeraldTeal: {
    bg: "bg-gradient-to-br from-emerald-500/10 to-teal-500/10 dark:from-[#0a3118]/90 dark:to-[#0a312f]/90",
    border: "border-emerald-500/25 dark:border-emerald-500/30 hover:border-emerald-500/50",
    text: "text-emerald-700 dark:text-emerald-400",
    icon: "text-emerald-600 dark:text-emerald-400",
    badge: "bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300",
    shadow: "shadow-[0_4px_20px_rgba(16,185,129,0.1)] dark:shadow-[0_4px_20px_rgba(16,185,129,0.15)]",
    arrow: "text-emerald-500 dark:text-emerald-500/70"
  },
  orangeAmber: {
    bg: "bg-gradient-to-br from-orange-500/10 to-amber-500/10 dark:from-[#3a2010]/90 dark:to-[#3a2a10]/90",
    border: "border-orange-500/25 dark:border-orange-500/30 hover:border-orange-500/50",
    text: "text-orange-700 dark:text-orange-400",
    icon: "text-orange-600 dark:text-orange-400",
    badge: "bg-gradient-to-r from-orange-500/20 to-amber-500/20 text-orange-700 dark:bg-orange-500/20 dark:text-orange-300",
    shadow: "shadow-[0_4px_20px_rgba(249,115,22,0.1)] dark:shadow-[0_4px_20px_rgba(249,115,22,0.15)]",
    arrow: "text-orange-500 dark:text-orange-500/70"
  },
  roseMagenta: {
    bg: "bg-gradient-to-br from-rose-500/10 to-fuchsia-500/10 dark:from-[#3a101a]/90 dark:to-[#3a1030]/90",
    border: "border-rose-500/25 dark:border-rose-500/30 hover:border-rose-500/50",
    text: "text-rose-700 dark:text-rose-400",
    icon: "text-rose-600 dark:text-rose-400",
    badge: "bg-gradient-to-r from-rose-500/20 to-fuchsia-500/20 text-rose-700 dark:bg-rose-500/20 dark:text-rose-300",
    shadow: "shadow-[0_4px_20px_rgba(225,29,72,0.1)] dark:shadow-[0_4px_20px_rgba(225,29,72,0.15)]",
    arrow: "text-rose-500 dark:text-rose-500/70"
  },
  violetCyan: {
    bg: "bg-gradient-to-br from-violet-500/10 to-cyan-500/10 dark:from-[#2a1744]/90 dark:to-[#103444]/90",
    border: "border-violet-500/25 dark:border-cyan-500/30 hover:border-cyan-500/50",
    text: "text-cyan-700 dark:text-cyan-400",
    icon: "text-cyan-600 dark:text-cyan-400",
    badge: "bg-gradient-to-r from-violet-500/20 to-cyan-500/20 text-cyan-700 dark:bg-cyan-500/20 dark:text-cyan-300",
    shadow: "shadow-[0_4px_20px_rgba(6,182,212,0.1)] dark:shadow-[0_4px_20px_rgba(6,182,212,0.15)]",
    arrow: "text-cyan-500 dark:text-cyan-500/70"
  },
  violetPink: {
    bg: "bg-gradient-to-br from-violet-500/10 to-pink-500/10 dark:from-[#2a1744]/90 dark:to-[#3a1024]/90",
    border: "border-violet-500/25 dark:border-pink-500/30 hover:border-pink-500/50",
    text: "text-pink-700 dark:text-pink-400",
    icon: "text-pink-600 dark:text-pink-400",
    badge: "bg-gradient-to-r from-violet-500/20 to-pink-500/20 text-pink-700 dark:bg-pink-500/20 dark:text-pink-300",
    shadow: "shadow-[0_4px_20px_rgba(236,72,153,0.1)] dark:shadow-[0_4px_20px_rgba(236,72,153,0.15)]",
    arrow: "text-pink-500 dark:text-pink-500/70"
  }
};

const PipelineConnector = ({ label, fromColor, toColor, textColor, borderColor, horizontal = false, final = false }) => {
  if (horizontal) {
    return (
      <div className="flex flex-col md:flex-row items-center justify-center p-2 md:p-0 md:px-2 relative z-0 flex-shrink-0 min-h-[40px] md:min-w-[40px]">
        <div className={`hidden md:block absolute left-0 right-0 h-1.5 bg-gradient-to-r ${fromColor} ${toColor} opacity-70 rounded-full top-1/2 -translate-y-1/2`}></div>
        <div className={`md:hidden absolute top-0 bottom-0 w-1.5 bg-gradient-to-b ${fromColor} ${toColor} opacity-70 rounded-full left-1/2 -translate-x-1/2`}></div>

        {!final && (
          <div className={`px-2 py-1 md:px-3 md:py-1.5 rounded-full border bg-white/95 dark:bg-[#1E0F3A]/95 flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-[0.1em] shadow-md z-10 relative whitespace-nowrap ${textColor} ${borderColor}`}>
            {label}
            <ArrowRight size={12} className="animate-pulse hidden md:block" />
            <ArrowDown size={12} className="animate-pulse md:hidden" />
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center py-6 relative w-full z-0">
      <div className={`absolute top-0 bottom-0 w-1.5 bg-gradient-to-b ${fromColor} ${toColor} opacity-70 rounded-full`}></div>
      {!final && (
        <div className={`px-4 py-1.5 rounded-full border bg-white/95 dark:bg-[#1E0F3A]/95 flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] shadow-md z-10 relative ${textColor} ${borderColor}`}>
          {label} <ArrowDown size={14} className="animate-pulse" />
        </div>
      )}
    </div>
  );
};

const PipelineCard = ({ step, title, desc, icon: Icon, colorTheme, nested = false }) => (
  <div className={`flex-shrink-0 w-full md:w-auto ${nested ? 'min-w-[200px]' : 'min-w-[220px] max-w-[280px]'} rounded-3xl p-5 md:p-6 ${colorTheme.bg} border ${colorTheme.border} ${colorTheme.shadow} flex flex-col items-center text-center transition-all duration-300 backdrop-blur-md relative z-10 hover:-translate-y-1 h-full`}>
    <div className={`mb-3 px-3 py-1 rounded-full ${colorTheme.badge} text-[10px] md:text-[11px] font-bold tracking-widest whitespace-nowrap`}>
      {step}
    </div>
    <div className={`mb-3 ${colorTheme.icon}`}>
      <Icon size={28} className="md:w-8 md:h-8" />
    </div>
    <h3 className="text-lg md:text-xl font-bold text-slate-900 dark:text-white mb-2 leading-tight">{title}</h3>
    <p className="text-slate-600 dark:text-[#BFAEFF] text-[13px] md:text-[14px] font-medium leading-relaxed">{desc}</p>
  </div>
);

const ArchCard = ({ layer, title, desc, icon: Icon, pills, colorTheme }) => (
  <div className={`w-full max-w-[700px] rounded-3xl p-8 ${colorTheme.bg} border ${colorTheme.border} ${colorTheme.shadow} flex flex-col items-center text-center transition-all duration-300 backdrop-blur-md relative z-10 hover:-translate-y-1`}>
    <div className={`mb-4 ${colorTheme.icon}`}>
      <Icon size={36} />
    </div>
    <div className={`mb-4 px-4 py-1.5 rounded-full ${colorTheme.badge} text-[11px] font-bold tracking-widest`}>
      {layer}
    </div>
    <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">{title}</h3>
    <p className="text-slate-600 dark:text-[#BFAEFF] text-[15px] font-medium mb-8 leading-relaxed">{desc}</p>

    <div className="flex flex-wrap justify-center gap-3">
      {pills.map((pill, idx) => (
        <span key={idx} className={`px-4 py-2 rounded-xl bg-white/40 dark:bg-black/30 ${colorTheme.text} text-sm font-semibold border border-white/50 dark:border-white/10 backdrop-blur-sm shadow-sm`}>
          {pill}
        </span>
      ))}
    </div>
  </div>
);

const SectionHeader = ({ icon: Icon, title, subtitle }) => (
  <div className="flex flex-col items-center mb-16 text-center">
    <h2 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3 mb-4">
      <Icon className="text-violet-600 dark:text-[#8B5CF6]" size={32} />
      {title}
    </h2>
    {subtitle && (
      <p className="text-slate-600 dark:text-[#BFAEFF] max-w-xl text-lg">{subtitle}</p>
    )}
    <div className="w-full max-w-[240px] h-px bg-gradient-to-r from-transparent via-violet-400/50 dark:via-purple-500/50 to-transparent mt-8"></div>
  </div>
);

const About = () => {
  return (
    <div className="w-full min-h-full overflow-hidden bg-gradient-to-b from-slate-50 to-slate-100 dark:from-[#160B2E] dark:to-[#1E0F3A] text-slate-900 dark:text-[#F3F0FF] custom-scroll transition-colors duration-300">

      {/* 1. HERO SECTION */}
      <section className="pt-24 pb-8">
        <div className="text-center max-w-2xl mx-auto px-6 space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-[1.2] pb-2 bg-gradient-to-r from-violet-600 to-purple-500 dark:from-purple-400 dark:to-purple-300 bg-clip-text text-transparent">
            HR Analytics
          </h1>
          <p className="text-2xl font-bold text-slate-800 dark:text-white tracking-wide">
            Data-driven hiring made intelligent.
          </p>
          <p className="text-slate-600 dark:text-[#BFAEFF] max-w-lg mx-auto leading-relaxed text-center">
            Empower your recruitment process with cutting-edge analytics,<br />
            real-time insights, and AI.
          </p>

          <div className="flex justify-center gap-3 mt-4 flex-wrap text-sm font-semibold text-violet-700 dark:text-purple-300">
            <span className="px-4 py-2 rounded-full bg-violet-100 dark:bg-purple-500/10 border border-violet-200 dark:border-purple-500/20">5000+ Candidates</span>
            <span className="hidden sm:inline pt-1.5 opacity-50">&bull;</span>
            <span className="px-4 py-2 rounded-full bg-violet-100 dark:bg-purple-500/10 border border-violet-200 dark:border-purple-500/20">AI Powered</span>
            <span className="hidden sm:inline pt-1.5 opacity-50">&bull;</span>
            <span className="px-4 py-2 rounded-full bg-violet-100 dark:bg-purple-500/10 border border-violet-200 dark:border-purple-500/20">Real-time Insights</span>
          </div>
        </div>
      </section>

      {/* 2. FEATURES */}
      <section className="py-20 mt-[120px] bg-violet-50/80 dark:bg-[#1f113a]/50 border-y border-violet-100 dark:border-white/5">
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeader
            icon={Trophy}
            title="Core Capabilities"
            subtitle="Intelligent tools to streamline your hiring process."
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "Analyze Candidates", icon: BarChart, desc: "Process thousands of applicant profiles instantly with semantic understanding." },
              { title: "AI Assistant", icon: Bot, desc: "Interact with your data naturally through our advanced generative AI interface." },
              { title: "Smart Ranking", icon: Trophy, desc: "Automatically prioritize top talent based on comprehensive multidimensional scoring." }
            ].map((feature, i) => (
              <div key={i} className="flex flex-col p-8 rounded-3xl bg-white/60 dark:bg-[#22123A]/60 backdrop-blur-md border border-violet-200 dark:border-[#8B5CF6]/20 transition-all duration-300 hover:scale-105 shadow-sm hover:shadow-lg dark:shadow-none dark:hover:shadow-[0_15px_40px_rgba(139,92,246,0.15)] hover:border-violet-400 dark:hover:border-[#8B5CF6]/40 cursor-default group">
                <div className="w-14 h-14 rounded-2xl bg-violet-50 dark:bg-[#160B2E] border border-violet-200 dark:border-[#8B5CF6]/30 flex items-center justify-center mb-6 shadow-inner group-hover:bg-violet-100 dark:group-hover:bg-[#8B5CF6]/10 transition-colors">
                  <feature.icon className="w-7 h-7 text-violet-600 dark:text-purple-400" />
                </div>
                <h3 className="font-bold text-xl text-slate-900 dark:text-white mb-3">{feature.title}</h3>
                <p className="text-slate-600 dark:text-[#BFAEFF] leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 3. SYSTEM ARCHITECTURE */}
      <section className="py-20 mt-[180px] bg-indigo-100/30 dark:bg-[#140826]/80 border-y border-indigo-200 dark:border-white/5">
        <div className="max-w-[1100px] mx-auto px-6">
          <SectionHeader
            icon={Workflow}
            title="System Architecture"
            subtitle="Implementation-driven architecture of the platform."
          />
          <div className="flex flex-col items-center mx-auto w-full relative">
            <ArchCard
              layer="LAYER 1" title="Presentation Layer" desc="React + Vite Frontend"
              icon={Globe} pills={["Login/Signup", "Dashboard", "AI Assistant"]}
              colorTheme={gradients.violetIndigo}
            />

            <PipelineConnector
              label="HTTP Requests" fromColor="from-indigo-500" toColor="to-blue-500"
              textColor="text-blue-700 dark:text-blue-400" borderColor="border-blue-500/30"
            />

            <ArchCard
              layer="LAYER 2" title="API Layer" desc="FastAPI Backend"
              icon={Server} pills={["Auth Routes", "Candidate Routes", "Dashboard API", "Chat Endpoints"]}
              colorTheme={gradients.blueCyan}
            />

            <PipelineConnector
              label="QUERY PROCESSING" fromColor="from-cyan-500" toColor="to-purple-500"
              textColor="text-purple-700 dark:text-purple-400" borderColor="border-purple-500/30"
            />

            <ArchCard
              layer="LAYER 3" title="Processing Layer" desc="Core Logic"
              icon={Layers} pills={["JWT Auth", "Intent Classifier", "DB Handler", "AI Router"]}
              colorTheme={gradients.purplePink}
            />

            <PipelineConnector
              label="SQL Queries" fromColor="from-pink-500" toColor="to-orange-500"
              textColor="text-orange-700 dark:text-orange-400" borderColor="border-orange-500/30"
            />

            <ArchCard
              layer="LAYER 4" title="Data Layer" desc="MySQL + SQLAlchemy"
              icon={Database} pills={["Candidates Table", "Users Table"]}
              colorTheme={gradients.orangeAmber}
            />

            <PipelineConnector
              label="LLM Calls" fromColor="from-amber-500" toColor="to-rose-500"
              textColor="text-rose-700 dark:text-rose-400" borderColor="border-rose-500/30"
            />

            <ArchCard
              layer="LAYER 5" title="LLM Layer" desc="External Services"
              icon={Cloud} pills={["Groq API", "Google Gemini", "Fallback Logic"]}
              colorTheme={gradients.roseMagenta}
            />
          </div>
        </div>
      </section>

      {/* 4. DATA PIPELINE */}
      <section className="py-20 mt-[180px] mb-[140px] bg-purple-50/60 dark:bg-[#261545]/60 border-y border-purple-100 dark:border-white/5 overflow-hidden">
        <div className="max-w-[1600px] mx-auto px-4 md:px-8">
          <SectionHeader
            icon={Activity}
            title="Data Pipeline"
            subtitle="How AI requests are processed through the platform."
          />

          <div className="flex flex-col md:flex-row flex-wrap justify-center items-stretch mx-auto w-full relative gap-y-4 md:gap-y-8">

            <PipelineCard
              step="01" title="User Input" desc="User types query in chat interface"
              icon={MessageSquare} colorTheme={gradients.violetIndigo}
            />
            <PipelineConnector
              horizontal={true} label="Request" fromColor="from-indigo-500" toColor="to-blue-500"
              textColor="text-blue-700 dark:text-blue-400" borderColor="border-blue-500/30"
            />

            <PipelineCard
              step="02" title="Frontend Processing" desc="Axios POST /chat with Bearer token"
              icon={Code} colorTheme={gradients.blueCyan}
            />
            <PipelineConnector
              horizontal={true} label="Validate" fromColor="from-cyan-500" toColor="to-cyan-500"
              textColor="text-cyan-700 dark:text-cyan-400" borderColor="border-cyan-500/30"
            />

            <PipelineCard
              step="03" title="API Processing" desc="Authentication + Query Preprocessing"
              icon={Server} colorTheme={gradients.cyanTeal}
            />
            <PipelineConnector
              horizontal={true} label="Process" fromColor="from-teal-500" toColor="to-purple-500"
              textColor="text-purple-700 dark:text-purple-400" borderColor="border-purple-500/30"
            />

            <PipelineCard
              step="04" title="Intent Classification" desc="Rule-based classifier (15+ intents)"
              icon={Brain} colorTheme={gradients.purplePink}
            />
            <PipelineConnector
              horizontal={true} label="Classify" fromColor="from-pink-500" toColor="to-violet-500"
              textColor="text-violet-700 dark:text-violet-400" borderColor="border-violet-500/30"
            />

            {/* Split Path (05A/05B) */}
            <div className={`flex-shrink-0 w-full md:w-auto flex flex-col items-center rounded-3xl p-4 md:p-6 bg-gradient-to-br from-violet-500/10 to-indigo-500/10 dark:from-violet-500/10 dark:to-indigo-500/10 border border-violet-500/20 dark:border-violet-500/20 backdrop-blur-md relative z-10 shadow-sm h-full`}>
              <div className="mb-4 px-4 py-1.5 rounded-full bg-gradient-to-r from-violet-500/20 to-indigo-500/20 text-violet-800 dark:text-violet-300 text-[11px] font-bold tracking-widest uppercase border border-violet-500/20 whitespace-nowrap">
                05 Split Execution
              </div>
              <div className="flex flex-col sm:flex-row gap-4 w-full h-full">
                <PipelineCard step="05A" title="SQL Path" desc="Intent → SQL → MySQL" icon={Database} colorTheme={gradients.violetCyan} nested={true} />
                <PipelineCard step="05B" title="AI Path" desc="GENERAL intent → LLMs" icon={Cpu} colorTheme={gradients.violetPink} nested={true} />
              </div>
            </div>

            <PipelineConnector
              horizontal={true} label="Retrieve" fromColor="from-indigo-500" toColor="to-pink-500"
              textColor="text-pink-700 dark:text-pink-400" borderColor="border-pink-500/30"
            />

            <PipelineCard
              step="06" title="Response Generation" desc="Combine Results + Generate Insight"
              icon={Layers} colorTheme={gradients.pinkViolet}
            />
            <PipelineConnector
              horizontal={true} label="Generate" fromColor="from-violet-500" toColor="to-indigo-500"
              textColor="text-indigo-700 dark:text-indigo-400" borderColor="border-indigo-500/30"
            />

            <PipelineCard
              step="07" title="JSON Response" desc="Format payload with metadata"
              icon={FileJson} colorTheme={gradients.indigoBlue}
            />
            <PipelineConnector
              horizontal={true} label="Format" fromColor="from-blue-500" toColor="to-emerald-500"
              textColor="text-emerald-700 dark:text-emerald-400" borderColor="border-emerald-500/30"
            />

            <PipelineCard
              step="08" title="View Results" desc="See Insights and answers"
              icon={Monitor} colorTheme={gradients.emeraldTeal}
            />

          </div>
        </div>
      </section>

      {/* 5. FOOTER */}
      <footer className="pt-8 pb-16 border-t border-violet-200 dark:border-[#8B5CF6]/20 flex flex-col items-center gap-6">
        <div className="flex gap-12 justify-center w-full">
          <div className="text-center">
            <p className="text-sm font-semibold text-slate-900 dark:text-[#F3F0FF]">Anmol Chawla</p>
            <div className="flex justify-center gap-4 mt-3 text-slate-500 dark:text-gray-400">
              <a href="https://github.com/anmol396" target="_blank" rel="noopener noreferrer" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 hover:text-slate-900 dark:hover:text-white transition">
                <Github size={18} />
              </a>
              <a href="https://www.linkedin.com/in/anmol-chawla-b079672b6/" target="_blank" rel="noopener noreferrer" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 hover:text-slate-900 dark:hover:text-white transition">
                <Linkedin size={18} />
              </a>
              <a href="mailto:anmolai907@gmail.com" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 hover:text-slate-900 dark:hover:text-white transition">
                <Mail size={18} />
              </a>
            </div>
          </div>

          <div className="text-center">
            <p className="text-sm font-semibold text-slate-900 dark:text-[#F3F0FF]">Drashti Rajgor</p>
            <div className="flex justify-center gap-4 mt-3 text-slate-500 dark:text-gray-400">
              <a href="https://github.com/DrashtiRaj" target="_blank" rel="noopener noreferrer" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 hover:text-slate-900 dark:hover:text-white transition">
                <Github size={18} />
              </a>
              <a href="https://www.linkedin.com/in/drashti-r-3437a73b3/" target="_blank" rel="noopener noreferrer" className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 hover:text-slate-900 dark:hover:text-white transition">
                <Linkedin size={18} />
              </a>
            </div>
          </div>
        </div>

        <div className="text-center text-sm text-slate-500 dark:text-gray-500 w-full mt-4">
          © 2026 HR Analytics. All rights reserved.
        </div>
      </footer>

    </div>
  );
};

export default About;

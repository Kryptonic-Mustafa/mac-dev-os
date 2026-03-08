"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { Activity, FolderKanban, MessageSquare, Cpu, Terminal } from 'lucide-react';

interface StatsProps {
  stats: {
    projects: number;
    messages: number;
    unread: number;
  };
}

export default function DashboardUI({ stats }: StatsProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Stagger in the header and cards
    gsap.from(".dash-el", {
      y: 20,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: "power3.out",
    });

    // Animate the numbers counting up
    const numbers = document.querySelectorAll('.stat-number');
    numbers.forEach((el) => {
      const target = parseFloat(el.getAttribute('data-val') || '0');
      gsap.to(el, {
        innerHTML: target,
        duration: 2,
        snap: { innerHTML: 1 },
        ease: "power2.out",
      });
    });
  }, { scope: containerRef });

  return (
    <div ref={containerRef} className="w-full flex flex-col gap-10">
      
      {/* Dashboard Header */}
      <div className="dash-el flex flex-col gap-2">
        <h1 className="text-3xl md:text-4xl font-display font-medium tracking-tight text-foreground">
          System Overview
        </h1>
        <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest">
          Primary Telemetry & Status Logs
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Projects Card */}
        <div className="dash-el bg-background border border-foreground/10 p-6 relative overflow-hidden group hover:border-primary/30 transition-colors">
          <div className="absolute top-0 right-0 p-6 opacity-5">
            <FolderKanban className="w-32 h-32" />
          </div>
          <div className="relative z-10 flex flex-col gap-4">
            <div className="p-3 bg-primary/10 w-max rounded border border-primary/20 text-primary">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="font-mono text-xs text-foreground/50 uppercase tracking-widest mb-1">Active Projects</div>
              <div className="text-4xl font-display text-foreground stat-number" data-val={stats.projects}>0</div>
            </div>
          </div>
        </div>

        {/* Messages Card */}
        <div className="dash-el bg-background border border-foreground/10 p-6 relative overflow-hidden group hover:border-primary/30 transition-colors">
          <div className="absolute top-0 right-0 p-6 opacity-5">
            <MessageSquare className="w-32 h-32" />
          </div>
          <div className="relative z-10 flex flex-col gap-4">
            <div className="p-3 bg-primary/10 w-max rounded border border-primary/20 text-primary">
              <MessageSquare className="w-5 h-5" />
            </div>
            <div>
              <div className="font-mono text-xs text-foreground/50 uppercase tracking-widest mb-1">Total Comm Links</div>
              <div className="text-4xl font-display text-foreground stat-number" data-val={stats.messages}>0</div>
            </div>
          </div>
        </div>

        {/* Unread Alerts Card */}
        <div className="dash-el bg-background border border-foreground/10 p-6 relative overflow-hidden group hover:border-red-500/30 transition-colors">
          <div className="absolute top-0 right-0 p-6 opacity-5">
            <Cpu className="w-32 h-32" />
          </div>
          <div className="relative z-10 flex flex-col gap-4">
            <div className={`p-3 w-max rounded border ${stats.unread > 0 ? 'bg-red-500/10 border-red-500/20 text-red-500' : 'bg-primary/10 border-primary/20 text-primary'}`}>
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="font-mono text-xs text-foreground/50 uppercase tracking-widest mb-1">Unread Transmissions</div>
              <div className={`text-4xl font-display stat-number ${stats.unread > 0 ? 'text-red-500' : 'text-foreground'}`} data-val={stats.unread}>0</div>
            </div>
          </div>
        </div>

      </div>

      {/* Terminal Output Mock */}
      <div className="dash-el mt-8 bg-black/50 border border-foreground/10 p-6 font-mono text-xs text-primary/70 leading-relaxed shadow-inner">
        <div className="flex items-center gap-2 mb-4 text-foreground/30 border-b border-foreground/10 pb-2">
          <Terminal className="w-4 h-4" />
          <span>macdevos_core.log</span>
        </div>
        <p>&gt; Initiating boot sequence...</p>
        <p>&gt; Checking database integrity... [OK]</p>
        <p>&gt; Fetching matrix configurations... [OK]</p>
        <p>&gt; Establishing secure edge network... [OK]</p>
        <p className="text-emerald-400 mt-2">&gt; SYSTEM FULLY OPERATIONAL.</p>
        <p className="animate-pulse mt-2">_</p>
      </div>

    </div>
  );
}

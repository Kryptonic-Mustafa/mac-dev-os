import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🎛️ M.A.C.DevOS HUD] {message}...")
    time.sleep(0.5)

def deploy_admin_dashboard():
    # 1. Create Logout API Route
    print_status("Engineering Secure Logout Protocol")
    logout_dir = PROJECT_PATH / "src/app/api/admin/logout"
    os.makedirs(logout_dir, exist_ok=True)
    
    logout_content = """import { NextResponse } from 'next/server';

export async function POST() {
  const response = NextResponse.json({ message: 'Comm channel closed.' }, { status: 200 });
  response.cookies.delete('macdevos_token');
  return response;
}
"""
    with open(logout_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write(logout_content)

    # 2. Create the Admin Layout (Sidebar & Wrapper)
    print_status("Constructing Persistent Admin Architecture")
    admin_dir = PROJECT_PATH / "src/app/admin"
    
    layout_content = """"use client";

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Terminal, LayoutDashboard, FolderKanban, MessageSquare, LogOut, Activity } from 'lucide-react';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // Do not apply this layout to the login page itself
  if (pathname === '/admin/login') {
    return <>{children}</>;
  }

  const handleLogout = async () => {
    await fetch('/api/admin/logout', { method: 'POST' });
    router.push('/admin/login');
  };

  const navLinks = [
    { name: 'Dashboard', href: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Matrix (Projects)', href: '/admin/projects', icon: FolderKanban },
    { name: 'Comm Channel', href: '/admin/messages', icon: MessageSquare },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground flex overflow-hidden selection:bg-primary/30">
      
      {/* Sidebar Matrix */}
      <aside className="w-64 border-r border-foreground/10 bg-background/50 backdrop-blur-md hidden md:flex flex-col relative z-20">
        
        {/* Brand Header */}
        <div className="h-20 border-b border-foreground/10 flex items-center px-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-6 h-6 text-primary" />
            <span className="font-display tracking-widest uppercase text-sm font-bold">M.A.C.DevOS</span>
          </div>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 px-4 py-8 flex flex-col gap-2">
          {navLinks.map((link) => {
            const isActive = pathname.startsWith(link.href);
            return (
              <Link 
                key={link.name} 
                href={link.href}
                className={`flex items-center gap-3 px-4 py-3 font-mono text-xs uppercase tracking-widest transition-all duration-300 border-l-2 ${
                  isActive 
                    ? 'border-primary bg-primary/10 text-primary' 
                    : 'border-transparent text-foreground/50 hover:bg-foreground/5 hover:text-foreground'
                }`}
              >
                <link.icon className="w-4 h-4" />
                {link.name}
              </Link>
            );
          })}
        </nav>

        {/* System Status & Logout */}
        <div className="p-4 border-t border-foreground/10">
          <div className="flex items-center gap-2 mb-6 px-4">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-mono text-[10px] text-foreground/40 uppercase tracking-widest">System Online</span>
          </div>
          
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 font-mono text-xs uppercase tracking-widest text-red-500/70 hover:bg-red-500/10 hover:text-red-500 transition-colors border border-transparent hover:border-red-500/20"
          >
            <LogOut className="w-4 h-4" />
            Disconnect
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 relative overflow-y-auto">
        {/* Top Mobile Bar (Hidden on Desktop) */}
        <div className="h-16 border-b border-foreground/10 bg-background/80 backdrop-blur-md md:hidden flex items-center justify-between px-6 sticky top-0 z-30">
          <Terminal className="w-5 h-5 text-primary" />
          <button onClick={handleLogout} className="text-red-500/70 hover:text-red-500">
            <LogOut className="w-5 h-5" />
          </button>
        </div>

        {/* Content Injection Point */}
        <div className="p-6 md:p-10 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
"""
    with open(admin_dir / "layout.tsx", "w", encoding="utf-8") as f:
        f.write(layout_content)

    # 3. Create the Server Component for the Dashboard (Fetches Data)
    print_status("Wiring Telemetry Data Link to MySQL")
    dashboard_dir = PROJECT_PATH / "src/app/admin/dashboard"
    os.makedirs(dashboard_dir, exist_ok=True)
    
    server_page_content = """import { db } from '@/lib/db';
import DashboardUI from './DashboardUI';

// Force dynamic rendering so stats are always fresh
export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  // Fetch live telemetry from MySQL
  const projectCount = await db.project.count();
  const messageCount = await db.message.count();
  const unreadMessages = await db.message.count({ where: { isRead: false } });

  const stats = {
    projects: projectCount,
    messages: messageCount,
    unread: unreadMessages,
  };

  return <DashboardUI stats={stats} />;
}
"""
    with open(dashboard_dir / "page.tsx", "w", encoding="utf-8") as f:
        f.write(server_page_content)

    # 4. Create the Client Component for the Dashboard (GSAP Animations)
    print_status("Rendering Cinematic UI Graphics")
    
    client_ui_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { Activity, FolderKanban, MessageSquare, Cpu } from 'lucide-react';

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
"""
    with open(dashboard_dir / "DashboardUI.tsx", "w", encoding="utf-8") as f:
        f.write(client_ui_content)

    print_status("Command Center HUD deployed.")

if __name__ == "__main__":
    deploy_admin_dashboard()
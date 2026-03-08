import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🎛️ M.A.C.DevOS OS] {message}...")
    time.sleep(0.5)

def deploy_admin_suite():
    # ---------------------------------------------------------
    # 1. FIX THE ROUTING & LAYOUT OVERLAP
    # ---------------------------------------------------------
    print_status("Patching Routing and Layout Overlap Bugs")
    
    # Update Middleware for /admin redirect
    middleware_path = PROJECT_PATH / "src/middleware.ts"
    middleware_content = """import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Auto-redirect root admin to dashboard
  if (pathname === '/admin') {
    return NextResponse.redirect(new URL('/admin/dashboard', request.url));
  }

  // Only protect /admin routes, but allow access to the login page
  if (pathname.startsWith('/admin') && !pathname.startsWith('/admin/login')) {
    const token = request.cookies.get('macdevos_token')?.value;

    if (!token) {
      return NextResponse.redirect(new URL('/admin/login', request.url));
    }

    try {
      const secret = new TextEncoder().encode(process.env.JWT_SECRET);
      await jwtVerify(token, secret);
      return NextResponse.next();
    } catch (error) {
      const response = NextResponse.redirect(new URL('/admin/login', request.url));
      response.cookies.delete('macdevos_token');
      return response;
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*'],
};
"""
    with open(middleware_path, "w", encoding="utf-8") as f:
        f.write(middleware_content)

    # Update Global CSS to hide frontend header in admin mode
    css_path = PROJECT_PATH / "src/app/globals.css"
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("\n\n/* ADMIN MODE ISOLATION */\nhtml.admin-mode header, html.admin-mode footer, html.admin-mode nav.fixed { display: none !important; }\n")

    # Update Admin Layout to trigger isolation mode and fix margins
    layout_path = PROJECT_PATH / "src/app/admin/layout.tsx"
    layout_content = """"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Terminal, LayoutDashboard, FolderKanban, MessageSquare, LogOut } from 'lucide-react';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // ISOLATION LOCK: Hide frontend navbar when in admin routes
  useEffect(() => {
    document.documentElement.classList.add('admin-mode');
    return () => document.documentElement.classList.remove('admin-mode');
  }, []);

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
        <div className="h-20 border-b border-foreground/10 flex items-center px-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-6 h-6 text-primary" />
            <span className="font-display tracking-widest uppercase text-sm font-bold">M.A.C.DevOS</span>
          </div>
        </div>

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
            <LogOut className="w-4 h-4" /> Disconnect
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 relative overflow-y-auto">
        <div className="h-16 border-b border-foreground/10 bg-background/80 backdrop-blur-md md:hidden flex items-center justify-between px-6 sticky top-0 z-30">
          <Terminal className="w-5 h-5 text-primary" />
          <button onClick={handleLogout} className="text-red-500/70 hover:text-red-500">
            <LogOut className="w-5 h-5" />
          </button>
        </div>

        {/* Added extra top padding here to ensure it breathes perfectly */}
        <div className="p-6 pt-12 md:p-12 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
"""
    with open(layout_path, "w", encoding="utf-8") as f:
        f.write(layout_content)

    # ---------------------------------------------------------
    # 2. MATRIX CONTROLLER (PROJECTS)
    # ---------------------------------------------------------
    print_status("Engineering Matrix (Projects) Controller")
    
    # API Routes
    os.makedirs(PROJECT_PATH / "src/app/api/admin/projects", exist_ok=True)
    with open(PROJECT_PATH / "src/app/api/admin/projects/route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  const projects = await db.project.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(projects);
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const systemId = `SYS-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
    const project = await db.project.create({
      data: { systemId, title: data.title, description: data.description, tech: data.tech, repoLink: data.repoLink, liveLink: data.liveLink }
    });
    return NextResponse.json(project);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create project' }, { status: 500 });
  }
}
""")

    os.makedirs(PROJECT_PATH / "src/app/api/admin/projects/[id]", exist_ok=True)
    with open(PROJECT_PATH / "src/app/api/admin/projects/[id]/route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  try {
    await db.project.delete({ where: { id: params.id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete' }, { status: 500 });
  }
}
""")

    # UI Files
    os.makedirs(PROJECT_PATH / "src/app/admin/projects", exist_ok=True)
    with open(PROJECT_PATH / "src/app/admin/projects/page.tsx", "w", encoding="utf-8") as f:
        f.write("""import { db } from '@/lib/db';
import ProjectsUI from './ProjectsUI';

export const dynamic = 'force-dynamic';

export default async function ProjectsPage() {
  const projects = await db.project.findMany({ orderBy: { createdAt: 'desc' } });
  return <ProjectsUI initialProjects={projects} />;
}
""")

    with open(PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx", "w", encoding="utf-8") as f:
        f.write(""""use client";
import { useState } from 'react';
import { FolderKanban, Plus, Trash2, Github, ExternalLink } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  const [projects, setProjects] = useState(initialProjects);
  const [isAdding, setIsAdding] = useState(false);

  const handleDelete = async (id: string) => {
    await fetch(`/api/admin/projects/${id}`, { method: 'DELETE' });
    setProjects(projects.filter(p => p.id !== id));
  };

  const handleAdd = async (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    const res = await fetch('/api/admin/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const newProj = await res.json();
    setProjects([newProj, ...projects]);
    setIsAdding(false);
  };

  return (
    <div className="w-full flex flex-col gap-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl md:text-4xl font-display font-medium text-foreground">Deployment Matrix</h1>
          <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Manage Portfolio Assets</p>
        </div>
        <button onClick={() => setIsAdding(!isAdding)} className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary text-primary font-mono text-xs uppercase hover:bg-primary/20 transition-colors">
          <Plus className="w-4 h-4" /> New Deployment
        </button>
      </div>

      {isAdding && (
        <form onSubmit={handleAdd} className="bg-background/50 border border-primary/30 p-6 flex flex-col gap-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input name="title" required placeholder="Project Title" className="bg-foreground/5 border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans" />
            <input name="tech" required placeholder="Tech Stack (e.g. React, Next.js, MySQL)" className="bg-foreground/5 border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans" />
            <input name="repoLink" placeholder="GitHub URL (Optional)" className="bg-foreground/5 border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans" />
            <input name="liveLink" placeholder="Live URL (Optional)" className="bg-foreground/5 border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans" />
          </div>
          <textarea name="description" required placeholder="Project Description..." rows={3} className="bg-foreground/5 border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans resize-none" />
          <div className="flex justify-end gap-3 mt-2">
            <button type="button" onClick={() => setIsAdding(false)} className="px-6 py-2 border border-foreground/20 text-foreground/70 font-mono text-xs uppercase hover:bg-foreground/5">Cancel</button>
            <button type="submit" className="px-6 py-2 bg-primary text-background font-mono text-xs uppercase font-bold hover:shadow-[0_0_15px_var(--color-primary)] transition-shadow">Deploy Asset</button>
          </div>
        </form>
      )}

      <div className="grid grid-cols-1 gap-4">
        {projects.map(proj => (
          <div key={proj.id} className="bg-background border border-foreground/10 p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 hover:border-primary/30 transition-colors">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-1">{proj.systemId}</span>
                <h3 className="text-xl font-display text-foreground">{proj.title}</h3>
              </div>
              <p className="text-sm text-foreground/60 font-sans mb-3">{proj.description}</p>
              <p className="font-mono text-xs text-foreground/40">TECH: {proj.tech}</p>
            </div>
            <div className="flex items-center gap-4">
              {proj.repoLink && <a href={proj.repoLink} target="_blank" className="text-foreground/50 hover:text-primary transition-colors"><Github className="w-5 h-5" /></a>}
              {proj.liveLink && <a href={proj.liveLink} target="_blank" className="text-foreground/50 hover:text-primary transition-colors"><ExternalLink className="w-5 h-5" /></a>}
              <button onClick={() => handleDelete(proj.id)} className="text-red-500/50 hover:text-red-500 p-2 border border-transparent hover:border-red-500/20 transition-all"><Trash2 className="w-5 h-5" /></button>
            </div>
          </div>
        ))}
        {projects.length === 0 && <div className="text-center p-12 border border-dashed border-foreground/20 text-foreground/50 font-mono text-sm uppercase">No assets deployed in matrix.</div>}
      </div>
    </div>
  );
}
""")

    # ---------------------------------------------------------
    # 3. COMM CHANNEL (MESSAGES)
    # ---------------------------------------------------------
    print_status("Engineering Comm Channel (Messages)")
    
    os.makedirs(PROJECT_PATH / "src/app/api/admin/messages/[id]", exist_ok=True)
    with open(PROJECT_PATH / "src/app/api/admin/messages/[id]/route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  try {
    await db.message.update({ where: { id: params.id }, data: { isRead: true } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to update' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  try {
    await db.message.delete({ where: { id: params.id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete' }, { status: 500 });
  }
}
""")

    os.makedirs(PROJECT_PATH / "src/app/admin/messages", exist_ok=True)
    with open(PROJECT_PATH / "src/app/admin/messages/page.tsx", "w", encoding="utf-8") as f:
        f.write("""import { db } from '@/lib/db';
import MessagesUI from './MessagesUI';

export const dynamic = 'force-dynamic';

export default async function MessagesPage() {
  const messages = await db.message.findMany({ orderBy: { createdAt: 'desc' } });
  return <MessagesUI initialMessages={messages} />;
}
""")

    with open(PROJECT_PATH / "src/app/admin/messages/MessagesUI.tsx", "w", encoding="utf-8") as f:
        f.write(""""use client";
import { useState } from 'react';
import { MessageSquare, CheckCircle2, Trash2, Mail } from 'lucide-react';

export default function MessagesUI({ initialMessages }: { initialMessages: any[] }) {
  const [messages, setMessages] = useState(initialMessages);

  const handleMarkRead = async (id: string) => {
    await fetch(`/api/admin/messages/${id}`, { method: 'PUT' });
    setMessages(messages.map(m => m.id === id ? { ...m, isRead: true } : m));
  };

  const handleDelete = async (id: string) => {
    await fetch(`/api/admin/messages/${id}`, { method: 'DELETE' });
    setMessages(messages.filter(m => m.id !== id));
  };

  return (
    <div className="w-full flex flex-col gap-10">
      <div>
        <h1 className="text-3xl md:text-4xl font-display font-medium text-foreground">Comm Channel</h1>
        <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Incoming Secure Transmissions</p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {messages.map(msg => (
          <div key={msg.id} className={`bg-background border p-6 transition-colors ${msg.isRead ? 'border-foreground/10 opacity-70' : 'border-primary/50 shadow-[0_0_20px_rgba(0,240,255,0.05)]'}`}>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-full ${msg.isRead ? 'bg-foreground/5 text-foreground/40' : 'bg-primary/10 text-primary animate-pulse'}`}>
                  <Mail className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-display text-foreground flex items-center gap-2">
                    {msg.name} {!msg.isRead && <span className="w-2 h-2 rounded-full bg-primary"></span>}
                  </h3>
                  <a href={`mailto:${msg.email}`} className="font-mono text-xs text-primary hover:underline">{msg.email}</a>
                </div>
              </div>
              <span className="font-mono text-[10px] text-foreground/40 tracking-widest uppercase">
                {new Date(msg.createdAt).toLocaleDateString()} // {new Date(msg.createdAt).toLocaleTimeString()}
              </span>
            </div>
            
            <div className="bg-black/50 border border-foreground/5 p-4 font-mono text-sm text-foreground/70 leading-relaxed whitespace-pre-wrap mb-4">
              {msg.payload}
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-foreground/5">
              {!msg.isRead && (
                <button onClick={() => handleMarkRead(msg.id)} className="flex items-center gap-2 px-4 py-2 text-emerald-500 font-mono text-xs uppercase hover:bg-emerald-500/10 transition-colors">
                  <CheckCircle2 className="w-4 h-4" /> Acknowledge
                </button>
              )}
              <button onClick={() => handleDelete(msg.id)} className="flex items-center gap-2 px-4 py-2 text-red-500/70 font-mono text-xs uppercase hover:bg-red-500/10 hover:text-red-500 transition-colors">
                <Trash2 className="w-4 h-4" /> Purge Data
              </button>
            </div>
          </div>
        ))}
        {messages.length === 0 && <div className="text-center p-12 border border-dashed border-foreground/20 text-foreground/50 font-mono text-sm uppercase">Comm channel is empty. No incoming transmissions.</div>}
      </div>
    </div>
  );
}
""")

    print_status("Matrix Controller and Comm Channel Deployed")

if __name__ == "__main__":
    deploy_admin_suite()
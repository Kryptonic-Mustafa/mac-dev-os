import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚙️ M.A.C.DevOS Update] {message}...")
    time.sleep(0.5)

def deploy_master_control():
    # ---------------------------------------------------------
    # 1. DATABASE SCHEMA UPDATE
    # ---------------------------------------------------------
    print_status("Updating Database Schema with System Settings")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    
    schema_content = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

model Admin {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   
  createdAt DateTime @default(now())
}

model Project {
  id          String   @id @default(uuid())
  systemId    String   @unique 
  title       String
  description String   @db.Text
  tech        String   
  repoLink    String?
  liveLink    String?
  order       Int      @default(0)
  isVisible   Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Review {
  id        String   @id @default(uuid())
  logId     String   @unique 
  client    String
  role      String
  content   String   @db.Text
  status    String   @default("VERIFIED")
  isVisible Boolean  @default(true)
  createdAt DateTime @default(now())
}

model Message {
  id        String   @id @default(uuid())
  name      String
  email     String
  payload   String   @db.Text
  isRead    Boolean  @default(false)
  createdAt DateTime @default(now())
}

// NEW: System Settings Table
model SystemSettings {
  id          String   @id @default("master_config")
  siteName    String   @default("M.A.C.DevOS")
  logoUrl     String?  
  faviconUrl  String?
  githubUrl   String?
  linkedinUrl String?
  twitterUrl  String?
  updatedAt   DateTime @updatedAt
}
"""
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(schema_content)

    # Push to DB and Generate
    print_status("Syncing Database Schema")
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # ---------------------------------------------------------
    # 2. UPDATE SIDEBAR LAYOUT
    # ---------------------------------------------------------
    print_status("Injecting Master Settings into HUD Layout")
    layout_path = PROJECT_PATH / "src/app/admin/layout.tsx"
    
    if layout_path.exists():
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_content = f.read()
        
        if "Settings" not in layout_content:
            layout_content = layout_content.replace(
                "import { Terminal, LayoutDashboard, FolderKanban, MessageSquare, LogOut } from 'lucide-react';",
                "import { Terminal, LayoutDashboard, FolderKanban, MessageSquare, LogOut, Settings } from 'lucide-react';"
            )
            layout_content = layout_content.replace(
                "{ name: 'Comm Channel', href: '/admin/messages', icon: MessageSquare },",
                "{ name: 'Comm Channel', href: '/admin/messages', icon: MessageSquare },\n    { name: 'Master Settings', href: '/admin/settings', icon: Settings },"
            )
            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(layout_content)

    # ---------------------------------------------------------
    # 3. UPGRADE MATRIX (PROJECTS MODAL)
    # ---------------------------------------------------------
    print_status("Upgrading Matrix to use Floating Deployment Modal")
    projects_ui_path = PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx"
    
    projects_ui_content = """"use client";
import { useState } from 'react';
import { FolderKanban, Plus, Trash2, Github, ExternalLink, X } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  const [projects, setProjects] = useState(initialProjects);
  const [isModalOpen, setIsModalOpen] = useState(false);

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
    setIsModalOpen(false);
  };

  return (
    <div className="w-full flex flex-col gap-10 relative">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl md:text-4xl font-display font-medium text-foreground">Deployment Matrix</h1>
          <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Manage Portfolio Assets</p>
        </div>
        <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary text-primary font-mono text-xs uppercase hover:bg-primary/20 hover:shadow-[0_0_15px_var(--color-primary)] transition-all">
          <Plus className="w-4 h-4" /> Deploy Asset
        </button>
      </div>

      {/* FLOATING DEPLOYMENT MODAL */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-300">
          <div className="bg-background border border-primary/50 shadow-[0_0_50px_rgba(0,240,255,0.1)] w-full max-w-2xl relative">
            
            <div className="flex items-center justify-between p-4 border-b border-foreground/10 bg-foreground/[0.02]">
              <div className="flex items-center gap-2 font-mono text-xs uppercase text-primary tracking-widest">
                <FolderKanban className="w-4 h-4" /> Initialize Deployment
              </div>
              <button onClick={() => setIsModalOpen(false)} className="text-foreground/50 hover:text-red-500 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAdd} className="p-6 flex flex-col gap-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">System Title</label>
                  <input name="title" required placeholder="e.g. Budget Master Engine" className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Tech Stack</label>
                  <input name="tech" required placeholder="React, Node.js, MySQL" className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">GitHub Repository URL</label>
                  <input name="repoLink" placeholder="https://github.com/..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Live Production URL</label>
                  <input name="liveLink" placeholder="https://..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">System Description</label>
                <textarea name="description" required placeholder="Detail the architecture and purpose of this system..." rows={4} className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full resize-none" />
              </div>

              <div className="flex justify-end gap-4 pt-4 border-t border-foreground/10">
                <button type="button" onClick={() => setIsModalOpen(false)} className="px-6 py-2 border border-foreground/20 text-foreground/70 font-mono text-xs uppercase hover:bg-foreground/5 transition-colors">Abort</button>
                <button type="submit" className="px-6 py-2 bg-primary/20 border border-primary text-primary font-mono text-xs uppercase font-bold hover:bg-primary hover:text-background transition-all">Execute Deployment</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MATRIX GRID */}
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
              {proj.repoLink && <a href={proj.repoLink} target="_blank" className="text-foreground/50 hover:text-primary transition-colors flex items-center gap-2 text-xs font-mono"><Github className="w-4 h-4" /> Repo</a>}
              {proj.liveLink && <a href={proj.liveLink} target="_blank" className="text-primary/70 hover:text-primary transition-colors flex items-center gap-2 text-xs font-mono"><ExternalLink className="w-4 h-4" /> Live</a>}
              <div className="w-px h-6 bg-foreground/10 mx-2"></div>
              <button onClick={() => handleDelete(proj.id)} className="text-red-500/50 hover:text-red-500 p-2 border border-transparent hover:border-red-500/20 transition-all"><Trash2 className="w-4 h-4" /></button>
            </div>
          </div>
        ))}
        {projects.length === 0 && <div className="text-center p-12 border border-dashed border-foreground/20 text-foreground/50 font-mono text-sm uppercase">No assets deployed in matrix.</div>}
      </div>
    </div>
  );
}
"""
    with open(projects_ui_path, "w", encoding="utf-8") as f:
        f.write(projects_ui_content)

    # ---------------------------------------------------------
    # 4. UPGRADE COMM CHANNEL (INBOX VIEW)
    # ---------------------------------------------------------
    print_status("Upgrading Comm Channel UI")
    messages_ui_path = PROJECT_PATH / "src/app/admin/messages/MessagesUI.tsx"
    
    messages_ui_content = """"use client";
import { useState } from 'react';
import { MessageSquare, CheckCircle2, Trash2, Mail, ExternalLink } from 'lucide-react';

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
        <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Secure Inbox Transmissions</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {messages.map(msg => (
          <div key={msg.id} className={`bg-background border p-6 flex flex-col gap-4 transition-all ${msg.isRead ? 'border-foreground/10 opacity-70' : 'border-primary/50 shadow-[0_0_20px_rgba(0,240,255,0.05)]'}`}>
            
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-4 border-b border-foreground/10">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded bg-foreground/[0.02] border ${msg.isRead ? 'border-foreground/10 text-foreground/40' : 'border-primary/30 text-primary'}`}>
                  <Mail className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-display text-foreground flex items-center gap-2">
                    {msg.name} {!msg.isRead && <span className="px-2 py-0.5 rounded bg-primary text-background font-mono text-[10px] uppercase font-bold tracking-widest animate-pulse">New</span>}
                  </h3>
                  <p className="font-mono text-xs text-primary/70">{msg.email}</p>
                </div>
              </div>
              <span className="font-mono text-xs text-foreground/40 tracking-widest uppercase">
                {new Date(msg.createdAt).toLocaleString()}
              </span>
            </div>
            
            {/* Payload */}
            <div className="bg-black/40 border-l-2 border-primary/30 p-6 font-mono text-sm text-foreground/80 leading-relaxed whitespace-pre-wrap">
              {msg.payload}
            </div>

            {/* Actions */}
            <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
              <a 
                href={`mailto:${msg.email}?subject=Re: [M.A.C.DevOS] Transmission Received`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 px-6 py-2.5 bg-foreground/5 border border-foreground/20 text-foreground font-mono text-xs uppercase hover:bg-foreground/10 transition-colors"
              >
                <ExternalLink className="w-4 h-4" /> Reply via Gmail
              </a>

              <div className="flex items-center gap-3">
                {!msg.isRead && (
                  <button onClick={() => handleMarkRead(msg.id)} className="flex items-center gap-2 px-4 py-2 text-emerald-500 font-mono text-xs uppercase hover:bg-emerald-500/10 transition-colors border border-transparent hover:border-emerald-500/20">
                    <CheckCircle2 className="w-4 h-4" /> Mark Acknowledged
                  </button>
                )}
                <button onClick={() => handleDelete(msg.id)} className="flex items-center gap-2 px-4 py-2 text-red-500/70 font-mono text-xs uppercase hover:bg-red-500/10 hover:text-red-500 transition-colors border border-transparent hover:border-red-500/20">
                  <Trash2 className="w-4 h-4" /> Purge
                </button>
              </div>
            </div>

          </div>
        ))}
        {messages.length === 0 && <div className="text-center p-12 border border-dashed border-foreground/20 text-foreground/50 font-mono text-sm uppercase">Comm channel is empty.</div>}
      </div>
    </div>
  );
}
"""
    with open(messages_ui_path, "w", encoding="utf-8") as f:
        f.write(messages_ui_content)

    # ---------------------------------------------------------
    # 5. CREATE MASTER SETTINGS MODULE
    # ---------------------------------------------------------
    print_status("Engineering Master Settings Control Panel")
    
    os.makedirs(PROJECT_PATH / "src/app/api/admin/settings", exist_ok=True)
    with open(PROJECT_PATH / "src/app/api/admin/settings/route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const settings = await db.systemSettings.upsert({
      where: { id: 'master_config' },
      update: data,
      create: { id: 'master_config', ...data }
    });
    return NextResponse.json(settings);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to save settings' }, { status: 500 });
  }
}
""")

    os.makedirs(PROJECT_PATH / "src/app/admin/settings", exist_ok=True)
    with open(PROJECT_PATH / "src/app/admin/settings/page.tsx", "w", encoding="utf-8") as f:
        f.write("""import { db } from '@/lib/db';
import SettingsUI from './SettingsUI';

export const dynamic = 'force-dynamic';

export default async function SettingsPage() {
  let settings = await db.systemSettings.findUnique({ where: { id: 'master_config' } });
  
  if (!settings) {
    settings = {
      id: 'master_config',
      siteName: 'M.A.C.DevOS',
      logoUrl: '',
      faviconUrl: '',
      githubUrl: '',
      linkedinUrl: '',
      twitterUrl: '',
      updatedAt: new Date()
    };
  }
  
  return <SettingsUI initialSettings={settings} />;
}
""")

    settings_ui_content = """"use client";
import { useState } from 'react';
import { Save, Settings2, ShieldCheck, Loader2, CheckCircle2 } from 'lucide-react';

export default function SettingsUI({ initialSettings }: { initialSettings: any }) {
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSave = async (e: any) => {
    e.preventDefault();
    setIsSaving(true);
    setSuccess(false);

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    await fetch('/api/admin/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    setIsSaving(false);
    setSuccess(true);
    setTimeout(() => setSuccess(false), 3000);
  };

  return (
    <div className="w-full flex flex-col gap-10">
      <div>
        <h1 className="text-3xl md:text-4xl font-display font-medium text-foreground">Master Settings</h1>
        <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Global Environment Variables</p>
      </div>

      <form onSubmit={handleSave} className="flex flex-col gap-8 max-w-3xl">
        
        {/* Brand Section */}
        <div className="bg-background border border-foreground/10 p-6 md:p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 pb-4 border-b border-foreground/10">
            <Settings2 className="w-5 h-5 text-primary" />
            <h2 className="font-display text-xl">Brand Identity</h2>
          </div>
          
          <div className="flex flex-col gap-2">
            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Global Site Name</label>
            <input name="siteName" defaultValue={initialSettings.siteName} required className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Logo Image URL</label>
              <input name="logoUrl" defaultValue={initialSettings.logoUrl} placeholder="/logo.png or https://..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
            </div>
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Favicon URL</label>
              <input name="faviconUrl" defaultValue={initialSettings.faviconUrl} placeholder="/favicon.ico" className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
            </div>
          </div>
        </div>

        {/* Social Links Section */}
        <div className="bg-background border border-foreground/10 p-6 md:p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 pb-4 border-b border-foreground/10">
            <ShieldCheck className="w-5 h-5 text-primary" />
            <h2 className="font-display text-xl">External Node Links (Footer)</h2>
          </div>
          
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">GitHub URL</label>
              <input name="githubUrl" defaultValue={initialSettings.githubUrl} placeholder="https://github.com/..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
            </div>
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">LinkedIn URL</label>
              <input name="linkedinUrl" defaultValue={initialSettings.linkedinUrl} placeholder="https://linkedin.com/in/..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
            </div>
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Twitter / X URL</label>
              <input name="twitterUrl" defaultValue={initialSettings.twitterUrl} placeholder="https://twitter.com/..." className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button type="submit" disabled={isSaving} className="flex items-center gap-2 px-8 py-4 bg-primary/20 border border-primary text-primary font-mono text-sm tracking-widest uppercase font-bold hover:bg-primary hover:text-background transition-all disabled:opacity-50">
            {isSaving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
            {isSaving ? 'Compiling...' : 'Save Configuration'}
          </button>
          
          {success && (
            <span className="text-emerald-500 font-mono text-xs flex items-center gap-2 animate-in slide-in-from-left-4">
              <CheckCircle2 className="w-4 h-4" /> Config Saved
            </span>
          )}
        </div>
        
      </form>
    </div>
  );
}
"""
    with open(PROJECT_PATH / "src/app/admin/settings/SettingsUI.tsx", "w", encoding="utf-8") as f:
        f.write(settings_ui_content)

    print_status("System Architecture Upgrade Complete")

if __name__ == "__main__":
    deploy_master_control()
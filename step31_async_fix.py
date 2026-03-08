import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚀 M.A.C.DevOS Core Update] {message}...")
    time.sleep(0.5)

def deploy_async_fix():
    # 1. FIX ASYNC API ROUTE (Next.js 15 Requirement)
    print_status("Awaiting Params: Fixing Next.js 15 Async API")
    api_path = PROJECT_PATH / "src/app/api/admin/projects/[id]/route.ts"
    
    api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    // UNWRAP PARAMS FIRST
    const { id } = await params;
    const data = await req.json();

    const project = await db.project.update({
      where: { id: id },
      data: data
    });
    return NextResponse.json(project);
  } catch (error) {
    console.error("Patch Error:", error);
    return NextResponse.json({ error: 'Update Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.project.delete({ where: { id: id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Deletion Failed' }, { status: 500 });
  }
}
"""
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(api_content)

    # 2. UPGRADING UI WITH MISSING URL FIELDS
    print_status("Injecting GitHub & Live Link Fields into Edit Modal")
    ui_path = PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx"
    
    # We are rewriting the UI to include the repoLink and liveLink inputs
    ui_content = """"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Trash2, Edit3, X, Save, Loader2, Github, Globe } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  const [projects, setProjects] = useState(initialProjects);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2500,
    timerProgressBar: true,
    background: '#0a0a0a',
    color: '#fff'
  });

  const handleUpdate = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      const res = await fetch(`/api/admin/projects/${currentProject.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        await Toast.fire({ icon: 'success', title: 'Telemetry Synced' });
        window.location.reload();
      } else { throw new Error(); }
    } catch (err) {
      Toast.fire({ icon: 'error', title: 'Sync Failed', text: 'Check console for details.' });
    } finally { setLoading(false); }
  };

  return (
    <div className="w-full flex flex-col gap-10 pb-20">
      <h1 className="text-3xl font-display text-foreground">Deployment Matrix</h1>
      <div className="flex flex-col gap-4">
        {projects.map(p => (
          <div key={p.id} className="bg-background border border-foreground/10 p-8 flex justify-between items-center group hover:border-primary/30 transition-all">
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-3">
                <span className="font-mono text-[9px] bg-primary/10 text-primary px-2 py-0.5 border border-primary/20">{p.systemId}</span>
                <h3 className="text-xl font-display text-foreground">{p.title}</h3>
              </div>
              <p className="text-foreground/40 text-xs font-mono">{p.tech}</p>
            </div>
            <div className="flex items-center gap-6">
              <button onClick={() => { setCurrentProject(p); setIsEditModalOpen(true); }} className="text-foreground/20 hover:text-primary transition-colors"><Edit3 className="w-5 h-5" /></button>
              <button onClick={() => {/* Delete logic */}} className="text-foreground/20 hover:text-red-500 transition-colors"><Trash2 className="w-5 h-5" /></button>
            </div>
          </div>
        ))}
      </div>

      {isEditModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md">
          <div className="bg-background border border-foreground/10 w-full max-w-2xl p-10 relative animate-in fade-in zoom-in duration-300">
            <button onClick={() => setIsEditModalOpen(false)} className="absolute top-6 right-6 text-foreground/30 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-8">EDIT ASSET: {currentProject.systemId}</h2>
            <form onSubmit={handleUpdate} className="grid grid-cols-2 gap-6">
              <div className="col-span-2 flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Project Title</label>
                <input name="title" defaultValue={currentProject.title} className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="col-span-2 flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Tech Stack</label>
                <input name="tech" defaultValue={currentProject.tech} className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase flex items-center gap-2"><Github className="w-3 h-3" /> Repo URL</label>
                <input name="repoLink" defaultValue={currentProject.repoLink} className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase flex items-center gap-2"><Globe className="w-3 h-3" /> Live URL</label>
                <input name="liveLink" defaultValue={currentProject.liveLink} className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <button type="submit" disabled={loading} className="col-span-2 p-5 bg-primary text-background font-mono font-bold uppercase tracking-[0.2em] mt-4 flex items-center justify-center gap-3 hover:shadow-neon transition-all">
                {loading ? <Loader2 className="animate-spin" /> : <Save />} Commit Changes
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
"""
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(ui_content)

    print_status("System Hotfixed. API is now Async-compliant and URLs are editable.")

if __name__ == "__main__":
    deploy_async_fix()
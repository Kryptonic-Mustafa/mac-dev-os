import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Project Editor] {message}...")
    time.sleep(0.5)

def deploy_project_editor():
    # 1. ENSURE REVIEW MODEL IS IN SCHEMA (Fixes the Review Page Loop)
    print_status("Aligning Prisma Schema for Telemetry Logs")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_content = f.read()
    
    if "model Review" not in schema_content:
        review_model = """
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
"""
        with open(schema_path, "a", encoding="utf-8") as f:
            f.write(review_model)
        print("  ✓ Review model injected into schema.")

    # 2. PHYSICAL DATABASE PUSH (Creates the missing table)
    print_status("Physically Creating Missing Tables in MySQL")
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # 3. ENGINEERING PROJECT EDIT API
    print_status("Deploying Project Update API")
    project_api_path = PROJECT_PATH / "src/app/api/admin/projects/[id]/route.ts"
    os.makedirs(project_api_path.parent, exist_ok=True)
    
    api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PATCH(req: Request, { params }: { params: { id: string } }) {
  try {
    const data = await req.json();
    const project = await db.project.update({
      where: { id: params.id },
      data: data
    });
    return NextResponse.json(project);
  } catch (error) {
    return NextResponse.json({ error: 'Update Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  try {
    await db.project.delete({ where: { id: params.id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Deletion Failed' }, { status: 500 });
  }
}
"""
    with open(project_api_path, "w", encoding="utf-8") as f:
        f.write(api_content)

    # 4. UPGRADING PROJECTS UI WITH EDIT MODAL & SWEETALERT
    print_status("Updating Project Matrix with Edit Suite")
    ui_path = PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx"
    
    ui_content = """"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Plus, Trash2, Edit3, ExternalLink, Globe, Github, X, Save, Loader2 } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  const [projects, setProjects] = useState(initialProjects);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2000,
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
        await Toast.fire({ icon: 'success', title: 'Matrix Re-aligned' });
        window.location.reload();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    const result = await Swal.fire({
      title: 'Purge Project?',
      text: "This asset will be permanently removed from the matrix.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      background: '#0a0a0a',
      color: '#fff'
    });

    if (result.isConfirmed) {
      const res = await fetch(`/api/admin/projects/${id}`, { method: 'DELETE' });
      if (res.ok) {
        Toast.fire('Purged!', '', 'success');
        setProjects(projects.filter(p => p.id !== id));
      }
    }
  };

  return (
    <div className="w-full flex flex-col gap-10 pb-20">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-display text-foreground">Deployment Matrix</h1>
        <button className="flex items-center gap-2 px-4 py-2 border border-primary text-primary font-mono text-[10px] uppercase hover:bg-primary hover:text-background transition-all">
          <Plus className="w-4 h-4" /> Deploy Asset
        </button>
      </div>

      <div className="flex flex-col gap-4">
        {projects.map(project => (
          <div key={project.id} className="bg-background border border-foreground/10 p-8 group hover:border-primary/30 transition-all">
            <div className="flex justify-between items-start">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-[10px] bg-primary/10 text-primary px-2 py-0.5 border border-primary/20">{project.systemId}</span>
                  <h3 className="text-xl font-display text-foreground">{project.title}</h3>
                </div>
                <p className="text-foreground/50 text-sm max-w-2xl">{project.description}</p>
                <p className="font-mono text-[10px] text-primary uppercase tracking-widest mt-2">Tech: {project.tech}</p>
              </div>
              <div className="flex items-center gap-4">
                <button onClick={() => { setCurrentProject(project); setIsEditModalOpen(true); }} className="text-foreground/30 hover:text-primary transition-colors">
                  <Edit3 className="w-5 h-5" />
                </button>
                <button onClick={() => handleDelete(project.id)} className="text-foreground/30 hover:text-red-500 transition-colors">
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {isEditModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm">
          <div className="bg-background border border-foreground/10 w-full max-w-2xl p-8 relative">
            <button onClick={() => setIsEditModalOpen(false)} className="absolute top-4 right-4 text-foreground/40 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-8">Edit Asset: {currentProject.systemId}</h2>
            <form onSubmit={handleUpdate} className="grid grid-cols-2 gap-6">
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Project Title</label>
                <input name="title" defaultValue={currentProject.title} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              </div>
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Description</label>
                <textarea name="description" rows={3} defaultValue={currentProject.description} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary resize-none" />
              </div>
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Technology Stack</label>
                <input name="tech" defaultValue={currentProject.tech} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Repo Link</label>
                <input name="repoLink" defaultValue={currentProject.repoLink} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Live Link</label>
                <input name="liveLink" defaultValue={currentProject.liveLink} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              </div>
              <button type="submit" disabled={loading} className="col-span-2 p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest mt-4 flex items-center justify-center gap-3">
                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : <Save className="w-5 h-5" />}
                Save Changes
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

    print_status("System Architecture Re-aligned and Project Editor Deployed.")

if __name__ == "__main__":
    deploy_project_editor()
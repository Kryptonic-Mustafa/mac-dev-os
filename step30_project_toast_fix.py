import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚡ M.A.C.DevOS Toast Engine] {message}...")
    time.sleep(0.5)

def deploy_toast_fix():
    # 1. UPGRADING PROJECTS UI WITH REINFORCED SWEETALERT
    print_status("Injecting Global Toasts into Project Matrix")
    ui_path = PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx"
    
    ui_content = """"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Plus, Trash2, Edit3, X, Save, Loader2 } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  const [projects, setProjects] = useState(initialProjects);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Reusable Toast Configuration
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2000,
    timerProgressBar: true,
    background: '#0a0a0a',
    color: '#fff',
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    }
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
        // TRIGGER SUCCESS TOAST BEFORE RELOAD
        await Toast.fire({
          icon: 'success',
          title: 'Matrix Entry Synchronized',
          text: 'Project data has been updated in MySQL core.'
        });
        window.location.reload();
      } else {
        throw new Error('Sync Failed');
      }
    } catch (err) {
      Toast.fire({
        icon: 'error',
        title: 'Sync Interrupted',
        text: 'Could not write to database.'
      });
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
      try {
        const res = await fetch(`/api/admin/projects/${id}`, { method: 'DELETE' });
        if (res.ok) {
          await Toast.fire({ icon: 'success', title: 'Asset Purged Successfully' });
          setProjects(projects.filter(p => p.id !== id));
        }
      } catch (err) {
        Toast.fire({ icon: 'error', title: 'Purge Failed' });
      }
    }
  };

  return (
    <div className="w-full flex flex-col gap-10 pb-20">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-display text-foreground">Deployment Matrix</h1>
      </div>

      <div className="flex flex-col gap-4">
        {projects.map(project => (
          <div key={project.id} className="bg-background border border-foreground/10 p-8 flex justify-between items-center hover:border-primary/30 transition-all">
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-3">
                <span className="font-mono text-[10px] bg-primary/10 text-primary px-2 py-0.5 border border-primary/20">{project.systemId}</span>
                <h3 className="text-xl font-display text-foreground">{project.title}</h3>
              </div>
              <p className="text-foreground/50 text-sm">{project.tech}</p>
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
        ))}
      </div>

      {isEditModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm">
          <div className="bg-background border border-foreground/10 w-full max-w-2xl p-8 relative">
            <button onClick={() => setIsEditModalOpen(false)} className="absolute top-4 right-4 text-foreground/40 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-8 uppercase tracking-tighter">Update Asset Telemetry</h2>
            <form onSubmit={handleUpdate} className="grid grid-cols-2 gap-6">
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Project Title</label>
                <input name="title" defaultValue={currentProject.title} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary" />
              </div>
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Description</label>
                <textarea name="description" rows={3} defaultValue={currentProject.description} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary resize-none" />
              </div>
              <div className="flex flex-col gap-2 col-span-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Technology Stack</label>
                <input name="tech" defaultValue={currentProject.tech} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary" />
              </div>
              <button type="submit" disabled={loading} className="col-span-2 p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest mt-4 flex items-center justify-center gap-3">
                {loading ? <Loader2 className="animate-spin w-5 h-5" /> : <Save className="w-5 h-5" />}
                Commit Changes
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

    print_status("Global SweetAlert Matrix Deployed. Your OS is now interactive.")

if __name__ == "__main__":
    deploy_toast_fix()
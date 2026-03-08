"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Trash2, Edit3, X, Save, Loader2, Github, Globe, PlusSquare } from 'lucide-react';

export default function ProjectsUI({ initialProjects }: { initialProjects: any[] }) {
  // Fallback to empty array if initialProjects is undefined
  const [projects, setProjects] = useState(initialProjects || []);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
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

  const handleCreate = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const data: any = Object.fromEntries(formData.entries());
    
    // Auto-generate a system ID like PRJ-8042
    data.systemId = `PRJ-${Math.floor(1000 + Math.random() * 9000)}`;
    data.order = projects.length; // Put it at the end of the list

    try {
      const res = await fetch('/api/admin/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        await Toast.fire({ icon: 'success', title: 'Asset Deployed to Matrix' });
        window.location.reload();
      } else { throw new Error(); }
    } catch (err) {
      Toast.fire({ icon: 'error', title: 'Deployment Failed' });
    } finally { setLoading(false); }
  };

  const handleUpdate = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const data: any = Object.fromEntries(formData.entries());

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
      Toast.fire({ icon: 'error', title: 'Sync Failed' });
    } finally { setLoading(false); }
  };

  const handleDelete = async (id: string, systemId: string) => {
    const confirm = await Swal.fire({
      title: `Purge Asset ${systemId}?`,
      text: "This action cannot be undone.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ef4444',
      cancelButtonColor: '#27272a',
      confirmButtonText: 'Yes, Purge It',
      background: '#0a0a0a',
      color: '#fff'
    });

    if (confirm.isConfirmed) {
      try {
        const res = await fetch(`/api/admin/projects/${id}`, { method: 'DELETE' });
        if (res.ok) {
          await Toast.fire({ icon: 'success', title: 'Asset Purged' });
          window.location.reload();
        } else { throw new Error(); }
      } catch (err) {
        Toast.fire({ icon: 'error', title: 'Purge Failed' });
      }
    }
  };

  return (
    <div className="w-full flex flex-col gap-10 pb-20">
      <div className="flex justify-between items-end border-b border-foreground/10 pb-6">
        <h1 className="text-3xl font-display text-foreground">Deployment Matrix</h1>
        <button 
          onClick={() => setIsAddModalOpen(true)}
          className="bg-primary/10 text-primary border border-primary/30 px-6 py-3 font-mono text-xs uppercase tracking-widest hover:bg-primary hover:text-background transition-all flex items-center gap-2"
        >
          <PlusSquare className="w-4 h-4" /> Deploy New Asset
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 border border-dashed border-foreground/20 text-foreground/40 font-mono text-sm">
          <p>[ MATRIX EMPTY ]</p>
          <p className="text-xs mt-2">Awaiting payload injection...</p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {projects.map((p: any) => (
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
                <button onClick={() => handleDelete(p.id, p.systemId)} className="text-foreground/20 hover:text-red-500 transition-colors"><Trash2 className="w-5 h-5" /></button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* CREATE MODAL */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md">
          <div className="bg-background border border-foreground/10 w-full max-w-2xl p-10 relative animate-in fade-in zoom-in duration-300">
            <button onClick={() => setIsAddModalOpen(false)} className="absolute top-6 right-6 text-foreground/30 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-8">INITIALIZE NEW ASSET</h2>
            <form onSubmit={handleCreate} className="grid grid-cols-2 gap-6">
              <div className="col-span-2 flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Project Title</label>
                <input name="title" required placeholder="e.g. CoreStrength Nutrition" className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="col-span-2 flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Description</label>
                <textarea name="description" required rows={3} placeholder="Project details..." className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground resize-none" />
              </div>
              <div className="col-span-2 flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Tech Stack</label>
                <input name="tech" required placeholder="e.g. Next.js, Tailwind, Prisma" className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase flex items-center gap-2"><Github className="w-3 h-3" /> Repo URL</label>
                <input name="repoLink" placeholder="https://github.com/..." className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/40 uppercase flex items-center gap-2"><Globe className="w-3 h-3" /> Live URL</label>
                <input name="liveLink" placeholder="https://..." className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground" />
              </div>
              <button type="submit" disabled={loading} className="col-span-2 p-5 bg-primary text-background font-mono font-bold uppercase tracking-[0.2em] mt-4 flex items-center justify-center gap-3 hover:shadow-neon transition-all">
                {loading ? <Loader2 className="animate-spin" /> : <Save />} Execute Deployment
              </button>
            </form>
          </div>
        </div>
      )}

      {/* EDIT MODAL (Existing logic maintained) */}
      {isEditModalOpen && currentProject && (
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
                <label className="font-mono text-[10px] text-foreground/40 uppercase">Description</label>
                <textarea name="description" defaultValue={currentProject.description} rows={3} className="bg-foreground/[0.03] border border-foreground/10 p-4 text-sm outline-none focus:border-primary text-foreground resize-none" />
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

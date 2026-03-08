"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Quote, Plus, Trash2, Edit3, ShieldCheck, Loader2, X, Save } from 'lucide-react';

export default function ReviewsUI({ initialReviews }: { initialReviews: any[] }) {
  const [reviews, setReviews] = useState(initialReviews);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentReview, setCurrentReview] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const Toast = Swal.mixin({
    toast: true, position: 'top-end', showConfirmButton: false, timer: 2500, background: '#0a0a0a', color: '#fff'
  });

  const handleAdd = async (e: any) => {
    e.preventDefault(); setLoading(true);
    const data = Object.fromEntries(new FormData(e.target));
    try {
      const res = await fetch('/api/admin/reviews', { method: 'POST', body: JSON.stringify(data) });
      if (res.ok) { await Toast.fire({ icon: 'success', title: 'Review Logged' }); window.location.reload(); }
    } finally { setLoading(false); }
  };

  const handleUpdate = async (e: any) => {
    e.preventDefault(); setLoading(true);
    const data = Object.fromEntries(new FormData(e.target));
    try {
      const res = await fetch(`/api/admin/reviews/${currentReview.id}`, { method: 'PATCH', body: JSON.stringify(data) });
      if (res.ok) { await Toast.fire({ icon: 'success', title: 'Telemetry Updated' }); window.location.reload(); }
    } finally { setLoading(false); }
  };

  const handleDelete = async (id: string) => {
    const result = await Swal.fire({ title: 'Purge Log?', icon: 'warning', showCancelButton: true, confirmButtonColor: '#d33', background: '#0a0a0a', color: '#fff' });
    if (result.isConfirmed) {
      const res = await fetch(`/api/admin/reviews/${id}`, { method: 'DELETE' });
      if (res.ok) { Toast.fire('Purged!', '', 'success'); setReviews(reviews.filter(r => r.id !== id)); }
    }
  };

  return (
    <div className="w-full flex flex-col gap-10 relative pb-20">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display text-foreground">Telemetry Logs</h1>
          <p className="font-mono text-xs text-foreground/50 uppercase tracking-widest mt-2">Client Reviews & Validation</p>
        </div>
        <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary text-primary font-mono text-[10px] uppercase hover:bg-primary hover:text-background transition-all">
          <Plus className="w-4 h-4" /> Add Review
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reviews.map(rev => (
          <div key={rev.id} className="bg-background border border-foreground/10 p-6 flex flex-col gap-4 group hover:border-primary/30 transition-colors">
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 px-2 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 rounded font-mono text-[9px] uppercase tracking-widest"><ShieldCheck className="w-3 h-3" /> {rev.logId}</div>
                <div className="px-2 py-1 bg-foreground/5 border border-foreground/10 text-foreground/60 rounded font-mono text-[9px] uppercase tracking-widest">PRIORITY: {rev.priority}</div>
              </div>
              <div className="flex items-center gap-3">
                <button onClick={() => { setCurrentReview(rev); setIsEditModalOpen(true); }} className="text-foreground/30 hover:text-primary transition-colors"><Edit3 className="w-4 h-4" /></button>
                <button onClick={() => handleDelete(rev.id)} className="text-foreground/30 hover:text-red-500 transition-colors"><Trash2 className="w-4 h-4" /></button>
              </div>
            </div>
            <p className="text-sm text-foreground/70 italic leading-relaxed">"{rev.content}"</p>
            <div className="pt-4 border-t border-foreground/5">
              <h4 className="font-display text-foreground">{rev.client}</h4>
              <p className="font-mono text-[10px] text-foreground/40 uppercase tracking-widest">{rev.role}</p>
            </div>
          </div>
        ))}
      </div>

      {/* ADD MODAL */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md animate-in fade-in zoom-in duration-300">
          <div className="bg-background border border-foreground/10 w-full max-w-lg p-8 relative">
            <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-4 text-foreground/40 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-6">New Telemetry Entry</h2>
            <form onSubmit={handleAdd} className="flex flex-col gap-4">
              <input name="client" required placeholder="Client Name" className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              <input name="role" required placeholder="Role (e.g. CEO at TechCorp)" className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              <input name="priority" type="number" defaultValue={0} placeholder="Display Priority (Higher = First)" className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              <textarea name="content" required placeholder="Review Content..." rows={4} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary resize-none" />
              <button type="submit" disabled={loading} className="w-full p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest mt-4 hover:shadow-neon transition-all">{loading ? 'Processing...' : 'Execute Log Entry'}</button>
            </form>
          </div>
        </div>
      )}

      {/* EDIT MODAL */}
      {isEditModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md animate-in fade-in zoom-in duration-300">
          <div className="bg-background border border-foreground/10 w-full max-w-lg p-8 relative">
            <button onClick={() => setIsEditModalOpen(false)} className="absolute top-4 right-4 text-foreground/40 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-6">Edit Telemetry: {currentReview?.logId}</h2>
            <form onSubmit={handleUpdate} className="flex flex-col gap-4">
              <input name="client" required defaultValue={currentReview?.client} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary text-foreground" />
              <input name="role" required defaultValue={currentReview?.role} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary text-foreground" />
              <input name="priority" type="number" defaultValue={currentReview?.priority} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary text-foreground" />
              <textarea name="content" required defaultValue={currentReview?.content} rows={4} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary resize-none text-foreground" />
              <button type="submit" disabled={loading} className="w-full p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest mt-4 flex justify-center gap-2 hover:shadow-neon transition-all">{loading ? <Loader2 className="animate-spin" /> : <Save />} Commit Changes</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

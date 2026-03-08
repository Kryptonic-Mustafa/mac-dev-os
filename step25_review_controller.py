import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📊 M.A.C.DevOS Telemetry] {message}...")
    time.sleep(0.5)

def deploy_review_system():
    # 1. FIX THE CONTACT FORM (Move "use client" to top)
    print_status("Fixing Contact Form Directive Error")
    contact_path = PROJECT_PATH / "src/components/sections/Contact.tsx"
    if contact_path.exists():
        with open(contact_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Remove any misplaced "use client" and put it at index 0
        new_lines = [l for l in lines if '"use client"' not in l and "'use client'" not in l]
        new_lines.insert(0, '"use client";\n')
        
        with open(contact_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    # 2. CREATE REVIEW API ROUTES
    print_status("Engineering Review CRUD API")
    api_dir = PROJECT_PATH / "src/app/api/admin/reviews"
    os.makedirs(api_dir, exist_ok=True)
    
    with open(api_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  const reviews = await db.review.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(reviews);
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const logId = `LOG-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
    const review = await db.review.create({
      data: { ...data, logId }
    });
    return NextResponse.json(review);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to log review' }, { status: 500 });
  }
}
""")

    # 3. CREATE REVIEW UI
    print_status("Rendering Review Controller HUD")
    review_ui_dir = PROJECT_PATH / "src/app/admin/reviews"
    os.makedirs(review_ui_dir, exist_ok=True)
    
    # Page Wrapper
    with open(review_ui_dir / "page.tsx", "w", encoding="utf-8") as f:
        f.write("""import { db } from '@/lib/db';
import ReviewsUI from './ReviewsUI';

export const dynamic = 'force-dynamic';

export default async function ReviewsPage() {
  const reviews = await db.review.findMany({ orderBy: { createdAt: 'desc' } });
  return <ReviewsUI initialReviews={reviews} />;
}
""")

    # ReviewsUI Component
    with open(review_ui_dir / "ReviewsUI.tsx", "w", encoding="utf-8") as f:
        f.write(""""use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Quote, Plus, Trash2, ShieldCheck, Loader2, X } from 'lucide-react';

export default function ReviewsUI({ initialReviews }: { initialReviews: any[] }) {
  const [reviews, setReviews] = useState(initialReviews);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2000,
    background: '#0a0a0a',
    color: '#fff'
  });

  const handleAdd = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      const res = await fetch('/api/admin/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        await Toast.fire({ icon: 'success', title: 'Review Logged' });
        window.location.reload();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    const result = await Swal.fire({
      title: 'Purge Log?',
      text: "This action cannot be undone.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      background: '#0a0a0a',
      color: '#fff'
    });

    if (result.isConfirmed) {
      // Add DELETE API logic here later if needed, for now just filter
      setReviews(reviews.filter(r => r.id !== id));
      Toast.fire('Deleted!', '', 'success');
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

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm">
          <div className="bg-background border border-foreground/10 w-full max-w-lg p-8 relative">
            <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-4 text-foreground/40 hover:text-foreground"><X /></button>
            <h2 className="text-2xl font-display mb-6">New Telemetry Entry</h2>
            <form onSubmit={handleAdd} className="flex flex-col gap-4">
              <input name="client" required placeholder="Client Name" className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              <input name="role" required placeholder="Role (e.g. CEO at TechCorp)" className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary" />
              <textarea name="content" required placeholder="Review Content..." rows={4} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm outline-none focus:border-primary resize-none" />
              <button type="submit" disabled={loading} className="w-full p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest mt-4">
                {loading ? 'Processing...' : 'Execute Log Entry'}
              </button>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reviews.map(rev => (
          <div key={rev.id} className="bg-background border border-foreground/10 p-6 flex flex-col gap-4 hover:border-primary/30 transition-colors">
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2 px-2 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 rounded font-mono text-[9px] uppercase tracking-widest">
                <ShieldCheck className="w-3 h-3" /> {rev.logId}
              </div>
              <button onClick={() => handleDelete(rev.id)} className="text-red-500/30 hover:text-red-500"><Trash2 className="w-4 h-4" /></button>
            </div>
            <p className="text-sm text-foreground/70 italic leading-relaxed">"{rev.content}"</p>
            <div className="pt-4 border-t border-foreground/5">
              <h4 className="font-display text-foreground">{rev.client}</h4>
              <p className="font-mono text-[10px] text-foreground/40 uppercase tracking-widest">{rev.role}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

    # 4. UPDATE SIDEBAR TO INCLUDE REVIEWS
    layout_path = PROJECT_PATH / "src/app/admin/layout.tsx"
    with open(layout_path, "r", encoding="utf-8") as f:
        layout_content = f.read()
    
    if "Reviews" not in layout_content:
        layout_content = layout_content.replace(
            "{ name: 'Master Settings', href: '/admin/settings', icon: Settings }",
            "{ name: 'Master Settings', href: '/admin/settings', icon: Settings },\n    { name: 'Telemetry Logs', href: '/admin/reviews', icon: Quote }"
        )
        layout_content = layout_content.replace(
            "LogOut } from 'lucide-react';",
            "LogOut, Quote } from 'lucide-react';"
        )
        with open(layout_path, "w", encoding="utf-8") as f:
            f.write(layout_content)

    print_status("Review Controller & Hotfix Deployed Successfully")

if __name__ == "__main__":
    deploy_review_system()
import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📡 M.A.C.DevOS Telemetry] {message}...")
    time.sleep(0.5)

def deploy_telemetry_upgrade():
    # 1. UPGRADE PRISMA SCHEMA (Adding Priority)
    print_status("Injecting Priority Parameter into Review Schema")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_content = f.read()

    if "priority" not in schema_content.split("model Review")[1]:
        # Replace the Review model with the upgraded version
        old_model = schema_content.split("model Review {")[1].split("}")[0]
        new_model = """
  id        String   @id @default(uuid())
  logId     String   @unique 
  client    String
  role      String
  content   String   @db.Text
  status    String   @default("VERIFIED")
  isVisible Boolean  @default(true)
  priority  Int      @default(0)
  createdAt DateTime @default(now())
"""
        schema_content = schema_content.replace(old_model, new_model)
        with open(schema_path, "w", encoding="utf-8") as f:
            f.write(schema_content)
            
    # Sync DB
    print_status("Synchronizing Schema with MySQL Core")
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # 2. UPGRADE GLOBAL API (Dynamic Fetching & Next.js 15 Async)
    print_status("Deploying Async-Compliant APIs & Cache Breakers")
    api_dir = PROJECT_PATH / "src/app/api/admin/reviews"
    os.makedirs(api_dir, exist_ok=True)

    # Main Route (GET/POST)
    with open(api_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export const dynamic = 'force-dynamic'; // BREAKS THE CACHE

export async function GET() {
  const reviews = await db.review.findMany({ 
    orderBy: [ { priority: 'desc' }, { createdAt: 'desc' } ] 
  });
  return NextResponse.json(reviews);
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const logId = `LOG-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
    const review = await db.review.create({
      data: { ...data, logId, priority: parseInt(data.priority) || 0 }
    });
    return NextResponse.json(review);
  } catch (error) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}
""")

    # Dynamic ID Route (PATCH/DELETE)
    id_api_dir = api_dir / "[id]"
    os.makedirs(id_api_dir, exist_ok=True)
    with open(id_api_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write("""import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const data = await req.json();
    const review = await db.review.update({
      where: { id },
      data: { ...data, priority: parseInt(data.priority) || 0 }
    });
    return NextResponse.json(review);
  } catch (error) {
    return NextResponse.json({ error: 'Update Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.review.delete({ where: { id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Deletion Failed' }, { status: 500 });
  }
}
""")

    # 3. UPGRADE ADMIN UI (Add Edit Suite & SweetAlert2)
    print_status("Rendering Edit Suite in Telemetry HUD")
    ui_path = PROJECT_PATH / "src/app/admin/reviews/ReviewsUI.tsx"
    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(""""use client";
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
""")

    # 4. UPGRADE FRONTEND (Fix Cache & Render)
    print_status("Re-Linking Frontend to Dynamic API")
    frontend_path = PROJECT_PATH / "src/components/sections/Reviews.tsx"
    with open(frontend_path, "w", encoding="utf-8") as f:
        f.write(""""use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Quote, ShieldCheck } from 'lucide-react';

if (typeof window !== "undefined") { gsap.registerPlugin(ScrollTrigger); }

export default function TelemetryLogs() {
  const [reviews, setReviews] = useState<any[]>([]);
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    // Adding a timestamp query bypasses any lingering browser cache
    fetch(`/api/admin/reviews?t=${new Date().getTime()}`)
      .then(res => res.json())
      .then(data => { if (Array.isArray(data)) setReviews(data); });
  }, []);

  useGSAP(() => {
    if (reviews.length === 0) return;
    gsap.from(".log-card", {
      opacity: 0, y: 50, stagger: 0.1, duration: 0.8,
      scrollTrigger: { trigger: containerRef.current, start: "top 80%" }
    });
  }, [reviews]);

  return (
    <section id="telemetry" ref={containerRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        <div className="mb-20 text-center md:text-left">
          <div className="flex items-center gap-3 mb-4 justify-center md:justify-start">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Validated Output</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">Telemetry Logs</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {reviews.map((rev) => (
            <div key={rev.id} className="log-card opacity-0 bg-foreground/[0.02] border border-foreground/10 p-8 flex flex-col gap-6 relative group hover:border-primary/30 transition-all">
              <div className="flex justify-between items-start">
                <Quote className="w-8 h-8 text-primary/20 group-hover:text-primary transition-colors" />
                <div className="font-mono text-[9px] text-emerald-500 bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 rounded uppercase flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> {rev.logId}
                </div>
              </div>
              <p className="text-foreground/70 font-sans italic leading-relaxed flex-1">"{rev.content}"</p>
              <div className="pt-6 border-t border-foreground/5">
                <h4 className="font-display text-foreground group-hover:text-primary transition-colors">{rev.client}</h4>
                <p className="font-mono text-[10px] text-foreground/40 uppercase tracking-widest">{rev.role}</p>
              </div>
            </div>
          ))}
        </div>
        
        {reviews.length === 0 && (
          <div className="text-center py-20 font-mono text-sm text-foreground/20 uppercase tracking-widest border border-dashed border-foreground/10">
            Scanning for telemetry data...
          </div>
        )}
      </div>
    </section>
  );
}
""")

    print_status("Telemetry Subsystem Fully Upgraded")

if __name__ == "__main__":
    deploy_telemetry_upgrade()
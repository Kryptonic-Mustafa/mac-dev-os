"use client";

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
    gsap.fromTo(".log-card", 
      { opacity: 0, y: 50 }, 
      { opacity: 1, y: 0, stagger: 0.1, duration: 0.8,
        scrollTrigger: { trigger: containerRef.current, start: "top 80%" }
      }
    );
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

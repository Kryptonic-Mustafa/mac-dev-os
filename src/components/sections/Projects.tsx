"use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Github, ExternalLink, Cpu } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function DeploymentMatrix() {
  const [projects, setProjects] = useState<any[]>([]);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    fetch('/api/admin/projects')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setProjects(data);
      });
  }, []);

  useGSAP(() => {
    if (projects.length === 0) return;
    
    gsap.from(".project-card", {
      y: 100,
      opacity: 0,
      duration: 1,
      stagger: 0.2,
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });
  }, [projects]);

  return (
    <section id="deploy" ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        <div className="mb-20">
          <div className="flex items-center gap-3 mb-4">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Active Deployments</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">System Matrix</h2>
        </div>

        <div className="grid grid-cols-1 gap-12">
          {projects.map((proj) => (
            <div key={proj.id} className="project-card flex flex-col md:flex-row gap-12 group">
              <div className="w-full md:w-1/3 flex flex-col gap-6">
                <div className="flex items-center gap-4 text-primary/40 font-mono text-[10px] tracking-widest uppercase">
                  <Cpu className="w-4 h-4" /> {proj.systemId}
                </div>
                <div className="flex flex-wrap gap-2">
                  {proj.tech.split(',').map((t: string) => (
                    <span key={t} className="px-3 py-1 border border-primary/20 bg-primary/5 text-primary font-mono text-[9px] uppercase tracking-widest">
                      {t.trim()}
                    </span>
                  ))}
                </div>
              </div>

              <div className="w-full md:w-2/3 border-l border-foreground/10 pl-0 md:pl-12">
                <h3 className="text-2xl md:text-3xl font-display text-foreground group-hover:text-primary transition-colors mb-4">{proj.title}</h3>
                <p className="text-foreground/60 font-sans leading-relaxed mb-8 max-w-2xl">{proj.description}</p>
                <div className="flex items-center gap-8">
                  {proj.repoLink && (
                    <a href={proj.repoLink} target="_blank" className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-foreground/40 hover:text-primary transition-colors">
                      <Github className="w-4 h-4" /> Repository
                    </a>
                  )}
                  {proj.liveLink && (
                    <a href={proj.liveLink} target="_blank" className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-primary hover:text-primary/70 transition-colors">
                      <ExternalLink className="w-4 h-4" /> Live Instance
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
          {projects.length === 0 && (
             <div className="font-mono text-sm text-foreground/30 uppercase tracking-widest py-10">No assets currently live in matrix.</div>
          )}
        </div>
      </div>
    </section>
  );
}

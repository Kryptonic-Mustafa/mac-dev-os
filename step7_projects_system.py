import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📂 M.A.C.DevOS Deployment Matrix] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_projects_system():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    print_status("Engineering GSAP ScrollTrigger Deployment Matrix")

    # 1. Projects Component
    projects_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { ExternalLink, Github, FolderGit2 } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

// System Deployment Data
const DEPLOYMENTS = [
  {
    id: "SYS-01",
    title: "Bank Management System (BMS)",
    description: "A secure, scalable financial architecture engineered for high-availability transaction processing and user account management. Deployed on high-performance edge infrastructure.",
    tech: ["React", "TypeScript", "Node.js", "Vercel"],
    link: "#",
    github: "#"
  },
  {
    id: "SYS-02",
    title: "Enterprise Bug Tracker",
    description: "Production-quality issue tracking environment featuring isolated containerization, real-time state synchronization, and strict typed data models.",
    tech: ["PHP", "Laravel", "React", "TypeScript", "Docker"],
    link: "#",
    github: "#"
  },
  {
    id: "SYS-03",
    title: "Budget Master Engine",
    description: "Advanced data visualization and financial forecasting system. Features deterministic state management and seamless cloud deployment integration.",
    tech: ["Next.js", "TailwindCSS", "Prisma", "Vercel"],
    link: "#",
    github: "#"
  }
];

export default function DeploymentMatrix() {
  const sectionRef = useRef<HTMLElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Header Reveal
    gsap.from(headerRef.current, {
      y: 40,
      opacity: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 75%",
      }
    });

    // Project Cards Stagger with Parallax feel
    if (listRef.current) {
      const projects = listRef.current.children;
      gsap.from(projects, {
        y: 80,
        opacity: 0,
        duration: 1,
        stagger: 0.2,
        ease: "expo.out",
        scrollTrigger: {
          trigger: listRef.current,
          start: "top 80%",
        }
      });
    }
  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 bg-background border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div ref={headerRef} className="mb-24">
          <div className="flex items-center gap-3 mb-4">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Active Deployments</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
            System Matrix
          </h2>
        </div>

        {/* Deployments List */}
        <div ref={listRef} className="flex flex-col gap-12">
          {DEPLOYMENTS.map((project, index) => (
            <div 
              key={project.id}
              className="group relative grid grid-cols-1 lg:grid-cols-12 gap-8 items-center border-b border-foreground/10 pb-12 hover:border-primary/50 transition-colors duration-500"
            >
              
              {/* Left Column: Metadata & Tech */}
              <div className="lg:col-span-4 flex flex-col gap-6">
                <div className="flex items-center gap-4">
                  <FolderGit2 className="w-6 h-6 text-primary opacity-70 group-hover:opacity-100 transition-opacity" />
                  <span className="font-mono text-sm text-foreground/40">{project.id}</span>
                </div>
                
                <ul className="flex flex-wrap gap-2">
                  {project.tech.map((t) => (
                    <li key={t} className="font-mono text-[10px] tracking-widest text-primary/80 uppercase px-3 py-1 bg-primary/5 border border-primary/20 rounded-sm">
                      {t}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Right Column: Details & Actions */}
              <div className="lg:col-span-8 flex flex-col gap-6 lg:pl-12 lg:border-l border-foreground/10">
                <h3 className="text-2xl md:text-3xl font-display text-foreground group-hover:text-primary transition-colors duration-300">
                  {project.title}
                </h3>
                
                <p className="font-sans text-foreground/60 leading-relaxed max-w-2xl text-sm md:text-base">
                  {project.description}
                </p>

                <div className="flex items-center gap-6 mt-2">
                  <a href={project.github} className="flex items-center gap-2 text-sm font-mono tracking-widest text-foreground/50 hover:text-foreground transition-colors uppercase">
                    <Github className="w-4 h-4" /> Repository
                  </a>
                  <a href={project.link} className="flex items-center gap-2 text-sm font-mono tracking-widest text-primary/70 hover:text-primary hover:shadow-[0_0_15px_var(--color-primary)] transition-all uppercase">
                    <ExternalLink className="w-4 h-4" /> Live Instance
                  </a>
                </div>
              </div>
              
              {/* Subtle Background Glow on Hover */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none -z-10"></div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
"""
    write_file("src/components/sections/Projects.tsx", projects_content)

    # 2. Update Home Page to Include Projects
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import DeploymentMatrix from "@/components/sections/Projects";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <DeploymentMatrix />
    </main>
  );
}
"""
    write_file("src/app/page.tsx", page_content)

    print_status("Deployment Matrix successfully integrated")

if __name__ == "__main__":
    deploy_projects_system()
import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🏗️ M.A.C.DevOS Architecture Grid] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_architecture_system():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    print_status("Engineering GSAP ScrollTrigger Architecture Grid")

    # 1. Architecture Component
    arch_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Server, Database, Shield, Cpu, Blocks, Zap } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const MODULES = [
  {
    id: "01",
    title: "Full-Stack Infrastructure",
    description: "Next.js App Router, React, and TypeScript engineered for scalable, high-concurrency environments.",
    icon: Server
  },
  {
    id: "02",
    title: "Database Architecture",
    description: "Relational data design using MySQL and TiDB, fully typed and protected via Prisma ORM.",
    icon: Database
  },
  {
    id: "03",
    title: "Motion & UI Systems",
    description: "Cinematic digital experiences powered by GSAP, Framer, and custom WebGL implementations.",
    icon: Zap
  },
  {
    id: "04",
    title: "Security Protocols",
    description: "Edge-computed middleware, strict CORS policies, and encrypted payload handling.",
    icon: Shield
  },
  {
    id: "05",
    title: "State Management",
    description: "Deterministic UI states using Zustand, Redux, and persistent local storage architectures.",
    icon: Blocks
  },
  {
    id: "06",
    title: "Performance Optimization",
    description: "Sub-second LCP, dynamic imports, and aggressive asset caching for maximum Lighthouse scores.",
    icon: Cpu
  }
];

export default function Architecture() {
  const sectionRef = useRef<HTMLElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Header Reveal
    gsap.from(headerRef.current, {
      y: 50,
      opacity: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });

    // Grid Cards Stagger
    if (gridRef.current) {
      const cards = gridRef.current.children;
      gsap.from(cards, {
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "power2.out",
        scrollTrigger: {
          trigger: gridRef.current,
          start: "top 85%",
        }
      });
    }
  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 bg-background border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div ref={headerRef} className="mb-20 flex flex-col md:flex-row md:items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
              <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Specs</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
              Core Architecture
            </h2>
          </div>
          <p className="text-foreground/50 max-w-md font-sans text-sm leading-relaxed">
            Every module is meticulously engineered to ensure maximum performance, maintainability, and visual supremacy.
          </p>
        </div>

        {/* Grid System */}
        <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {MODULES.map((mod) => (
            <div 
              key={mod.id} 
              className="group relative p-8 bg-foreground/[0.02] border border-foreground/5 hover:border-primary/50 transition-colors duration-500 overflow-hidden"
            >
              {/* Hover Glow Effect */}
              <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
              
              <div className="relative z-10 flex flex-col h-full justify-between gap-12">
                <div className="flex items-start justify-between">
                  <mod.icon className="w-8 h-8 text-primary opacity-80 group-hover:opacity-100 transition-opacity group-hover:scale-110 duration-500" />
                  <span className="font-mono text-xs text-foreground/30 group-hover:text-primary/50 transition-colors">{mod.id}</span>
                </div>
                
                <div>
                  <h3 className="text-xl font-display text-foreground mb-3">{mod.title}</h3>
                  <p className="text-sm font-sans text-foreground/60 leading-relaxed">
                    {mod.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
"""
    write_file("src/components/sections/Architecture.tsx", arch_content)

    # 2. Update Home Page to Include Architecture
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
    </main>
  );
}
"""
    write_file("src/app/page.tsx", page_content)

    print_status("Architecture Grid successfully deployed")

if __name__ == "__main__":
    deploy_architecture_system()
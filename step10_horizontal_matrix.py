import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔄 M.A.C.DevOS Horizontal Matrix] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_horizontal_matrix():
    print_status("Engineering GSAP Pinned Horizontal Scroll Section")

    # 1. System Advantages Component
    advantages_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, ShieldCheck, Activity, Layers, Cpu } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const ADVANTAGES = [
  {
    id: "ADV-01",
    title: "Sub-Second LCP",
    description: "Our architecture prioritizes immediate paint times. By leveraging Edge networks and aggressive caching, the system loads before the user even realizes.",
    icon: Zap
  },
  {
    id: "ADV-02",
    title: "Cinematic Motion",
    description: "Unlike standard templates, we utilize hardware-accelerated WebGL and GSAP pipelines to deliver fluid, 60fps animations without draining device batteries.",
    icon: Activity
  },
  {
    id: "ADV-03",
    title: "Military-Grade Security",
    description: "Strict CORS policies, encrypted payload handling, and deterministic state management ensure zero data leaks across the deployment matrix.",
    icon: ShieldCheck
  },
  {
    id: "ADV-04",
    title: "Modular Scalability",
    description: "Built on strictly typed Next.js App Routers and Prisma ORM, allowing the system to scale from 10 to 10,000,000 concurrent connections seamlessly.",
    icon: Layers
  },
  {
    id: "ADV-05",
    title: "Serverless Compute",
    description: "We bypass legacy monolithic servers. Database transactions via TiDB and Vercel Serverless Functions guarantee infinite elasticity.",
    icon: Cpu
  }
];

export default function Advantages() {
  const containerRef = useRef<HTMLElement>(null);
  const scrollTrackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!containerRef.current || !scrollTrackRef.current) return;
    
    // Disable horizontal scroll on mobile to keep a standard vertical flow
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (isMobile) return;

    const sections = gsap.utils.toArray(".horizontal-panel");
    
    gsap.to(sections, {
      xPercent: -100 * (sections.length - 1),
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        pin: true,
        scrub: 1,
        snap: 1 / (sections.length - 1),
        end: () => "+=" + scrollTrackRef.current?.offsetWidth,
      }
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative w-full overflow-hidden bg-transparent border-t border-foreground/5 z-20 md:h-screen flex items-center py-20 md:py-0">
      <div className="max-w-7xl mx-auto px-6 lg:px-12 w-full absolute top-12 md:top-24 left-0 right-0 z-10 hidden md:block pointer-events-none">
        <div className="flex items-center gap-3 mb-4">
          <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
          <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Advantages</span>
        </div>
        <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
          Why Choose M.A.C.DevOS
        </h2>
      </div>

      {/* Mobile Header (Hidden on Desktop) */}
      <div className="px-6 mb-12 md:hidden w-full">
        <div className="flex items-center gap-3 mb-4">
          <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
          <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Advantages</span>
        </div>
        <h2 className="text-4xl font-display font-medium text-foreground tracking-tight">
          Why Choose Us
        </h2>
      </div>

      {/* Horizontal Scroll Track */}
      <div ref={scrollTrackRef} className="flex flex-col md:flex-row w-full md:w-[300vw] lg:w-[250vw] h-full items-center gap-8 md:gap-0 px-6 md:px-0">
        
        {/* Placeholder panel for initial desktop scroll padding */}
        <div className="horizontal-panel hidden md:flex w-full md:w-[50vw] h-[50vh] shrink-0 items-center justify-center">
           {/* Empty space to let the header breathe before cards slide in */}
        </div>

        {ADVANTAGES.map((adv, index) => (
          <div 
            key={adv.id} 
            className="horizontal-panel w-full md:w-[40vw] lg:w-[30vw] h-auto md:h-[50vh] shrink-0 flex items-center justify-center md:px-6"
          >
            <div className="group relative p-10 bg-background/60 backdrop-blur-md border border-foreground/10 hover:border-primary/50 transition-all duration-500 w-full h-full flex flex-col justify-center">
              
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
              
              <div className="flex items-center justify-between mb-8">
                <div className="p-4 rounded-full bg-primary/5 group-hover:bg-primary/10 transition-colors border border-primary/20">
                  <adv.icon className="w-8 h-8 text-primary group-hover:scale-110 transition-transform duration-500" />
                </div>
                <span className="font-mono text-4xl font-black text-foreground/5 group-hover:text-primary/10 transition-colors duration-500">
                  0{index + 1}
                </span>
              </div>

              <h3 className="text-2xl font-display text-foreground mb-4 group-hover:text-primary transition-colors duration-300">
                {adv.title}
              </h3>
              
              <p className="font-sans text-foreground/60 leading-relaxed text-sm md:text-base">
                {adv.description}
              </p>

              <div className="mt-8 pt-6 border-t border-foreground/5 flex justify-between items-center">
                <span className="font-mono text-xs tracking-widest text-primary/50 uppercase">{adv.id}</span>
                <span className="w-2 h-2 rounded-full bg-primary/50 group-hover:bg-primary group-hover:shadow-[0_0_10px_var(--color-primary)] transition-all duration-500"></span>
              </div>
            </div>
          </div>
        ))}
        
        {/* Trailing padding */}
        <div className="horizontal-panel hidden md:flex w-full md:w-[10vw] shrink-0"></div>
      </div>
    </section>
  );
}
"""
    write_file("src/components/sections/Advantages.tsx", advantages_content)

    # 2. Update Home Page to Include Advantages
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import DeploymentMatrix from "@/components/sections/Projects";
import Advantages from "@/components/sections/Advantages";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <Advantages />
      <DeploymentMatrix />
    </main>
  );
}
"""
    write_file("src/app/page.tsx", page_content)

    print_status("Horizontal Matrix integrated successfully")

if __name__ == "__main__":
    deploy_horizontal_matrix()
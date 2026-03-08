import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚙️ M.A.C.DevOS System Protocol] {message}...")
    time.sleep(0.5)

def deploy_tech_stats_and_fixes():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    # ---------------------------------------------------------
    # 1. BULLETPROOF HORIZONTAL SCROLL FIX
    # ---------------------------------------------------------
    print_status("Deploying Bulletproof Horizontal Scroll Math")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    adv_content = """"use client";

import { useRef, useEffect } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, ShieldCheck, Activity, Layers, Cpu } from 'lucide-react';

const ADVANTAGES = [
  { id: "ADV-01", title: "Sub-Second LCP", description: "Our architecture prioritizes immediate paint times. By leveraging Edge networks and aggressive caching, the system loads before the user even realizes.", icon: Zap },
  { id: "ADV-02", title: "Cinematic Motion", description: "Unlike standard templates, we utilize hardware-accelerated WebGL and GSAP pipelines to deliver fluid, 60fps animations without draining device batteries.", icon: Activity },
  { id: "ADV-03", title: "Military-Grade Security", description: "Strict CORS policies, encrypted payload handling, and deterministic state management ensure zero data leaks across the deployment matrix.", icon: ShieldCheck },
  { id: "ADV-04", title: "Modular Scalability", description: "Built on strictly typed Next.js App Routers and Prisma ORM, allowing the system to scale from 10 to 10,000,000 concurrent connections seamlessly.", icon: Layers },
  { id: "ADV-05", title: "Serverless Compute", description: "We bypass legacy monolithic servers. Database transactions via TiDB and Vercel Serverless Functions guarantee infinite elasticity.", icon: Cpu }
];

export default function Advantages() {
  const containerRef = useRef<HTMLElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (typeof window !== "undefined") {
      gsap.registerPlugin(ScrollTrigger);
    }
    
    if (!containerRef.current || !trackRef.current) return;
    
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (isMobile) return;

    const track = trackRef.current;
    
    // Bulletproof Math: Total width of track minus the width of the screen
    const getScrollAmount = () => -(track.scrollWidth - window.innerWidth);

    const tween = gsap.to(track, {
      x: getScrollAmount,
      ease: "none",
    });

    ScrollTrigger.create({
      trigger: containerRef.current,
      start: "top top",
      end: () => `+=${track.scrollWidth - window.innerWidth}`,
      pin: true,
      animation: tween,
      scrub: 1,
      invalidateOnRefresh: true,
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative w-full h-screen flex flex-col justify-center overflow-hidden bg-transparent border-t border-foreground/5 z-20">
      
      {/* Absolute Header - Protected from overlap */}
      <div className="absolute top-[12%] md:top-[15%] left-0 w-full px-6 lg:px-12 z-10 pointer-events-none">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Advantages</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
            Why Choose M.A.C.DevOs
          </h2>
        </div>
      </div>

      {/* The Scroll Track - Exactly fits its contents */}
      <div ref={trackRef} className="flex flex-nowrap items-center gap-6 md:gap-12 w-max px-6 lg:px-12 mt-20 md:mt-32">
        {ADVANTAGES.map((adv, index) => (
          <div key={adv.id} className="w-[85vw] md:w-[40vw] lg:w-[30vw] shrink-0">
            <div className="group relative p-8 md:p-10 bg-background/60 backdrop-blur-md border border-foreground/10 hover:border-primary/50 transition-all duration-300 w-full h-[400px] flex flex-col justify-between overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
              
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className="p-3 rounded-full bg-primary/5 group-hover:bg-primary/10 transition-colors border border-primary/20">
                    <adv.icon className="w-6 h-6 md:w-8 md:h-8 text-primary group-hover:scale-110 transition-transform duration-500" />
                  </div>
                  <span className="font-mono text-3xl md:text-4xl font-black text-foreground/5 group-hover:text-primary/10 transition-colors duration-500">
                    0{index + 1}
                  </span>
                </div>
                <h3 className="text-xl md:text-2xl font-display text-foreground mb-3 group-hover:text-primary transition-colors duration-300">
                  {adv.title}
                </h3>
                <p className="font-sans text-foreground/60 leading-relaxed text-sm">
                  {adv.description}
                </p>
              </div>

              <div className="pt-4 border-t border-foreground/5 flex justify-between items-center mt-4">
                <span className="font-mono text-xs tracking-widest text-primary/50 uppercase">{adv.id}</span>
                <span className="w-2 h-2 rounded-full bg-primary/50 group-hover:bg-primary group-hover:shadow-[0_0_10px_var(--color-primary)] transition-all duration-500"></span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
"""
    with open(adv_path, "w", encoding="utf-8") as f:
        f.write(adv_content)


    # ---------------------------------------------------------
    # 2. REVIEWS HOTFIX (Ensuring Visibility)
    # ---------------------------------------------------------
    print_status("Stabilizing Telemetry Logs Trigger Points")
    reviews_path = PROJECT_PATH / "src/components/sections/Reviews.tsx"
    
    with open(reviews_path, "r", encoding="utf-8") as f:
        rev_content = f.read()
    
    # Update the start trigger to "top 95%" so it fires slightly earlier in case the pin spacer messes with it
    rev_content = rev_content.replace('start: "top 80%"', 'start: "top 95%"')
    rev_content = rev_content.replace('start: "top 85%"', 'start: "top 95%"')
    
    with open(reviews_path, "w", encoding="utf-8") as f:
        f.write(rev_content)


    # ---------------------------------------------------------
    # 3. ENGINEERING THE TECH STATS MATRIX
    # ---------------------------------------------------------
    print_status("Engineering Tech Stats Matrix Module")
    tech_path = PROJECT_PATH / "src/components/sections/TechStack.tsx"
    
    tech_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Code2, ServerCog, DatabaseZap } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const TECH_CATEGORIES = [
  {
    id: "CAT-01",
    title: "Front-End Architecture",
    icon: Code2,
    skills: [
      { name: "React.js / React Native", level: 95 },
      { name: "TypeScript / JavaScript", level: 90 },
      { name: "TailwindCSS / Bootstrap", level: 95 },
      { name: "HTML5 / CSS3 / jQuery", level: 85 }
    ]
  },
  {
    id: "CAT-02",
    title: "Back-End & Systems",
    icon: ServerCog,
    skills: [
      { name: "PHP", level: 90 },
      { name: "Laravel", level: 85 },
      { name: "Node.js", level: 75 },
    ]
  },
  {
    id: "CAT-03",
    title: "Data & Infrastructure",
    icon: DatabaseZap,
    skills: [
      { name: "MySQL", level: 90 },
      { name: "Docker", level: 80 },
      { name: "Vercel / Edge Deployments", level: 85 }
    ]
  }
];

export default function TechStack() {
  const sectionRef = useRef<HTMLElement>(null);
  const progressRefs = useRef<(HTMLDivElement | null)[]>([]);

  useGSAP(() => {
    // Animate progress bars filling up when scrolled into view
    progressRefs.current.forEach((bar) => {
      if (!bar) return;
      const targetWidth = bar.getAttribute('data-width');
      
      gsap.fromTo(bar, 
        { width: "0%" },
        {
          width: `${targetWidth}%`,
          duration: 1.5,
          ease: "power3.out",
          scrollTrigger: {
            trigger: bar,
            start: "top 90%",
          }
        }
      );
    });

    // Stagger entire categories
    gsap.from(".tech-category", {
      y: 50,
      opacity: 0,
      duration: 0.8,
      stagger: 0.2,
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });

  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div className="mb-20 flex flex-col md:flex-row md:items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
              <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Tech Specifications</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
              Operational Matrix
            </h2>
          </div>
          <p className="text-foreground/50 max-w-md font-sans text-sm leading-relaxed">
            Proficiency parameters across front-end rendering engines, server-side infrastructure, and relational database management.
          </p>
        </div>

        {/* Tech Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 md:gap-12">
          {TECH_CATEGORIES.map((category) => (
            <div key={category.id} className="tech-category flex flex-col gap-8 p-8 border border-foreground/10 bg-background/40 backdrop-blur-sm hover:border-primary/30 transition-colors duration-500">
              
              <div className="flex items-center gap-4">
                <div className="p-3 bg-primary/5 border border-primary/20 rounded-sm">
                  <category.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-display text-foreground tracking-wide">
                  {category.title}
                </h3>
              </div>

              <div className="flex flex-col gap-6">
                {category.skills.map((skill, index) => (
                  <div key={skill.name} className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="font-mono text-xs text-foreground/70 uppercase tracking-widest">{skill.name}</span>
                      <span className="font-mono text-xs text-primary/80">[{skill.level}%]</span>
                    </div>
                    {/* The Bar Track */}
                    <div className="w-full h-1.5 bg-foreground/10 overflow-hidden relative">
                      {/* The Animated Fill */}
                      <div 
                        ref={(el) => { progressRefs.current.push(el); }}
                        data-width={skill.level}
                        className="h-full bg-gradient-to-r from-primary/50 to-primary shadow-[0_0_10px_var(--color-primary)] w-0"
                      />
                    </div>
                  </div>
                ))}
              </div>

            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
"""
    with open(tech_path, "w", encoding="utf-8") as f:
        f.write(tech_content)


    # ---------------------------------------------------------
    # 4. UPDATE PAGE ARCHITECTURE
    # ---------------------------------------------------------
    print_status("Integrating Tech Stats into Main Pipeline")
    page_path = PROJECT_PATH / "src/app/page.tsx"
    
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import Advantages from "@/components/sections/Advantages";
import TechStack from "@/components/sections/TechStack";
import DeploymentMatrix from "@/components/sections/Projects";
import SystemReviews from "@/components/sections/Reviews";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <Advantages />
      <TechStack />
      <DeploymentMatrix />
      <SystemReviews />
    </main>
  );
}
"""
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(page_content)

    print_status("System Matrix successfully updated and patched")

if __name__ == "__main__":
    deploy_tech_stats_and_fixes()
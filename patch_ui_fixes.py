import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def apply_fixes():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    # ---------------------------------------------------------
    # 1. PATCH THE LOADER (Smoothness, Text, and Percentage)
    # ---------------------------------------------------------
    print_status("Optimizing Loader animations and text output")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    loader_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function Loader({ onComplete }: { onComplete: () => void }) {
  const { isMounted } = useVisualSettings();
  const containerRef = useRef<HTMLDivElement>(null);
  const percentRef = useRef<HTMLSpanElement>(null);
  const textRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!isMounted || !containerRef.current) return;

    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to(containerRef.current, {
          opacity: 0,
          duration: 0.6,
          ease: "power2.inOut",
          onComplete
        });
      }
    });

    // 1. Draw SVG Paths
    tl.fromTo(".logo-path", 
      { strokeDasharray: 1, strokeDashoffset: 1 }, 
      { strokeDashoffset: 0, duration: 1.5, stagger: 0.15, ease: "power3.inOut" }
    );

    // 2. Telemetry Percentage Counter (Fixed to true percentage without 0 padding)
    const counterObj = { val: 0 };
    tl.to(counterObj, {
      val: 100,
      duration: 1.5,
      ease: "power1.inOut",
      onUpdate: () => {
        if (percentRef.current) {
          percentRef.current.innerText = `[SYS.BOOT]: ${Math.round(counterObj.val)}%`;
        }
      }
    }, "<0.2");

    // 3. Reveal System Text (GPU Accelerated - No letterSpacing lag)
    tl.fromTo(textRef.current,
      { opacity: 0, y: 20, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power2.out" },
      "-=0.5"
    );

    tl.to({}, { duration: 0.4 });

    // 4. Undraw & Fade Out
    tl.to(".logo-path", { strokeDashoffset: -1, duration: 1, stagger: 0.1, ease: "power3.inOut" });
    tl.to([textRef.current, percentRef.current], { opacity: 0, y: -20, scale: 0.95, duration: 0.5, ease: "power2.in" }, "<0.2");

  }, [isMounted]);

  if (!isMounted) return <div className="fixed inset-0 bg-background z-[100]"></div>;

  return (
    <div ref={containerRef} className="fixed inset-0 bg-background z-[100] flex flex-col items-center justify-center overflow-hidden">
      
      <div className="relative w-32 h-32 flex items-center justify-center mb-8">
        <svg viewBox="0 0 100 100" className="w-full h-full stroke-primary fill-none stroke-[1.5] drop-shadow-[0_0_15px_var(--color-primary)]">
          <polygon points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" pathLength="1" className="logo-path" />
          <polygon points="50,20 75,35 75,65 50,80 25,65 25,35" pathLength="1" className="logo-path opacity-60" />
          <circle cx="50" cy="50" r="8" pathLength="1" className="logo-path opacity-40" />
        </svg>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-primary rounded-full blur-[10px] opacity-50"></div>
      </div>

      <div ref={textRef} className="font-display font-medium text-xl text-foreground mb-4 tracking-widest">
        M.A.C.<span className="text-primary">DevOs</span>
      </div>

      <span ref={percentRef} className="font-mono text-sm text-primary/80 tracking-widest">
        [SYS.BOOT]: 0%
      </span>

      <div className="absolute inset-0 pointer-events-none opacity-10 bg-[linear-gradient(rgba(255,255,255,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%] z-50"></div>
    </div>
  );
}
"""
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(loader_content)


    # ---------------------------------------------------------
    # 2. PATCH THE ADVANTAGES GRID (Overlap Fix & Momentum Scroll)
    # ---------------------------------------------------------
    print_status("Re-architecting Horizontal Matrix layout and momentum")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"

    adv_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, ShieldCheck, Activity, Layers, Cpu } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const ADVANTAGES = [
  { id: "ADV-01", title: "Sub-Second LCP", description: "Our architecture prioritizes immediate paint times. By leveraging Edge networks and aggressive caching, the system loads before the user even realizes.", icon: Zap },
  { id: "ADV-02", title: "Cinematic Motion", description: "Unlike standard templates, we utilize hardware-accelerated WebGL and GSAP pipelines to deliver fluid, 60fps animations without draining device batteries.", icon: Activity },
  { id: "ADV-03", title: "Military-Grade Security", description: "Strict CORS policies, encrypted payload handling, and deterministic state management ensure zero data leaks across the deployment matrix.", icon: ShieldCheck },
  { id: "ADV-04", title: "Modular Scalability", description: "Built on strictly typed Next.js App Routers and Prisma ORM, allowing the system to scale from 10 to 10,000,000 concurrent connections seamlessly.", icon: Layers },
  { id: "ADV-05", title: "Serverless Compute", description: "We bypass legacy monolithic servers. Database transactions via TiDB and Vercel Serverless Functions guarantee infinite elasticity.", icon: Cpu }
];

export default function Advantages() {
  const containerRef = useRef<HTMLElement>(null);
  const scrollTrackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!containerRef.current || !scrollTrackRef.current) return;
    
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (isMobile) return;

    const sections = gsap.utils.toArray(".horizontal-panel");
    
    gsap.to(sections, {
      xPercent: -100 * (sections.length - 1),
      ease: "none",
      scrollTrigger: {
        trigger: containerRef.current,
        pin: true,
        scrub: 1.5, // Increased for a smoother "momentum" auto-glide feel
        pinSpacing: true,
        invalidateOnRefresh: true,
        snap: {
          snapTo: 1 / (sections.length - 1),
          duration: { min: 0.3, max: 0.8 },
          delay: 0.05,
          ease: "power1.inOut"
        },
        end: () => "+=" + scrollTrackRef.current?.offsetWidth,
      }
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative w-full overflow-hidden border-t border-foreground/5 z-20 h-screen flex flex-col bg-transparent pt-24 pb-12">
      
      {/* 1. Header is now strictly part of the layout flow, preventing overlap */}
      <div className="w-full max-w-7xl mx-auto px-6 lg:px-12 shrink-0 mb-8 md:mb-16">
        <div className="flex items-center gap-3 mb-4">
          <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
          <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Advantages</span>
        </div>
        <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
          Why Choose M.A.C.DevOs
        </h2>
      </div>

      {/* 2. Scroll Track takes up the remaining flexible space */}
      <div className="flex-grow flex items-center relative w-full">
        <div ref={scrollTrackRef} className="flex flex-col md:flex-row w-full md:w-[300vw] lg:w-[250vw] items-center gap-8 md:gap-0 px-6 md:px-0">
          
          <div className="horizontal-panel hidden md:flex w-full md:w-[20vw] shrink-0"></div>

          {ADVANTAGES.map((adv, index) => (
            <div key={adv.id} className="horizontal-panel w-full md:w-[40vw] lg:w-[30vw] h-auto md:h-[400px] shrink-0 flex items-center justify-center md:px-6">
              <div className="group relative p-8 md:p-10 bg-background/60 backdrop-blur-md border border-foreground/10 hover:border-primary/50 transition-all duration-300 w-full h-full flex flex-col justify-between overflow-hidden">
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
          
          <div className="horizontal-panel hidden md:flex w-full md:w-[20vw] shrink-0"></div>
        </div>
      </div>
    </section>
  );
}
"""
    with open(adv_path, "w", encoding="utf-8") as f:
        f.write(adv_content)

    print_status("Patch deployed successfully")

if __name__ == "__main__":
    apply_fixes()
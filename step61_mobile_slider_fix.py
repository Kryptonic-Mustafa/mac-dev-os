import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📱 M.A.C.DevOS Touch UI] {message}...")
    time.sleep(0.5)

def fix_mobile_slider():
    # 1. FIX THE ADVANTAGES SLIDER (Native Swipe on Mobile, GSAP on Desktop)
    print_status("Rewriting Advantages.tsx for Native Mobile Swiping (GSAP matchMedia)")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    adv_content = """"use client";
import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, Activity, Shield, Cpu } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function Advantages() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sliderRef = useRef<HTMLDivElement>(null);

  const advantages = [
    { icon: Zap, title: "Sub-Second LCP", desc: "Our architecture prioritizes immediate paint times. Edge networks and aggressive caching mean the system loads before the user realizes.", id: "01" },
    { icon: Activity, title: "Cinematic Motion", desc: "Hardware-accelerated WebGL and GSAP pipelines deliver fluid, 60fps animations without draining device batteries.", id: "02" },
    { icon: Shield, title: "Military-Grade Security", desc: "Strict CORS policies, encrypted payloads, and deterministic state management ensure zero data leaks.", id: "03" },
    { icon: Cpu, title: "Edge Computing", desc: "Distributed serverless functions ensure your portfolio is executed physically closer to the user, eliminating latency.", id: "04" }
  ];

  useGSAP(() => {
    // matchMedia is the secret weapon: It applies different GSAP rules based on screen size
    let mm = gsap.matchMedia();

    // DESKTOP ONLY: Apply the pinned horizontal scroll
    mm.add("(min-width: 768px)", () => {
      let sections = gsap.utils.toArray(".adv-card");
      gsap.to(sections, {
        xPercent: -100 * (sections.length - 1),
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          pin: true,
          scrub: 1,
          snap: 1 / (sections.length - 1),
          // Calculate the exact width needed to scroll
          end: () => "+=" + sliderRef.current?.offsetWidth
        }
      });
    });

    // MOBILE (max-width: 767px): GSAP does absolutely nothing. 
    // We let the native CSS overflow-x-auto handle the touch swiping!

    return () => mm.revert(); // Automatically cleans up when resizing
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="py-20 bg-background text-foreground overflow-hidden">
      <div className="container mx-auto px-4 mb-10">
        <h2 className="text-sm font-mono text-primary mb-2 uppercase tracking-widest flex items-center gap-2">
          <span className="w-8 h-[1px] bg-primary"></span> System Advantages
        </h2>
        <h3 className="text-4xl md:text-5xl font-display">Why Choose M.A.C.DevOS</h3>
      </div>

      <div className="pl-4 md:pl-0">
        {/* MOBILE CSS: overflow-x-auto, touch-pan-x, and snap-x create a perfect native slider */}
        {/* DESKTOP CSS: flex-nowrap and w-max allow GSAP to translate the whole row */}
        <div
          ref={sliderRef}
          className="flex gap-6 md:gap-8 w-max md:w-[200vw] overflow-x-auto md:overflow-visible snap-x snap-mandatory touch-pan-x pb-8 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none] pr-4 md:pr-0"
        >
          {advantages.map((adv, i) => (
            <div
              key={i}
              className="adv-card w-[85vw] md:w-[45vw] lg:w-[30vw] flex-shrink-0 snap-center bg-background border border-foreground/10 p-8 md:p-12 relative group hover:border-primary/50 transition-colors"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/0 via-primary to-primary/0 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="flex justify-between items-start mb-8">
                <div className="p-4 rounded-full bg-primary/10 text-primary border border-primary/20">
                  <adv.icon className="w-8 h-8" />
                </div>
                <span className="text-4xl font-display text-foreground/10 font-bold">{adv.id}</span>
              </div>
              <h4 className="text-2xl font-display mb-4">{adv.title}</h4>
              <p className="text-foreground/50 leading-relaxed">{adv.desc}</p>
              <div className="mt-8 pt-8 border-t border-foreground/5 flex justify-between items-center text-xs font-mono text-foreground/30">
                <span>ADV-{adv.id}</span>
                <span className="w-2 h-2 rounded-full bg-primary/50 group-hover:bg-primary transition-colors shadow-[0_0_10px_rgba(0,255,128,0)] group-hover:shadow-[0_0_10px_rgba(0,255,128,0.8)]"></span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
"""
    with open(adv_path, "w", encoding="utf-8") as f:
        f.write(adv_content)

    # 2. FIX THE SPIDER CURSOR (CSS-based mobile hiding)
    print_status("Hardcoding Cursor removal on Mobile devices")
    cursor_path = PROJECT_PATH / "src/components/ui/CustomCursor.tsx"
    
    cursor_content = """"use client";
import { useState, useEffect, useRef } from 'react';

export default function CustomCursor() {
  const [mounted, setMounted] = useState(false);
  const cursorDot = useRef<HTMLDivElement>(null);
  const cursorRing = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    const moveCursor = (e: MouseEvent) => {
      if (cursorDot.current && cursorRing.current) {
        cursorDot.current.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        cursorRing.current.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
      }
    };
    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, []);

  if (!mounted) return null;

  return (
    // The 'hidden md:block' ensures this entire DOM tree is vaporized on mobile screens
    <div className="hidden md:block pointer-events-none">
      <div ref={cursorDot} className="fixed top-0 left-0 w-1.5 h-1.5 bg-primary rounded-full z-[999] -translate-x-1/2 -translate-y-1/2 transition-transform duration-75 ease-out" />
      <div ref={cursorRing} className="fixed top-0 left-0 w-8 h-8 border border-primary/30 rounded-full z-[998] -translate-x-1/2 -translate-y-1/2 transition-transform duration-300 ease-out" />
    </div>
  );
}
"""
    with open(cursor_path, "w", encoding="utf-8") as f:
        f.write(cursor_content)

    print_status("Touch UI Matrix successfully deployed.")

if __name__ == "__main__":
    fix_mobile_slider()
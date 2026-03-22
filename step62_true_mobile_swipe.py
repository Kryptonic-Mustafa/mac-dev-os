import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔓 M.A.C.DevOS Unlocked] {message}...")
    time.sleep(0.5)

def deploy_true_swipe():
    print_status("Releasing touch locks and injecting mobile swipe indicators")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        # We are rewriting the file to ensure the ArrowRight icon is imported 
        # and all touch-blocking CSS is eradicated.
        adv_content = """"use client";
import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, Activity, Shield, Cpu, ArrowRight } from 'lucide-react';

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
    let mm = gsap.matchMedia();

    // DESKTOP ONLY: GSAP controls the scroll
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
          end: () => "+=" + sliderRef.current?.offsetWidth
        }
      });
    });

    return () => mm.revert();
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="py-20 bg-background text-foreground overflow-hidden">
      <div className="container mx-auto px-4 mb-6">
        <h2 className="text-sm font-mono text-primary mb-2 uppercase tracking-widest flex items-center gap-2">
          <span className="w-8 h-[1px] bg-primary"></span> System Advantages
        </h2>
        <h3 className="text-4xl md:text-5xl font-display mb-4">Why Choose M.A.C.DevOS</h3>
        
        {/* MOBILE ONLY: Visual cue to swipe */}
        <div className="md:hidden flex items-center text-xs font-mono text-primary/70 animate-pulse mt-2">
          <span>Swipe matrix to explore</span>
          <ArrowRight className="w-4 h-4 ml-2" />
        </div>
      </div>

      <div className="pl-4 md:pl-0">
        {/* CRITICAL FIXES: 
            1. Removed 'touch-pan-x' to allow natural vertical scrolling past the section.
            2. Removed scrollbar hiding classes so the native scroll track appears on mobile.
            3. Added 'touch-auto' to explicitly tell browsers not to restrict finger movement.
        */}
        <div
          ref={sliderRef}
          className="flex gap-6 md:gap-8 w-max md:w-[200vw] overflow-x-auto md:overflow-visible snap-x snap-mandatory pb-8 pr-4 md:pr-0 touch-auto"
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
        print_status("Mobile swiping restrictions removed. Visual cues added.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    deploy_true_swipe()
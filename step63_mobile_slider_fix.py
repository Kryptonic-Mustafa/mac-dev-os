import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📱 M.A.C.DevOS Touch UI] {message}...")
    time.sleep(0.5)

def deploy_mobile_touch_fix():
    print_status("Hardening Advantages.tsx with GSAP Observer touch binding and custom scroll UI")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        # We are completely rewriting this file to implement the custom indicator and Observer logic.
        adv_content = """"use client";
import { useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
# import { ScrollToPlugin } from 'gsap/ScrollToPlugin'; // Optional, for clicking indicator
import { Zap, Activity, Shield, Cpu, ArrowRight } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export default function Advantages() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sliderRef = useRef<HTMLDivElement>(null);
  const indicatorRef = useRef<HTMLDivElement>(null); // New ref for custom scrollbar
  const [progress, setProgress] = useState(0); // Track progress for the modern UI indicator

  const advantages = [
    { icon: Zap, title: "Sub-Second LCP", desc: "Our architecture prioritizes immediate paint times. Edge networks and aggressive caching mean the system loads before the user realizes.", id: "01" },
    { icon: Activity, title: "Cinematic Motion", desc: "Hardware-accelerated WebGL and GSAP pipelines deliver fluid, 60fps animations without draining device batteries.", id: "02" },
    { icon: Shield, title: "Military-Grade Security", desc: "Strict CORS policies, encrypted payloads, and deterministic state management ensure zero data leaks.", id: "03" },
    { icon: Cpu, title: "Edge Computing", desc: "Distributed serverless functions ensure your portfolio is executed physically closer to the user, eliminating latency.", id: "04" }
  ];

  useGSAP(() => {
    let mm = gsap.matchMedia();

    // DESKTOP ONLY: Cinematic vertical-pin-to-horizontal-scrub logic
    mm.add("(min-width: 768px)", () => {
      let sections = gsap.utils.toArray(".adv-card");
      const totalWidth = sliderRef.current?.offsetWidth || 0;
      
      gsap.to(sections, {
        xPercent: -100 * (sections.length - 1),
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          pin: true,
          scrub: 1,
          snap: 1 / (sections.length - 1),
          end: () => "+=" + totalWidth,
          // Link the progress state to the scroll progress for desktop feedback
          onUpdate: (self) => setProgress(Math.round(self.progress * 100))
        }
      });
    });

    // MOBILE ONLY (< 768px): Explicit touch and drag events via GSAP Observer
    mm.add("(max-width: 767px)", () => {
      const slider = sliderRef.current;
      const totalCards = advantages.length;
      const cardWidth = 0.85 * window.innerWidth; // w-[85vw] from Tailwind
      const gap = 24; // gap-6 from Tailwind (24px)
      const maxScroll = (totalCards * cardWidth) + ((totalCards - 1) * gap) - window.innerWidth;

      // Ensure the container handles touch safely
      gsap.set(slider, { x: 0, userSelect: 'none', touchAction: 'none' });

      let currentX = 0;
      let targetX = 0;

      // Handle the touch/drag movement
      gsap.addObserver({
        target: containerRef.current,
        type: "touch,pointer",
        onChangeX: (self) => {
          targetX += self.deltaX * 1.5; // Amplify the drag for mobile feel
          targetX = gsap.utils.clamp(-maxScroll, 0, targetX); // Prevent scrolling past start/end

          // Buttery smooth inertia effect
          gsap.to(slider, {
            x: targetX,
            ease: "expo.out",
            duration: 0.5,
            overwrite: 'auto',
            onUpdate: () => {
              const currentProgress = gsap.utils.normalize(0, -maxScroll, sliderRef.current?.style.transform.match(/translate\(([-\\d.]+)/)?.[1] || 0);
              setProgress(Math.round(currentProgress * 100));
            }
          });
        },
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
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 md:gap-0">
          <h3 className="text-4xl md:text-5xl font-display">Why Choose M.A.C.DevOS</h3>
          
          {/* 📱 MODERN MOBILE UI: Horizontal Scroll indicator */}
          <div className="md:hidden flex flex-col gap-2 mt-2 w-full max-w-[200px] border border-foreground/5 p-4 bg-background/50 backdrop-blur-sm">
            <div className="flex items-center text-xs font-mono text-primary/70 animate-pulse">
                <span>Touch/Drag matrix to explore</span>
                <ArrowRight className="w-4 h-4 ml-2" />
            </div>
            
            {/* The actual modern scrollbar track and indicator */}
            <div className="relative w-full h-1 bg-foreground/10 rounded-full overflow-hidden mt-1">
              <div 
                ref={indicatorRef} 
                className="absolute top-0 left-0 h-full bg-primary rounded-full shadow-[0_0_10px_rgba(0,255,128,0.6)]"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="text-[9px] font-mono text-foreground/30 text-center">[ {progress}% DEPLOYED ]</div>
          </div>
        </div>
      </div>

      <div className="pl-4 md:pl-0">
        {/* MOBILE CSS: 
            1. flex-nowrap: critical for the horizontal layout.
            2. user-select-none and touch-action-none: ensures GSAP Observer takes full control of the touch events.
            3. removed all previous browser-native 'overflow' and 'snap' logic.
        */}
        <div
          ref={sliderRef}
          className="flex gap-6 md:gap-8 w-max md:w-[200vw] flex-nowrap md:flex-nowrap pr-4 md:pr-0 user-select-none touch-action-none"
        >
          {advantages.map((adv, i) => (
            <div
              key={i}
              className="adv-card w-[85vw] md:w-[45vw] lg:w-[30vw] flex-shrink-0 bg-background border border-foreground/10 p-8 md:p-12 relative group hover:border-primary/50 transition-colors"
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
        print_status("Custom touch events and scroll progress UI successfully implemented.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    deploy_mobile_touch_fix()
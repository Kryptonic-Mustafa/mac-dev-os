import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚙️ M.A.C.DevOS Boot Protocol] {message}...")
    time.sleep(0.5)

def update_loader():
    print_status("Engineering Signature SVG Draw/Undraw Loader with Telemetry")

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
        // Clean unmount
        gsap.to(containerRef.current, {
          opacity: 0,
          duration: 0.6,
          ease: "power2.inOut",
          onComplete
        });
      }
    });

    // 1. Draw SVG Paths (Creates the logo)
    tl.fromTo(".logo-path", 
      { strokeDasharray: 1, strokeDashoffset: 1 }, 
      { strokeDashoffset: 0, duration: 1.5, stagger: 0.15, ease: "power3.inOut" }
    );

    // 2. Telemetry Percentage Counter (Hackery feel)
    const counterObj = { val: 0 };
    tl.to(counterObj, {
      val: 100,
      duration: 1.5,
      ease: "power1.inOut",
      onUpdate: () => {
        if (percentRef.current) {
          // Formats as [SYS.BOOT]: 045%
          percentRef.current.innerText = `[SYS.BOOT]: ${Math.round(counterObj.val).toString().padStart(3, '0')}%`;
        }
      }
    }, "<0.2"); // Starts slightly after the SVG drawing begins

    // 3. Reveal System Text
    tl.fromTo(textRef.current,
      { opacity: 0, y: 10, letterSpacing: "0px" },
      { opacity: 1, y: 0, letterSpacing: "8px", duration: 0.8, ease: "power2.out" },
      "-=0.5"
    );

    // 4. Brief Pause at 100% for impact
    tl.to({}, { duration: 0.4 });

    // 5. Undraw Paths (Uncreates the logo)
    tl.to(".logo-path", { strokeDashoffset: -1, duration: 1, stagger: 0.1, ease: "power3.inOut" });
    
    // 6. Fade out Text & Counter
    tl.to([textRef.current, percentRef.current], { opacity: 0, y: -10, duration: 0.5, ease: "power2.in" }, "<0.2");

  }, [isMounted]);

  if (!isMounted) return <div className="fixed inset-0 bg-background z-[100]"></div>;

  return (
    <div ref={containerRef} className="fixed inset-0 bg-background z-[100] flex flex-col items-center justify-center overflow-hidden">
      
      {/* SVG Container */}
      <div className="relative w-32 h-32 flex items-center justify-center mb-8">
        <svg viewBox="0 0 100 100" className="w-full h-full stroke-primary fill-none stroke-[1.5] drop-shadow-[0_0_15px_var(--color-primary)]">
          {/* Outer Hexagon */}
          <polygon 
            points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" 
            pathLength="1" 
            className="logo-path" 
          />
          {/* Inner Hexagon */}
          <polygon 
            points="50,20 75,35 75,65 50,80 25,65 25,35" 
            pathLength="1" 
            className="logo-path opacity-60" 
          />
          {/* Core Target Circle */}
          <circle 
            cx="50" 
            cy="50" 
            r="8" 
            pathLength="1" 
            className="logo-path opacity-40" 
          />
        </svg>
        
        {/* Glow Core */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-primary rounded-full blur-[10px] opacity-50"></div>
      </div>

      {/* Brand Text */}
      <div ref={textRef} className="font-display font-medium text-xl text-foreground mb-4 uppercase tracking-widest">
        M.A.C.<span className="text-primary">DevOS</span>
      </div>

      {/* Percentage Counter */}
      <span ref={percentRef} className="font-mono text-sm text-primary/80 tracking-widest">
        [SYS.BOOT]: 000%
      </span>

      {/* Subtle Scanline Overlay specific to the loader */}
      <div className="absolute inset-0 pointer-events-none opacity-10 bg-[linear-gradient(rgba(255,255,255,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%] z-50"></div>
    </div>
  );
}
"""
    
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(loader_content)

    print_status("Loader successfully upgraded to Signature SVG Engine")

if __name__ == "__main__":
    update_loader()
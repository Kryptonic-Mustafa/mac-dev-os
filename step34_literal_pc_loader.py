import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🖥️ M.A.C.DevOS Clean Loader] {message}...")
    time.sleep(0.5)

def deploy_clean_loader():
    print_status("Purging Glitch & Engineering CSS Monitor Scene")
    
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    loader_content = """"use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { MousePointer2 } from 'lucide-react';

export default function Loader({ onComplete }: { onComplete?: () => void }) {
  const [progress, setProgress] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const monitorRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const bootTextRef = useRef<HTMLDivElement>(null);
  const nameTextRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Lock scrolling while booting
    document.body.style.overflow = 'hidden';

    const tl = gsap.timeline({
      onComplete: () => {
        document.body.style.overflow = 'auto'; // Unlock scroll
        if (onComplete) onComplete();
      }
    });

    // 1. Initial Monitor Fade In
    tl.from(monitorRef.current, { opacity: 0, scale: 0.9, duration: 0.8, ease: "power2.out" });

    // 2. Mouse Glides in from bottom right to the center (over the button)
    tl.fromTo(mouseRef.current, 
      { x: 120, y: 120, opacity: 0 },
      { x: 0, y: 10, opacity: 1, duration: 1.2, ease: "power3.out" }
    );

    // 3. The Click Interaction
    tl.to(mouseRef.current, { scale: 0.8, duration: 0.1 }) // Press down
      .to(buttonRef.current, { scale: 0.9, backgroundColor: "rgba(0, 255, 128, 0.2)", duration: 0.1 })
      .to(mouseRef.current, { scale: 1, duration: 0.1 }) // Release
      .to(buttonRef.current, { scale: 1, duration: 0.1 });

    // 4. Hide mouse and button
    tl.to([mouseRef.current, buttonRef.current], { opacity: 0, duration: 0.3, display: "none" });

    // 5. Show Boot Percentage inside screen
    tl.to(bootTextRef.current, { opacity: 1, duration: 0.3 });
    
    const dummy = { val: 0 };
    tl.to(dummy, {
      val: 100,
      duration: 2, // Loading duration
      ease: "power1.inOut",
      onUpdate: () => setProgress(Math.round(dummy.val))
    });

    // 6. Hide Boot Text, Show M.A.C.DevOS
    tl.to(bootTextRef.current, { opacity: 0, duration: 0.2, display: "none" })
      .to(nameTextRef.current, { opacity: 1, scale: 1.1, duration: 0.5, ease: "back.out(1.5)" });

    // 7. THE DIVE: Massive scale up to dive "into" the screen
    tl.to(monitorRef.current, {
      scale: 40, // Scaled massively so the inside of the CSS screen covers the viewport
      opacity: 0,
      duration: 1.2,
      ease: "power4.inOut"
    }, "+=0.4")
    .set(containerRef.current, { display: "none" });

    return () => tl.kill(); // Cleanup
  }, [onComplete]);

  return (
    <div ref={containerRef} className="fixed inset-0 z-[100] flex items-center justify-center bg-black overflow-hidden selection:bg-none">
      
      {/* THE LITERAL PC */}
      <div ref={monitorRef} className="relative flex flex-col items-center origin-center">
        
        {/* The Monitor Screen Frame */}
        <div className="w-[300px] h-[220px] border-8 border-foreground/20 rounded-xl bg-[#050505] relative overflow-hidden flex items-center justify-center shadow-[0_0_50px_rgba(0,0,0,0.5)]">
          
          {/* Phase 1: Launch Button */}
          <button ref={buttonRef} className="px-5 py-2 border border-primary/50 text-primary font-mono text-[10px] uppercase tracking-widest relative z-10 transition-colors bg-primary/5">
            Launch System
          </button>

          {/* Phase 2: Boot Counter */}
          <div ref={bootTextRef} className="absolute inset-0 flex items-center justify-center opacity-0 font-mono text-primary text-sm tracking-widest z-10">
            [SYS.BOOT]: {progress}%
          </div>

          {/* Phase 3: Brand Name */}
          <div ref={nameTextRef} className="absolute inset-0 flex items-center justify-center opacity-0 z-10">
            <span className="font-display font-bold text-white tracking-[0.2em] text-2xl uppercase drop-shadow-[0_0_10px_rgba(255,255,255,0.3)]">
              M.A.C.DevOS
            </span>
          </div>

          {/* The Ghost Mouse Cursor */}
          <div ref={mouseRef} className="absolute z-30 top-1/2 left-1/2 text-white pointer-events-none drop-shadow-[0_4px_4px_rgba(0,0,0,0.8)]">
            <MousePointer2 className="w-6 h-6 fill-white" />
          </div>

          {/* Optional CRT Scanline effect purely for aesthetics inside the screen */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:100%_4px] pointer-events-none opacity-20"></div>
        </div>
        
        {/* The Monitor Stand */}
        <div className="w-20 h-10 border-x-8 border-b-8 border-foreground/20 rounded-b-lg opacity-80"></div>
        <div className="w-40 h-3 bg-foreground/20 rounded-full mt-1 opacity-80"></div>
      
      </div>

    </div>
  );
}
"""
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(loader_content)

    print_status("Literal PC Dive loader successfully deployed")

if __name__ == "__main__":
    deploy_clean_loader()
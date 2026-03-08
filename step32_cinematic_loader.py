import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📺 M.A.C.DevOS Boot Sequence] {message}...")
    time.sleep(0.5)

def deploy_cinematic_loader():
    print_status("Engineering CRT TV Switch-On Animation")
    
    # We will overwrite your existing Loader component. 
    # Usually, this is in src/components/ui/Loader.tsx or src/components/Loader.tsx
    # We will create it in ui/Loader.tsx and you can adjust the import if needed.
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    os.makedirs(loader_path.parent, exist_ok=True)
    
    loader_content = """"use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';

export default function Loader({ onComplete }: { onComplete?: () => void }) {
  const [progress, setProgress] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const lineRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Lock scrolling while booting
    document.body.style.overflow = 'hidden';

    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        onComplete: () => {
          document.body.style.overflow = 'auto'; // Unlock scroll
          if (onComplete) onComplete();
        }
      });

      // 1. TV Line expands horizontally (The Spark)
      tl.to(lineRef.current, { width: "100vw", duration: 0.2, ease: "power4.in" })
        
        // 2. Line expands vertically to fill screen (The Flash)
        .to(lineRef.current, { height: "100vh", duration: 0.25, ease: "power2.out" })
        
        // 3. Fade out the white flash to reveal dark OS background
        .to(lineRef.current, { opacity: 0, duration: 0.15 })
        
        // 4. Reveal the text and counter
        .fromTo(contentRef.current,
          { opacity: 0, scale: 0.8 },
          { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.5)" },
          "-=0.1"
        );

      // 5. Run the boot percentage (0 to 100%)
      const dummy = { val: 0 };
      tl.to(dummy, {
        val: 100,
        duration: 1.8, // Adjust this to make loading faster or slower
        ease: "power1.inOut",
        onUpdate: () => setProgress(Math.round(dummy.val))
      });

      // 6. The "Dive In" Zoom effect
      tl.to(contentRef.current, { scale: 2.5, opacity: 0, duration: 0.4, ease: "power3.in" })
        .to(containerRef.current, { scale: 4, opacity: 0, duration: 0.6, ease: "power3.in" }, "-=0.2")
        .set(containerRef.current, { display: "none" });

    }, containerRef);

    return () => ctx.revert(); // Cleanup GSAP on unmount
  }, [onComplete]);

  return (
    <div ref={containerRef} className="fixed inset-0 z-[100] flex items-center justify-center bg-black overflow-hidden origin-center">
      {/* Dark OS Background Layer */}
      <div className="absolute inset-0 bg-[#050505]" />

      {/* TV CRT Flash Line */}
      <div ref={lineRef} className="absolute bg-white w-0 h-[2px] shadow-[0_0_30px_rgba(255,255,255,1)] z-10 origin-center" />

      {/* Boot Sequence Content */}
      <div ref={contentRef} className="relative z-20 flex flex-col items-center gap-6 opacity-0">
        <h1 className="text-4xl md:text-6xl font-display font-bold text-white tracking-[0.2em] uppercase drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">
          M.A.C.DevOS
        </h1>
        <div className="flex items-center gap-3">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
          <span className="font-mono text-primary text-xl md:text-2xl tracking-[0.3em] uppercase">
            [SYS.BOOT]: {progress}%
          </span>
        </div>
      </div>
    </div>
  );
}
"""
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(loader_content)

    print_status("Cinematic GSAP Boot Engine successfully integrated")

if __name__ == "__main__":
    deploy_cinematic_loader()
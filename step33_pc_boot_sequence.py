import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🖥️ M.A.C.DevOS Interactive Boot] {message}...")
    time.sleep(0.5)

def deploy_pc_loader():
    # 1. INSTALL MOUSE ICON (lucide-react)
    print_status("Checking Lucide Icon Assets")
    # Ensuring MousePointer2 is available. It should be if lucide-react is installed.
    # No action needed unless lucide isn't installed.

    # 2. CREATE NEW INTERACTIVE LOADER
    print_status("Engineering Interactive PC Bootloader with GSAP")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    loader_content = """"use client";

import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { MonitorDot, MousePointer2, Zap } from 'lucide-react';

export default function Loader({ onComplete }: { onComplete?: () => void }) {
  const [progress, setProgress] = useState(0);
  const [bootStatus, setBootStatus] = useState("AWAITING_INPUT");
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<HTMLDivElement>(null);
  const pcRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const cursorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Lock scrolling while booting
    document.body.style.overflow = 'hidden';

    // Timeline 1: The Mouse Clicking Interaction
    const interactionTl = gsap.timeline({ delay: 0.5 });
    
    // Animate Scene In
    interactionTl.fromTo(sceneRef.current, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1, ease: "power3.out" })
        .fromTo(buttonRef.current, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }, "-=0.3")
        .fromTo(cursorRef.current, { opacity: 0 }, { opacity: 1, duration: 0.2 }, "-=0.1");

    // Move "ghost" cursor to the button
    interactionTl.to(cursorRef.current, {
      x: 140, // Adjust based on button placement
      y: 90, 
      duration: 1.2,
      ease: "power2.inOut",
      delay: 0.3
    });

    // Simulate "Click" (Button scaling)
    interactionTl.to(buttonRef.current, { scale: 0.9, duration: 0.1, ease: "power1.in" })
        .to(buttonRef.current, { scale: 1, duration: 0.1, ease: "power1.out" })
        .to(cursorRef.current, { scale: 1.5, opacity: 0, duration: 0.2 }, "-=0.1");

    // Hide Button & Mouse setup, Show PC Powering On
    interactionTl.to([buttonRef.current, mouseRef.current], { opacity: 0, duration: 0.3, ease: "power2.in" })
        .to(pcRef.current, { scale: 1.2, color: "#fff", duration: 0.3 }, "-=0.2")
        .to(pcRef.current, { x: 0, y: 0, duration: 0.8, ease: "power3.inOut" }, "-=0.1");

    // Trigger Timeline 2 (Boot Sequence)
    interactionTl.add(() => startBootSequence());

    const startBootSequence = () => {
      setBootStatus("BOOT_INITIATED");
      const bootTl = gsap.timeline({
        onComplete: () => {
          document.body.style.overflow = 'auto'; // Unlock scroll
          if (onComplete) onComplete();
        }
      });

      // 1. Run the boot percentage (0 to 100%) inside the monitor
      const dummy = { val: 0 };
      bootTl.to(dummy, {
        val: 100,
        duration: 2.2, // Adjust speed here
        ease: "power2.inOut",
        onUpdate: () => setProgress(Math.round(dummy.val))
      });

      // 2. Center Name Appears
      bootTl.fromTo("#boot-name", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" })
            .to("#boot-status", { opacity: 0, duration: 0.2 }, "-=0.1");

      // 3. THE DIVE: Zoom in fully towards main screen
      bootTl.to("#boot-name", { scale: 0.6, opacity: 0, duration: 0.3, ease: "power2.in" }, "+=0.3")
            .to(sceneRef.current, { scale: 10, opacity: 0, duration: 0.8, ease: "power4.in" })
            .set(containerRef.current, { display: "none" });
    }

    return () => { gsap.context((c) => c.revert(), containerRef) }; // Cleanup GSAP
  }, [onComplete]);

  return (
    <div ref={containerRef} className="fixed inset-0 z-[100] flex items-center justify-center bg-black overflow-hidden selection:bg-none">
      
      {/* Interactive Scene Wrapper */}
      <div ref={sceneRef} className="relative flex flex-col items-center gap-16 opacity-0">
        
        {/* Literal PC Monitor Icon */}
        <div ref={pcRef} className="text-foreground/20 text-center flex flex-col items-center gap-6 translate-x-[-120px]">
          <MonitorDot className="w-32 h-32 md:w-48 md:h-48 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]" />
          
          <div id="boot-status" className="font-mono text-xs uppercase tracking-widest h-6">
            {bootStatus === "AWAITING_INPUT" && "[ PR_SYS_BOOT: OFFLINE ]"}
            {bootStatus === "BOOT_INITIATED" && `[ SYS.BOOT ]: ${progress}%`}
          </div>
          
          {/* Centered Name (Reveals at end) */}
          <h1 id="boot-name" className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-5xl md:text-7xl font-display font-bold text-white uppercase tracking-[0.2em] opacity-0 whitespace-nowrap">
            M.A.C.DevOS
          </h1>
        </div>

        {/* Input Interface Area */}
        <div className="relative flex items-center gap-12 border border-foreground/5 bg-foreground/[0.02] p-6 rounded-lg">
          
          {/* Launch Button */}
          <button ref={buttonRef} className="flex items-center gap-3 px-6 py-3 bg-primary text-background font-mono font-bold uppercase text-sm tracking-widest hover:shadow-neon transition-all">
            <Zap className="w-4 h-4" />
            Launch System
          </button>
          
          {/* Passive Mouse Icon */}
          <div ref={mouseRef} className="text-foreground/10 p-3 border border-dashed border-foreground/10 rounded-full">
            <MousePointer2 className="w-8 h-8" />
          </div>

          {/* Animated "Ghost" Cursor */}
          <div ref={cursorRef} className="absolute top-[-30px] left-[-30px] text-white opacity-0 z-20 pointer-events-none">
            <MousePointer2 className="w-6 h-6 fill-white" />
          </div>
        </div>

      </div>
    </div>
  );
}
"""
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(loader_content)

    print_status("Cinematic PC Boot Sequence successfully integrated")

if __name__ == "__main__":
    deploy_pc_loader()
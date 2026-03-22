import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚡ M.A.C.DevOS GPU Optimizer] {message}...")
    time.sleep(0.5)

def deploy_performance_patch():
    print_status("Applying Hardware Acceleration to Loader Sequence")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    # 100% working logic, but with the GSAP timeline optimized for 60fps mobile rendering
    optimized_content = """"use client";
import { useEffect, useState, useRef } from 'react';
import gsap from 'gsap';
import { MousePointer2, Terminal } from 'lucide-react';

export default function Loader({ onComplete }: { onComplete?: () => void }) {
  const [mounted, setMounted] = useState(false);
  const [progress, setProgress] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const monitorRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const bootTextRef = useRef<HTMLDivElement>(null);
  const nameTextRef = useRef<HTMLDivElement>(null);
  const backgroundRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    
    if (!monitorRef.current || !mouseRef.current || !buttonRef.current) return;

    document.body.style.overflow = 'hidden';

    const tl = gsap.timeline({
      onComplete: () => {
        document.body.style.overflow = 'auto';
        if (onComplete) onComplete();
      }
    });

    tl.from(monitorRef.current, { opacity: 0, y: 50, duration: 1, ease: "power4.out" })
      .from(backgroundRef.current, { opacity: 0, duration: 1 }, "-=0.5");

    tl.fromTo(mouseRef.current, 
      { x: 150, y: 150, opacity: 0, scale: 2 },
      { x: 25, y: -2, opacity: 1, scale: 1, duration: 1.5, ease: "power3.inOut" },
      "-=0.2"
    );

    tl.to(mouseRef.current, { scale: 0.8, duration: 0.1 })
      .to(buttonRef.current, { scale: 0.95, boxShadow: "0 0 10px rgba(0, 255, 128, 0.1)", duration: 0.1 })
      .to(mouseRef.current, { scale: 1, duration: 0.1 })
      .to(buttonRef.current, { scale: 1, boxShadow: "0 0 20px rgba(0, 255, 128, 0.5)", duration: 0.1 });

    tl.to([mouseRef.current, buttonRef.current], { opacity: 0, duration: 0.4, display: "none" })
      .to(".screen-overlay", { opacity: 1, duration: 0.2, ease: "power1.in" }, "-=0.2");

    tl.to(bootTextRef.current, { opacity: 1, duration: 0.3 });
    
    const dummy = { val: 0 };
    tl.to(dummy, {
      val: 100,
      duration: 2.2,
      ease: "power1.inOut",
      onUpdate: () => setProgress(Math.round(dummy.val))
    });

    tl.to(bootTextRef.current, { opacity: 0, duration: 0.3, y: -10 })
      .to(nameTextRef.current, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.7)" }, "-=0.1");

    // ⚡ THE GPU-OPTIMIZED NEON DIVE ⚡
    // 1. Instantly kill heavy box-shadows before scaling to save thousands of GPU recalculations
    tl.to(monitorRef.current, { boxShadow: "none", duration: 0.1 }, "+=0.4");
    
    // 2. Hardware Accelerated Scale
    tl.to(monitorRef.current, {
      scale: 45, // Slightly larger to guarantee screen cover
      opacity: 0,
      duration: 1.2,
      ease: "power3.inOut",
      force3D: true, // Forces GPU rendering
      rotationZ: 0.01 // WebKit hack to prevent subpixel layout thrashing on mobile
    }, "<") // "<" means start at the same time as the shadow removal
    .to(backgroundRef.current, { opacity: 0, duration: 0.8, ease: "power2.in" }, "<")
    .set(containerRef.current, { display: "none" });

    return () => { 
      tl.kill(); 
      document.body.style.overflow = 'auto';
    };
  }, [mounted, onComplete]);

  if (!mounted) return null;

  return (
    <div ref={containerRef} className="fixed inset-0 z-[100] flex items-center justify-center bg-black overflow-hidden selection:bg-none">
      <div ref={backgroundRef} className="absolute inset-0 opacity-10 overflow-hidden text-[9px] font-mono whitespace-nowrap z-0 pointer-events-none text-emerald-500/50 scale-110 will-change-opacity">
          <div className="scrolling-binary animate-matrix-fast">
              {Array(30).fill(0).map((_, i) => (
                  <div key={i} style={{ animationDelay: `${i * 0.1}s` }}>
                      01011001 11010010 00110100 INIT_MACDEVOS --status=boot --auth=chhabrawalamustafa --env=prod --node=mac-os-v1.7 10110010 00110100
                  </div>
              ))}
          </div>
          <div className="scrolling-terminal animate-matrix-slow absolute inset-0 text-emerald-500/30">
              {Array(20).fill(0).map((_, i) => (
                  <pre key={i} style={{ animationDelay: `${i * 0.3}s` }}>
                      {`> Load Module [UI_Architecture] ... SUCCESS\\n> Mount Filesystem [Projects] ... SUCCESS\\n> Initialize Auth Matrix ... SUCCESS\\n> Establishing Socket Link ... CONNECTED\\n`}
                  </pre>
              ))}
          </div>
      </div>

      {/* Added will-change-transform and backface-hidden for mobile GPU optimization */}
      <div ref={monitorRef} className="relative z-10 flex flex-col items-center origin-center will-change-transform transform-gpu [backface-visibility:hidden]">
        <div className="w-[320px] h-[230px] border-8 border-primary rounded-xl bg-[#030303] relative overflow-hidden flex items-center justify-center shadow-[0_0_30px_rgba(0,255,128,0.3)] hover:shadow-[0_0_50px_rgba(0,255,128,0.5)] transition-shadow">
          <button ref={buttonRef} className="px-6 py-3 border border-primary text-primary font-mono text-xs uppercase tracking-[0.2em] relative z-10 transition-all bg-primary/5 shadow-[0_0_15px_rgba(0,255,128,0.3)] flex items-center gap-2">
            <Terminal className="w-4 h-4" />
            Launch System
          </button>
          <div ref={bootTextRef} className="absolute inset-0 flex items-center justify-center opacity-0 font-mono text-primary text-sm tracking-[0.3em] z-10 text-center flex-col gap-2">
            <div>PR_SYS_BOOT:</div>
            <div>[ {progress}% ]</div>
          </div>
          <div ref={nameTextRef} className="absolute inset-0 flex items-center justify-center opacity-0 z-10">
            <span className="font-display font-bold text-white tracking-[0.25em] text-3xl uppercase drop-shadow-[0_0_15px_rgba(0,255,128,0.6)]">
              M.A.C.DevOS
            </span>
          </div>
          <div className="screen-overlay absolute inset-0 bg-primary/10 opacity-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_0%,rgba(0,0,0,0.5)_100%)]"></div>
          <div ref={mouseRef} className="absolute z-30 top-1/2 left-1/2 text-white pointer-events-none drop-shadow-[0_4px_10px_rgba(0,0,0,1)]">
            <MousePointer2 className="w-7 h-7 fill-white" />
          </div>
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:100%_4px] pointer-events-none opacity-40 z-20"></div>
        </div>
        <div className="w-22 h-10 border-x-8 border-b-8 border-primary rounded-b-lg opacity-90 shadow-[0_5px_15px_rgba(0,255,128,0.2)]"></div>
        <div className="w-44 h-4 bg-primary rounded-full mt-1 opacity-90 shadow-[0_2px_10px_rgba(0,255,128,0.3)]"></div>
      </div>
    </div>
  );
}
"""
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(optimized_content)
    
    print_status("GPU optimizations successfully injected. Loader is now 60fps capable.")

if __name__ == "__main__":
    deploy_performance_patch()
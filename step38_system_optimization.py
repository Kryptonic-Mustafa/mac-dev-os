import os
import time
import re
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⚙️ M.A.C.DevOS Optimization] {message}...")
    time.sleep(0.5)

def deploy_optimizations():
    # 1. GLOBAL CSS OPTIMIZATION (Hardware Acceleration & Mobile Overflow Lock)
    print_status("Injecting Hardware Acceleration into Global CSS")
    css_path = PROJECT_PATH / "src/app/globals.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
        if "/* OS OPTIMIZATIONS */" not in css_content:
            optimizations = """
/* OS OPTIMIZATIONS */
html, body {
  overflow-x: hidden; /* Prevents mobile horizontal scrolling bugs */
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overscroll-behavior-y: none; /* Prevents pull-to-refresh glitch on mobile */
}

/* Force GPU rendering for smooth GSAP animations */
.gpu-accelerate {
  transform: translateZ(0);
  will-change: transform, opacity;
  backface-visibility: hidden;
  perspective: 1000px;
}
"""
            with open(css_path, "a", encoding="utf-8") as f:
                f.write(optimizations)

    # 2. CREATE THE GSAP GPU-ACCELERATED PARALLAX BACKGROUND
    print_status("Engineering Zero-Lag Parallax Matrix Background")
    ui_dir = PROJECT_PATH / "src/components/ui"
    os.makedirs(ui_dir, exist_ok=True)
    
    bg_path = ui_dir / "InteractiveBackground.tsx"
    bg_content = r""""use client";

import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export default function InteractiveBackground() {
  const bgRef1 = useRef<HTMLDivElement>(null);
  const bgRef2 = useRef<HTMLDivElement>(null);
  const bgRef3 = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Force GSAP to use GPU 3D acceleration for everything
    gsap.config({ force3D: true });

    // GSAP quickTo is significantly faster than React state for mouse tracking
    const xTo1 = gsap.quickTo(bgRef1.current, "x", { duration: 0.8, ease: "power3.out" });
    const yTo1 = gsap.quickTo(bgRef1.current, "y", { duration: 0.8, ease: "power3.out" });
    
    const xTo2 = gsap.quickTo(bgRef2.current, "x", { duration: 1.2, ease: "power3.out" });
    const yTo2 = gsap.quickTo(bgRef2.current, "y", { duration: 1.2, ease: "power3.out" });

    const xTo3 = gsap.quickTo(bgRef3.current, "x", { duration: 1.6, ease: "power3.out" });
    const yTo3 = gsap.quickTo(bgRef3.current, "y", { duration: 1.6, ease: "power3.out" });

    const handleMouseMove = (e: MouseEvent) => {
      // Normalize coordinates (-1 to 1)
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;

      // Apply distinct depth tracking (Parallax)
      xTo1(x * -15); yTo1(y * -15); // Foreground (Fastest)
      xTo2(x * -30); yTo2(y * -30); // Midground
      xTo3(x * -50); yTo3(y * -50); // Background (Slowest)
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div className="fixed inset-0 z-[-1] pointer-events-none overflow-hidden bg-[#020202]">
      
      {/* LAYER 3: Deep Background (Darker Glow) */}
      <div 
        ref={bgRef3} 
        className="absolute inset-[-10%] w-[120%] h-[120%] gpu-accelerate opacity-30"
        style={{ background: 'radial-gradient(circle at center, rgba(0, 255, 128, 0.04) 0%, transparent 60%)' }}
      />

      {/* LAYER 2: The Matrix Grid (Darker, Subtle Dots) */}
      <div 
        ref={bgRef2} 
        className="absolute inset-[-10%] w-[120%] h-[120%] gpu-accelerate opacity-20"
        style={{ 
          backgroundImage: 'radial-gradient(rgba(0, 255, 128, 0.15) 1px, transparent 1px)',
          backgroundSize: '40px 40px' 
        }}
      />

      {/* LAYER 1: Floating Sparks (Darker Neon Accents) */}
      <div ref={bgRef1} className="absolute inset-[-10%] w-[120%] h-[120%] gpu-accelerate opacity-40">
        <div className="absolute top-[20%] left-[30%] w-1.5 h-1.5 rounded-full bg-primary/20 shadow-[0_0_15px_rgba(0,255,128,0.4)]" />
        <div className="absolute top-[70%] left-[60%] w-2 h-2 rounded-full bg-primary/10 shadow-[0_0_20px_rgba(0,255,128,0.3)]" />
        <div className="absolute top-[40%] left-[80%] w-1 h-1 rounded-full bg-primary/30 shadow-[0_0_10px_rgba(0,255,128,0.5)]" />
        <div className="absolute top-[80%] left-[20%] w-2.5 h-2.5 rounded-full bg-primary/5 shadow-[0_0_25px_rgba(0,255,128,0.2)]" />
      </div>

    </div>
  );
}
"""
    with open(bg_path, "w", encoding="utf-8") as f:
        f.write(bg_content)

    # 3. INJECT BACKGROUND INTO MAIN PAGE
    print_status("Linking Parallax Engine to Main OS Interface")
    page_path = PROJECT_PATH / "src/app/page.tsx"
    
    if page_path.exists():
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "InteractiveBackground" not in content:
            # Add import
            import_statement = "import InteractiveBackground from '@/components/ui/InteractiveBackground';\n"
            content = import_statement + content
            
            # Inject component just inside the main return wrapper
            # Find the first return statement returning a <main> or <div> wrapper
            content = re.sub(
                r'(return\s*\(\s*<[a-zA-Z0-9_]+[^>]*>)', 
                r'\1\n      <InteractiveBackground />', 
                content, 
                count=1
            )
            
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  ✓ Parallax Engine injected into page.tsx")
        else:
            print("  ✓ Parallax Engine already exists in page.tsx")

    print_status("System Optimization Protocol Complete.")

if __name__ == "__main__":
    deploy_optimizations()
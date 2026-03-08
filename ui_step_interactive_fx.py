import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[✨ M.A.C.DevOS UI Engine] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_interactive_fx():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    print_status("Injecting Canvas Interactive Background and GSAP Precision Cursor")

    # 1. Background FX Component (Canvas based for max performance)
    bg_fx_content = """"use client";

import { useEffect, useRef } from 'react';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function BackgroundFX() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { isMounted } = useVisualSettings();

  useEffect(() => {
    if (!isMounted || !canvasRef.current) return;
    
    // Only run heavy FX on non-touch devices
    const isTouch = window.matchMedia("(pointer: coarse)").matches;
    if (isTouch) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let particles: Particle[] = [];
    const mouse = { x: -1000, y: -1000, active: false };

    // Get primary color from computed CSS variables
    const getPrimaryColor = () => {
      const root = document.documentElement;
      const color = getComputedStyle(root).getPropertyValue('--color-primary').trim();
      return color || '#00F0FF';
    };

    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;

      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 1.5;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      }

      draw() {
        if (!ctx) return;
        ctx.fillStyle = getPrimaryColor();
        ctx.globalAlpha = 0.2;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    const init = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      particles = [];
      const particleCount = Math.floor((canvas.width * canvas.height) / 15000); // Responsive amount
      for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const color = getPrimaryColor();

      // Keyboard activity visual burst effect
      ctx.fillStyle = color;

      particles.forEach((p, index) => {
        p.update();
        p.draw();

        // Connect particles near mouse (Hacker Nexus Effect)
        if (mouse.active) {
          const dx = mouse.x - p.x;
          const dy = mouse.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 150) {
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.globalAlpha = 1 - dist / 150;
            ctx.lineWidth = 0.5;
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
          }
        }
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    // Event Listeners
    const handleMouseMove = (e: MouseEvent) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      mouse.active = true;
    };
    
    const handleMouseLeave = () => { mouse.active = false; };
    const handleResize = () => { init(); };

    // Keyboard trigger (draws a scanning line)
    const handleKeyDown = () => {
       ctx.fillStyle = getPrimaryColor();
       ctx.globalAlpha = 0.05;
       ctx.fillRect(0, Math.random() * canvas.height, canvas.width, 2);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('resize', handleResize);
    window.addEventListener('keydown', handleKeyDown);

    init();
    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isMounted]);

  return (
    <canvas 
      ref={canvasRef} 
      className="fixed inset-0 pointer-events-none z-0 opacity-40 transition-opacity duration-1000"
    />
  );
}
"""
    write_file("src/components/ui/BackgroundFX.tsx", bg_fx_content)

    # 2. Custom GSAP Cursor Component
    cursor_content = """"use client";

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function CustomCursor() {
  const cursorDot = useRef<HTMLDivElement>(null);
  const cursorRing = useRef<HTMLDivElement>(null);
  const { isMounted } = useVisualSettings();

  useEffect(() => {
    if (!isMounted) return;
    
    // Disable on touch devices
    if (window.matchMedia("(pointer: coarse)").matches) return;

    // We add a class to body to hide the default cursor
    document.body.classList.add('cursor-none');

    const dot = cursorDot.current;
    const ring = cursorRing.current;
    if (!dot || !ring) return;

    // GSAP quickTo is optimized for mouse tracking (60fps)
    const xMoveDot = gsap.quickTo(dot, "x", { duration: 0, ease: "none" });
    const yMoveDot = gsap.quickTo(dot, "y", { duration: 0, ease: "none" });
    
    const xMoveRing = gsap.quickTo(ring, "x", { duration: 0.15, ease: "power3.out" });
    const yMoveRing = gsap.quickTo(ring, "y", { duration: 0.15, ease: "power3.out" });

    const handleMouseMove = (e: MouseEvent) => {
      xMoveDot(e.clientX);
      yMoveDot(e.clientY);
      xMoveRing(e.clientX);
      yMoveRing(e.clientY);
    };

    const handleMouseDown = () => {
      gsap.to(ring, { scale: 0.5, duration: 0.2, ease: "power2.out" });
      gsap.to(dot, { scale: 2, duration: 0.2, ease: "power2.out" });
    };

    const handleMouseUp = () => {
      gsap.to(ring, { scale: 1, duration: 0.2, ease: "power2.out" });
      gsap.to(dot, { scale: 1, duration: 0.2, ease: "power2.out" });
    };

    // Hover effects for clickable elements
    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('a, button, [role="button"]')) {
        gsap.to(ring, { scale: 1.5, opacity: 0.5, backgroundColor: "var(--color-primary)", duration: 0.3 });
        gsap.to(dot, { opacity: 0, duration: 0.3 });
      }
    };

    const handleMouseOut = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('a, button, [role="button"]')) {
        gsap.to(ring, { scale: 1, opacity: 1, backgroundColor: "transparent", duration: 0.3 });
        gsap.to(dot, { opacity: 1, duration: 0.3 });
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mousedown", handleMouseDown);
    window.addEventListener("mouseup", handleMouseUp);
    document.addEventListener("mouseover", handleMouseOver);
    document.addEventListener("mouseout", handleMouseOut);

    return () => {
      document.body.classList.remove('cursor-none');
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("mouseover", handleMouseOver);
      document.removeEventListener("mouseout", handleMouseOut);
    };
  }, [isMounted]);

  if (typeof window !== 'undefined' && window.matchMedia("(pointer: coarse)").matches) {
    return null;
  }

  return (
    <>
      <div 
        ref={cursorDot} 
        className="fixed top-0 left-0 w-1.5 h-1.5 bg-primary rounded-full pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2 mix-blend-screen shadow-[0_0_10px_var(--color-primary)]"
      />
      <div 
        ref={cursorRing} 
        className="fixed top-0 left-0 w-8 h-8 border border-primary/50 rounded-full pointer-events-none z-[9998] -translate-x-1/2 -translate-y-1/2 transition-colors duration-300"
      />
    </>
  );
}
"""
    write_file("src/components/ui/CustomCursor.tsx", cursor_content)

    # 3. Update Layout to include both FX
    layout_content = """import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import BootSequence from "@/components/layout/BootSequence";
import Navbar from "@/components/layout/Navbar";
import BackgroundFX from "@/components/ui/BackgroundFX";
import CustomCursor from "@/components/ui/CustomCursor";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space-grotesk" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains-mono" });

export const metadata: Metadata = {
  title: "M.A.C.DevOS | Premium Digital Engineering",
  description: "Advanced full-stack engineering and UI systems architecture.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased bg-background text-foreground selection:bg-primary selection:text-background relative">
        <BackgroundFX />
        <CustomCursor />
        <BootSequence>
          <Navbar />
          {children}
        </BootSequence>
      </body>
    </html>
  );
}
"""
    write_file("src/app/layout.tsx", layout_content)

    # 4. Add the cursor-none class to globals.css safely via python replace
    css_path = PROJECT_PATH / "src/app/globals.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css_data = f.read()
    
    if ".cursor-none *" not in css_data:
        css_data += "\n/* Custom Cursor Override */\n.cursor-none, .cursor-none * {\n  cursor: none !important;\n}\n"
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_data)

    print_status("Interactive systems deployed successfully. Mouse tracking and Canvas Grid active.")

if __name__ == "__main__":
    deploy_interactive_fx()
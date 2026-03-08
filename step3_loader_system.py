import os
import time
from pathlib import Path

# --- Configuration ---
PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚀 M.A.C.DevOS Boot Sequence] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_loader_system():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found. Ensure you are inside the 'mac-dev-os' directory.")
        return

    print_status("Engineering GSAP Signature Loader System")

    # 1. GSAP Loader Component
    loader_content = """"use client";

import { useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function Loader({ onComplete }: { onComplete: () => void }) {
  const { loaderStyle, isMounted } = useVisualSettings();
  const containerRef = useRef<HTMLDivElement>(null);
  const elementRef = useRef<HTMLDivElement>(null);
  const coreRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!isMounted || !elementRef.current || !containerRef.current || !coreRef.current) return;

    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to(containerRef.current, {
          opacity: 0,
          duration: 0.8,
          ease: "power2.inOut",
          onComplete
        });
      }
    });

    // Premium Intro Sequence (Universal)
    tl.fromTo(elementRef.current, 
      { scale: 0, opacity: 0 }, 
      { scale: 1, opacity: 1, duration: 1, ease: "expo.out" }
    );

    // Style-specific sequences
    if (loaderStyle === 'morphing-geometry') {
      tl.to(elementRef.current, { borderRadius: "50%", rotation: 90, duration: 0.8, ease: "power2.inOut" })
        .to(elementRef.current, { borderRadius: "0%", rotation: 180, scale: 0.5, duration: 0.8, ease: "power2.inOut" })
        .to(coreRef.current, { scale: 5, opacity: 0, duration: 0.6, ease: "power2.in" });

    } else if (loaderStyle === 'pulse') {
      tl.to(elementRef.current, { scale: 1.2, boxShadow: "0 0 60px var(--color-glow)", duration: 0.6, yoyo: true, repeat: 2, ease: "sine.inOut" })
        .to(coreRef.current, { scale: 10, opacity: 0, duration: 0.5, ease: "power3.in" });

    } else { // scan
      tl.to(coreRef.current, { height: "100%", top: "0%", duration: 1, ease: "power1.inOut" })
        .to(coreRef.current, { height: "2px", top: "100%", duration: 0.8, ease: "power1.inOut" })
        .to(elementRef.current, { scaleX: 4, opacity: 0, duration: 0.5, ease: "power2.in" });
    }

    // Exit scale
    tl.to(elementRef.current, { scale: 0, opacity: 0, duration: 0.5, ease: "back.in(1.7)" }, "-=0.3");

  }, [isMounted, loaderStyle]);

  // Prevent hydration mismatch render
  if (!isMounted) return <div className="fixed inset-0 bg-background z-50"></div>;

  return (
    <div ref={containerRef} className="fixed inset-0 bg-background z-50 flex items-center justify-center overflow-hidden">
      <div 
        ref={elementRef} 
        className="relative w-16 h-16 border border-primary flex items-center justify-center overflow-hidden shadow-neon"
      >
        <div 
          ref={coreRef} 
          className="absolute w-full h-[2px] bg-secondary top-1/2 -translate-y-1/2 shadow-[0_0_15px_var(--color-primary)]"
        />
      </div>
    </div>
  );
}
"""
    write_file("src/components/ui/Loader.tsx", loader_content)

    # 2. Boot Sequence Wrapper
    boot_sequence_content = """"use client";

import { useState } from 'react';
import Loader from '@/components/ui/Loader';

export default function BootSequence({ children }: { children: React.ReactNode }) {
  const [isBooted, setIsBooted] = useState(false);

  return (
    <>
      {!isBooted && <Loader onComplete={() => setIsBooted(true)} />}
      <div 
        className={`transition-opacity duration-1000 ease-out min-h-screen ${
          isBooted ? 'opacity-100' : 'opacity-0 h-screen overflow-hidden'
        }`}
      >
        {children}
      </div>
    </>
  );
}
"""
    write_file("src/components/layout/BootSequence.tsx", boot_sequence_content)

    # 3. Root Layout (Injecting Fonts and BootSequence)
    layout_content = """import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import BootSequence from "@/components/layout/BootSequence";
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
      <body className="font-sans antialiased bg-background text-foreground selection:bg-primary selection:text-background">
        <BootSequence>
          {children}
        </BootSequence>
      </body>
    </html>
  );
}
"""
    write_file("src/app/layout.tsx", layout_content)

    # 4. Cleanup default page.tsx so we have a blank canvas for the Hero
    page_content = """export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center">
      {/* The Hero component will be injected here in Step 4 */}
      <div className="font-mono text-primary/50 text-sm tracking-widest uppercase">
        System Ready. Awaiting Hero Module.
      </div>
    </main>
  );
}
"""
    write_file("src/app/page.tsx", page_content)

    print_status("Boot Loader sequence integrated. System is primed for the Hero Module.")

if __name__ == "__main__":
    deploy_loader_system()
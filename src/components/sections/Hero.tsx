"use client";

import { useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

const PHRASES = [
  "Booting M.A.C.DevOS...",
  "Engineering Digital Systems.",
  "Building Interfaces.",
  "Deploying Intelligence."
];

export default function Hero() {
  const containerRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLDivElement>(null);
  const cursorRef = useRef<HTMLSpanElement>(null);
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);

  // 1. Blinking Cursor Animation
  useGSAP(() => {
    gsap.to(cursorRef.current, {
      opacity: 0,
      ease: "steps(1)",
      repeat: -1,
      duration: 0.5
    });
  });

  // 2. GSAP Native Typing Engine (No external plugins required)
  useGSAP(() => {
    const target = textRef.current;
    if (!target) return;

    const phrase = PHRASES[currentPhraseIndex];
    const proxy = { length: 0 };
    
    const tl = gsap.timeline({
      onComplete: () => {
        // Pause, then execute backspace sequence
        gsap.to(proxy, {
          length: 0,
          duration: phrase.length * 0.03, // Faster delete speed
          ease: "none",
          delay: 2.5, // Readability pause
          onUpdate: () => {
            target.innerText = phrase.substring(0, Math.floor(proxy.length));
          },
          onComplete: () => {
            setCurrentPhraseIndex((prev) => (prev + 1) % PHRASES.length);
          }
        });
      }
    });

    // Typing sequence
    tl.to(proxy, {
      length: phrase.length,
      duration: phrase.length * 0.08, // Human-like typing rhythm
      ease: "none",
      onUpdate: () => {
        target.innerText = phrase.substring(0, Math.floor(proxy.length));
      }
    });
  }, [currentPhraseIndex]);

  // 3. UI Entrance Stagger
  useGSAP(() => {
    gsap.from(".hero-element", {
      y: 40,
      opacity: 0,
      duration: 1.2,
      stagger: 0.15,
      ease: "power3.out",
      delay: 0.2 // Wait for loader to clear
    });
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Engineered Background Depth */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] bg-primary/5 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_10%,transparent_100%)] pointer-events-none" />

      <div className="relative z-10 w-full max-w-6xl mx-auto px-6 lg:px-12 flex flex-col items-start">
        
        {/* Status Indicator */}
        <div className="hero-element flex items-center gap-3 mb-8">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-primary shadow-neon"></span>
          </span>
          <span className="font-mono text-xs tracking-[0.2em] text-primary/80 uppercase">System Online // Core Active</span>
        </div>

        {/* Main Terminal Heading */}
        <h1 className="hero-element text-5xl md:text-7xl lg:text-8xl font-display font-medium tracking-tight mb-8 text-foreground">
          <span className="block text-foreground/40 mb-2 text-2xl md:text-4xl">Executing:</span>
          <div className="flex items-center min-h-[1.2em]">
            <span ref={textRef} className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary"></span>
            <span ref={cursorRef} className="inline-block w-[0.08em] h-[0.9em] bg-primary ml-2 shadow-[0_0_15px_var(--color-primary)]"></span>
          </div>
        </h1>

        {/* Brand Statement */}
        <p className="hero-element text-lg md:text-xl text-foreground/60 max-w-2xl font-sans font-light leading-relaxed mb-12">
          Architecting premium digital systems. We engineer scalable, high-performance web infrastructure with corporate credibility and futuristic precision.
        </p>

        {/* CTA Actions */}
        <div className="hero-element flex flex-wrap gap-5">
          <button className="group relative px-8 py-4 bg-primary/10 border border-primary text-primary font-mono text-sm tracking-widest uppercase overflow-hidden transition-all duration-300 hover:shadow-[0_0_30px_var(--color-glow)]">
            <div className="absolute inset-0 w-0 bg-primary transition-all duration-300 ease-out group-hover:w-full z-0"></div>
            <span className="relative z-10 group-hover:text-background font-semibold transition-colors duration-300">Deploy Protocol</span>
          </button>
          
          <button className="px-8 py-4 border border-foreground/20 text-foreground font-mono text-sm tracking-widest uppercase hover:border-foreground/60 hover:bg-foreground/5 transition-all duration-300">
            View Architecture
          </button>
        </div>

      </div>
    </section>
  );
}

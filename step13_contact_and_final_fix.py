import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚀 M.A.C.DevOS Final Protocol] {message}...")
    time.sleep(0.5)

def deploy_final_systems():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    # ---------------------------------------------------------
    # 1. THE SILVER BULLET ADVANTAGES FIX
    # ---------------------------------------------------------
    print_status("Deploying Silver Bullet GSAP Pin Fix for Horizontal Matrix")
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    adv_content = """"use client";

import { useRef, useEffect } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, ShieldCheck, Activity, Layers, Cpu } from 'lucide-react';

const ADVANTAGES = [
  { id: "ADV-01", title: "Sub-Second LCP", description: "Our architecture prioritizes immediate paint times. By leveraging Edge networks and aggressive caching, the system loads before the user even realizes.", icon: Zap },
  { id: "ADV-02", title: "Cinematic Motion", description: "Unlike standard templates, we utilize hardware-accelerated WebGL and GSAP pipelines to deliver fluid, 60fps animations without draining device batteries.", icon: Activity },
  { id: "ADV-03", title: "Military-Grade Security", description: "Strict CORS policies, encrypted payload handling, and deterministic state management ensure zero data leaks across the deployment matrix.", icon: ShieldCheck },
  { id: "ADV-04", title: "Modular Scalability", description: "Built on strictly typed Next.js App Routers and Prisma ORM, allowing the system to scale from 10 to 10,000,000 concurrent connections seamlessly.", icon: Layers },
  { id: "ADV-05", title: "Serverless Compute", description: "We bypass legacy monolithic servers. Database transactions via TiDB and Vercel Serverless Functions guarantee infinite elasticity.", icon: Cpu }
];

export default function Advantages() {
  const containerRef = useRef<HTMLElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (typeof window !== "undefined") {
      gsap.registerPlugin(ScrollTrigger);
    }
    
    // Force a total recalculation after hydration to prevent 0-height pin bugs
    setTimeout(() => {
      ScrollTrigger.refresh();
    }, 500);

    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (isMobile || !containerRef.current || !trackRef.current) return;

    const track = trackRef.current;

    // Wait until next tick to calculate width
    gsap.delayedCall(0.1, () => {
      const totalWidth = track.scrollWidth;
      const viewportWidth = window.innerWidth;
      const scrollDistance = totalWidth - viewportWidth + 200; // Add padding buffer

      gsap.to(track, {
        x: -scrollDistance,
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: () => `+=${scrollDistance}`,
          pin: true,
          pinSpacing: true, // Strictly force the spacer block
          scrub: 1,
          invalidateOnRefresh: true,
        }
      });
    });

  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="relative w-full h-screen flex flex-col justify-center bg-transparent border-t border-foreground/5 z-20 overflow-hidden">
      
      {/* Absolute Header - Protected from flex layout overlap */}
      <div className="absolute top-[12%] md:top-[15%] left-0 w-full px-6 lg:px-12 z-10 pointer-events-none">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-4">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">System Advantages</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
            Why Choose M.A.C.DevOs
          </h2>
        </div>
      </div>

      {/* The Scroll Track */}
      <div ref={trackRef} className="flex flex-nowrap items-center gap-6 md:gap-12 w-max px-6 lg:px-[10vw] mt-24">
        {ADVANTAGES.map((adv, index) => (
          <div key={adv.id} className="w-[85vw] md:w-[400px] shrink-0">
            <div className="group relative p-8 md:p-10 bg-background/60 backdrop-blur-md border border-foreground/10 hover:border-primary/50 transition-all duration-300 w-full h-[400px] flex flex-col justify-between overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
              
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className="p-3 rounded-full bg-primary/5 group-hover:bg-primary/10 transition-colors border border-primary/20">
                    <adv.icon className="w-6 h-6 md:w-8 md:h-8 text-primary group-hover:scale-110 transition-transform duration-500" />
                  </div>
                  <span className="font-mono text-3xl md:text-4xl font-black text-foreground/5 group-hover:text-primary/10 transition-colors duration-500">
                    0{index + 1}
                  </span>
                </div>
                <h3 className="text-xl md:text-2xl font-display text-foreground mb-3 group-hover:text-primary transition-colors duration-300">
                  {adv.title}
                </h3>
                <p className="font-sans text-foreground/60 leading-relaxed text-sm">
                  {adv.description}
                </p>
              </div>

              <div className="pt-4 border-t border-foreground/5 flex justify-between items-center mt-4">
                <span className="font-mono text-xs tracking-widest text-primary/50 uppercase">{adv.id}</span>
                <span className="w-2 h-2 rounded-full bg-primary/50 group-hover:bg-primary group-hover:shadow-[0_0_10px_var(--color-primary)] transition-all duration-500"></span>
              </div>
            </div>
          </div>
        ))}
        {/* End Buffer to prevent snapping off-screen */}
        <div className="w-[20vw] shrink-0 hidden md:block"></div>
      </div>
    </section>
  );
}
"""
    with open(adv_path, "w", encoding="utf-8") as f:
        f.write(adv_content)


    # ---------------------------------------------------------
    # 2. CONTACT US FORM (Secure Comm Channel)
    # ---------------------------------------------------------
    print_status("Engineering Secure Comm Channel (Contact Form)")
    contact_path = PROJECT_PATH / "src/components/sections/Contact.tsx"
    
    contact_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { TerminalSquare, Send, ServerCrash } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function Contact() {
  const sectionRef = useRef<HTMLElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  useGSAP(() => {
    gsap.from(".contact-element", {
      y: 40,
      opacity: 0,
      duration: 1,
      stagger: 0.15,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });
  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20 overflow-hidden">
      
      {/* Background Tech Details */}
      <div className="absolute inset-0 pointer-events-none opacity-5">
        <div className="absolute top-[20%] right-[10%] font-mono text-9xl tracking-tighter">SYS.</div>
        <div className="absolute bottom-[10%] left-[5%] font-mono text-[15rem] leading-none tracking-tighter opacity-50">0X</div>
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        
        {/* Section Header */}
        <div className="contact-element mb-16 text-center flex flex-col items-center">
          <div className="flex items-center gap-3 mb-6">
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
            <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Secure Link</span>
            <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
          </div>
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-display font-medium text-foreground tracking-tight mb-6">
            Initialize Connection
          </h2>
          <p className="text-foreground/50 max-w-xl font-sans text-sm md:text-base leading-relaxed">
            Ready to deploy your next high-performance digital asset? Transmit your project parameters below to open a secure comm channel.
          </p>
        </div>

        {/* Terminal Form Window */}
        <form ref={formRef} className="contact-element w-full bg-background/80 backdrop-blur-xl border border-foreground/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] overflow-hidden">
          
          {/* Terminal Header */}
          <div className="w-full bg-foreground/[0.03] border-b border-foreground/10 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></span>
              <span className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></span>
              <span className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></span>
            </div>
            <div className="flex items-center gap-2 text-foreground/40 font-mono text-[10px] uppercase tracking-widest">
              <TerminalSquare className="w-3 h-3" />
              macdevos_transmit.exe
            </div>
            <div className="w-16"></div> {/* Spacer for centering */}
          </div>

          {/* Form Body */}
          <div className="p-6 md:p-10 flex flex-col gap-8">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex flex-col gap-3">
                <label className="font-mono text-xs text-primary tracking-widest uppercase">ID // Identity</label>
                <input 
                  type="text" 
                  placeholder="Enter your name..."
                  className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors"
                />
              </div>
              <div className="flex flex-col gap-3">
                <label className="font-mono text-xs text-primary tracking-widest uppercase">COMM // Email</label>
                <input 
                  type="email" 
                  placeholder="Enter secure comm link..."
                  className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors"
                />
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <label className="font-mono text-xs text-primary tracking-widest uppercase">PAYLOAD // Project Data</label>
              <textarea 
                rows={5}
                placeholder="Detail your system requirements and architecture needs..."
                className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors resize-none"
              ></textarea>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-foreground/10">
              <div className="flex items-center gap-2 text-foreground/30 font-mono text-[10px] tracking-widest uppercase">
                <ServerCrash className="w-3 h-3" /> End-to-end encrypted
              </div>
              
              <button 
                type="button" 
                className="group relative px-8 py-4 bg-primary/10 border border-primary text-primary font-mono text-sm tracking-widest uppercase overflow-hidden transition-all duration-300 hover:shadow-[0_0_20px_var(--color-glow)]"
              >
                <div className="absolute inset-0 w-0 bg-primary transition-all duration-300 ease-out group-hover:w-full z-0"></div>
                <span className="relative z-10 group-hover:text-background font-semibold transition-colors duration-300 flex items-center gap-2">
                  Transmit Data <Send className="w-4 h-4" />
                </span>
              </button>
            </div>

          </div>
        </form>

      </div>
    </section>
  );
}
"""
    with open(contact_path, "w", encoding="utf-8") as f:
        f.write(contact_content)


    # ---------------------------------------------------------
    # 3. UPDATE PAGE ARCHITECTURE
    # ---------------------------------------------------------
    print_status("Integrating final modules into the Main Frame")
    page_path = PROJECT_PATH / "src/app/page.tsx"
    
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import Advantages from "@/components/sections/Advantages";
import TechStack from "@/components/sections/TechStack";
import DeploymentMatrix from "@/components/sections/Projects";
import SystemReviews from "@/components/sections/Reviews";
import Contact from "@/components/sections/Contact";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <Advantages />
      <TechStack />
      <DeploymentMatrix />
      <SystemReviews />
      <Contact />
    </main>
  );
}
"""
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(page_content)

    print_status("M.A.C.DevOS Front-End Systems are 100% Locked and Deployed.")

if __name__ == "__main__":
    deploy_final_systems()
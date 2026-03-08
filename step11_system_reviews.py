import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[💬 M.A.C.DevOs Telemetry Logs] {message}...")
    time.sleep(0.5)

def write_file(filepath, content):
    full_path = PROJECT_PATH / filepath
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Engineered: {filepath}")

def deploy_reviews():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    print_status("Engineering GSAP Testimonials (System Reviews) Section")

    # 1. Reviews Component
    reviews_content = """"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { MessageSquareTerminal, CheckCircle2 } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const REVIEWS = [
  {
    id: "LOG-992",
    client: "Sarah Jenkins",
    role: "CTO, FinTech Global",
    status: "VERIFIED",
    content: "The Bank Management System engineered by M.A.C.DevOs completely overhauled our transaction latency. Sub-second processing and flawless UI execution. Highly recommended."
  },
  {
    id: "LOG-405",
    client: "Marcus Chen",
    role: "Director of Ops, RetailCorp",
    status: "VERIFIED",
    content: "Our enterprise bug tracker was a mess before this deployment. The deterministic state management and clean architecture they provided scaled effortlessly to our 500+ team."
  },
  {
    id: "LOG-711",
    client: "Elena Rodriguez",
    role: "Founder, DataSync AI",
    status: "VERIFIED",
    content: "Unmatched cinematic motion and front-end precision. They didn't just build a website; they built a premium digital product that immediately elevated our brand authority."
  }
];

export default function SystemReviews() {
  const sectionRef = useRef<HTMLElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Header Reveal
    gsap.from(headerRef.current, {
      y: 40,
      opacity: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });

    // Staggered Cards Reveal
    if (gridRef.current) {
      const cards = gridRef.current.children;
      gsap.from(cards, {
        y: 60,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "back.out(1.2)",
        scrollTrigger: {
          trigger: gridRef.current,
          start: "top 85%",
        }
      });
    }
  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div ref={headerRef} className="mb-20 flex flex-col md:flex-row md:items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
              <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Telemetry Logs</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
              System Reviews
            </h2>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-primary/5 border border-primary/20 rounded-sm">
            <CheckCircle2 className="w-4 h-4 text-primary" />
            <span className="font-mono text-xs text-primary uppercase tracking-widest">100% Client Success Rate</span>
          </div>
        </div>

        {/* Reviews Grid */}
        <div ref={gridRef} className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {REVIEWS.map((review) => (
            <div 
              key={review.id} 
              className="group relative p-8 bg-background/40 backdrop-blur-md border border-foreground/10 hover:border-primary/50 transition-all duration-500 overflow-hidden flex flex-col justify-between h-full"
            >
              {/* Subtle top gradient line */}
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

              <div>
                <div className="flex items-center justify-between mb-8">
                  <MessageSquareTerminal className="w-6 h-6 text-foreground/40 group-hover:text-primary transition-colors duration-300" />
                  <span className="font-mono text-[10px] text-primary/60 tracking-widest px-2 py-1 bg-primary/10 border border-primary/20 rounded-sm">
                    {review.status}
                  </span>
                </div>
                
                <p className="font-sans text-foreground/70 leading-relaxed text-sm md:text-base italic mb-8">
                  "{review.content}"
                </p>
              </div>

              <div className="pt-6 border-t border-foreground/10 flex items-center justify-between">
                <div>
                  <h4 className="font-display text-foreground text-sm group-hover:text-primary transition-colors">{review.client}</h4>
                  <p className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase mt-1">{review.role}</p>
                </div>
                <span className="font-mono text-[10px] text-foreground/30">{review.id}</span>
              </div>
              
              {/* Background Glow */}
              <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none -z-10"></div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
"""
    write_file("src/components/sections/Reviews.tsx", reviews_content)

    # 2. Update Home Page to Include Reviews
    page_content = """import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import Advantages from "@/components/sections/Advantages";
import DeploymentMatrix from "@/components/sections/Projects";
import SystemReviews from "@/components/sections/Reviews";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <Advantages />
      <DeploymentMatrix />
      <SystemReviews />
    </main>
  );
}
"""
    write_file("src/app/page.tsx", page_content)

    print_status("System Reviews integrated successfully")

if __name__ == "__main__":
    deploy_reviews()
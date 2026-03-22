"use client";

import { useState, useEffect,  useRef, useEffect } from 'react';
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
  const [screenWidth, setScreenWidth] = useState(0);

  useEffect(() => {
    const handleResize = () => setScreenWidth(window.innerWidth);
    handleResize(); // Set on mount
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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

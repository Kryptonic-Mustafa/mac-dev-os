"use client";
import { useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Zap, Activity, Shield, Cpu, ArrowRight } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function Advantages() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sliderRef = useRef<HTMLDivElement>(null);
  const indicatorRef = useRef<HTMLDivElement>(null);
  const [progress, setProgress] = useState(0);

  const advantages = [
    { icon: Zap, title: "Sub-Second LCP", desc: "Our architecture prioritizes immediate paint times. Edge networks and aggressive caching mean the system loads before the user realizes.", id: "01" },
    { icon: Activity, title: "Cinematic Motion", desc: "Hardware-accelerated WebGL and GSAP pipelines deliver fluid, 60fps animations without draining device batteries.", id: "02" },
    { icon: Shield, title: "Military-Grade Security", desc: "Strict CORS policies, encrypted payloads, and deterministic state management ensure zero data leaks.", id: "03" },
    { icon: Cpu, title: "Edge Computing", desc: "Distributed serverless functions ensure your portfolio is executed physically closer to the user, eliminating latency.", id: "04" }
  ];

  useGSAP(() => {
    let mm = gsap.matchMedia();

    // DESKTOP ONLY: Cinematic ScrollTrigger
    mm.add("(min-width: 768px)", () => {
      let sections = gsap.utils.toArray(".adv-card");
      const totalWidth = sliderRef.current?.offsetWidth || 0;
      
      gsap.to(sections, {
        xPercent: -100 * (sections.length - 1),
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          pin: true,
          scrub: 1,
          snap: 1 / (sections.length - 1),
          end: () => "+=" + totalWidth,
          onUpdate: (self) => setProgress(Math.round(self.progress * 100))
        }
      });
    });

    // MOBILE ONLY: Native Event Listener (NO scroll trapping!)
    mm.add("(max-width: 767px)", () => {
      const slider = sliderRef.current;
      if (!slider) return;

      // Clear any GSAP formatting so native CSS can take over
      gsap.set(slider, { clearProps: "all" });

      const handleScroll = () => {
        const maxScroll = slider.scrollWidth - slider.clientWidth;
        const currentScroll = slider.scrollLeft;
        const prog = maxScroll > 0 ? (currentScroll / maxScroll) * 100 : 0;
        setProgress(Math.round(prog));
      };

      // Listen to native scrolling to update the glowing bar
      slider.addEventListener("scroll", handleScroll, { passive: true });
      handleScroll(); // Init progress

      return () => slider.removeEventListener("scroll", handleScroll);
    });

    return () => mm.revert();
  }, { scope: containerRef });

  return (
    <section ref={containerRef} className="py-20 bg-background text-foreground overflow-hidden">
      <div className="container mx-auto px-4 mb-6">
        <h2 className="text-sm font-mono text-primary mb-2 uppercase tracking-widest flex items-center gap-2">
          <span className="w-8 h-[1px] bg-primary"></span> System Advantages
        </h2>
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 md:gap-0">
          <h3 className="text-4xl md:text-5xl font-display">Why Choose M.A.C.DevOS</h3>
          
          <div className="md:hidden flex flex-col gap-2 mt-2 w-full max-w-[200px] border border-foreground/5 p-4 bg-background/50 backdrop-blur-sm">
            <div className="flex items-center text-xs font-mono text-primary/70 animate-pulse">
                <span>Swipe matrix</span>
                <ArrowRight className="w-4 h-4 ml-2" />
            </div>
            
            <div className="relative w-full h-1 bg-foreground/10 rounded-full overflow-hidden mt-1">
              <div 
                ref={indicatorRef} 
                className="absolute top-0 left-0 h-full bg-primary rounded-full shadow-[0_0_10px_rgba(0,255,128,0.6)]"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="text-[9px] font-mono text-foreground/30 text-center">[ {progress}% DEPLOYED ]</div>
          </div>
        </div>
      </div>

      <div className="pl-4 md:pl-0">
        {/* CRITICAL FIX: 
          w-full + overflow-x-auto enables native touch panning.
          touch-auto explicitly tells the browser to NOT trap vertical scrolling.
        */}
        <div
          ref={sliderRef}
          className="flex gap-6 md:gap-8 w-full md:w-[200vw] overflow-x-auto md:overflow-visible snap-x snap-mandatory touch-auto pr-4 md:pr-0 scroll-smooth [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden"
        >
          {advantages.map((adv, i) => (
            <div
              key={i}
              className="adv-card w-[85vw] md:w-[45vw] lg:w-[30vw] flex-shrink-0 snap-center bg-background border border-foreground/10 p-8 md:p-12 relative group hover:border-primary/50 transition-colors"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/0 via-primary to-primary/0 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="flex justify-between items-start mb-8">
                <div className="p-4 rounded-full bg-primary/10 text-primary border border-primary/20">
                  <adv.icon className="w-8 h-8" />
                </div>
                <span className="text-4xl font-display text-foreground/10 font-bold">{adv.id}</span>
              </div>
              <h4 className="text-2xl font-display mb-4">{adv.title}</h4>
              <p className="text-foreground/50 leading-relaxed">{adv.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

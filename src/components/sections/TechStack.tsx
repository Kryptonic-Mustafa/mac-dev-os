"use client";

import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Code2, ServerCog, DatabaseZap } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

const TECH_CATEGORIES = [
  {
    id: "CAT-01",
    title: "Front-End Architecture",
    icon: Code2,
    skills: [
      { name: "React.js / React Native", level: 95 },
      { name: "TypeScript / JavaScript", level: 90 },
      { name: "TailwindCSS / Bootstrap", level: 95 },
      { name: "HTML5 / CSS3 / jQuery", level: 85 }
    ]
  },
  {
    id: "CAT-02",
    title: "Back-End & Systems",
    icon: ServerCog,
    skills: [
      { name: "PHP", level: 90 },
      { name: "Laravel", level: 85 },
      { name: "Node.js", level: 75 },
    ]
  },
  {
    id: "CAT-03",
    title: "Data & Infrastructure",
    icon: DatabaseZap,
    skills: [
      { name: "MySQL", level: 90 },
      { name: "Docker", level: 80 },
      { name: "Vercel / Edge Deployments", level: 85 }
    ]
  }
];

export default function TechStack() {
  const sectionRef = useRef<HTMLElement>(null);
  const progressRefs = useRef<(HTMLDivElement | null)[]>([]);

  useGSAP(() => {
    // Animate progress bars filling up when scrolled into view
    progressRefs.current.forEach((bar) => {
      if (!bar) return;
      const targetWidth = bar.getAttribute('data-width');
      
      gsap.fromTo(bar, 
        { width: "0%" },
        {
          width: `${targetWidth}%`,
          duration: 1.5,
          ease: "power3.out",
          scrollTrigger: {
            trigger: bar,
            start: "top 90%",
          }
        }
      );
    });

    // Stagger entire categories
    gsap.from(".tech-category", {
      y: 50,
      opacity: 0,
      duration: 0.8,
      stagger: 0.2,
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top 80%",
      }
    });

  }, { scope: sectionRef });

  return (
    <section ref={sectionRef} className="relative w-full py-32 px-6 lg:px-12 border-t border-foreground/5 z-20">
      <div className="max-w-7xl mx-auto">
        
        {/* Section Header */}
        <div className="mb-20 flex flex-col md:flex-row md:items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-3 mb-4">
              <span className="h-[1px] w-8 bg-primary shadow-neon"></span>
              <span className="font-mono text-xs tracking-[0.2em] text-primary uppercase">Tech Specifications</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-display font-medium text-foreground tracking-tight">
              Operational Matrix
            </h2>
          </div>
          <p className="text-foreground/50 max-w-md font-sans text-sm leading-relaxed">
            Proficiency parameters across front-end rendering engines, server-side infrastructure, and relational database management.
          </p>
        </div>

        {/* Tech Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 md:gap-12">
          {TECH_CATEGORIES.map((category) => (
            <div key={category.id} className="tech-category flex flex-col gap-8 p-8 border border-foreground/10 bg-background/40 backdrop-blur-sm hover:border-primary/30 transition-colors duration-500">
              
              <div className="flex items-center gap-4">
                <div className="p-3 bg-primary/5 border border-primary/20 rounded-sm">
                  <category.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-xl font-display text-foreground tracking-wide">
                  {category.title}
                </h3>
              </div>

              <div className="flex flex-col gap-6">
                {category.skills.map((skill, index) => (
                  <div key={skill.name} className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="font-mono text-xs text-foreground/70 uppercase tracking-widest">{skill.name}</span>
                      <span className="font-mono text-xs text-primary/80">[{skill.level}%]</span>
                    </div>
                    {/* The Bar Track */}
                    <div className="w-full h-1.5 bg-foreground/10 overflow-hidden relative">
                      {/* The Animated Fill */}
                      <div 
                        ref={(el) => { progressRefs.current.push(el); }}
                        data-width={skill.level}
                        className="h-full bg-gradient-to-r from-primary/50 to-primary shadow-[0_0_10px_var(--color-primary)] w-0"
                      />
                    </div>
                  </div>
                ))}
              </div>

            </div>
          ))}
        </div>

      </div>
    </section>
  );
}

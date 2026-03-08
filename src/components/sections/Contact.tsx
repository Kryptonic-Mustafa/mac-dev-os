"use client";
import Swal from 'sweetalert2';

import { useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { TerminalSquare, Send, ServerCrash, Loader2, CheckCircle2 } from 'lucide-react';

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}

export default function Contact() {
  const sectionRef = useRef<HTMLElement>(null);
  const formRef = useRef<HTMLFormElement>(null);
  
  // Transmission States
  const [isTransmitting, setIsTransmitting] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');

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

  const handleTransmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsTransmitting(true);
    setStatus('idle');

    const formData = new FormData(e.currentTarget);
    const data = {
      name: formData.get('name'),
      email: formData.get('email'),
      payload: formData.get('payload'),
    };

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        setStatus('success');
        if (formRef.current) formRef.current.reset();
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    } finally {
      setIsTransmitting(false);
      
      // Reset success message after 5 seconds
      if (status !== 'error') {
        setTimeout(() => setStatus('idle'), 5000);
      }
    }
  };

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
        <form ref={formRef} onSubmit={handleTransmit} className="contact-element w-full bg-background/80 backdrop-blur-xl border border-foreground/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] overflow-hidden">
          
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
            <div className="w-16"></div>
          </div>

          {/* Form Body */}
          <div className="p-6 md:p-10 flex flex-col gap-8">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex flex-col gap-3">
                <label className="font-mono text-xs text-primary tracking-widest uppercase">ID // Identity</label>
                <input 
                  type="text" 
                  name="name"
                  required
                  disabled={isTransmitting}
                  placeholder="Enter your name..."
                  className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors disabled:opacity-50"
                />
              </div>
              <div className="flex flex-col gap-3">
                <label className="font-mono text-xs text-primary tracking-widest uppercase">COMM // Email</label>
                <input 
                  type="email" 
                  name="email"
                  required
                  disabled={isTransmitting}
                  placeholder="Enter secure comm link..."
                  className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors disabled:opacity-50"
                />
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <label className="font-mono text-xs text-primary tracking-widest uppercase">PAYLOAD // Project Data</label>
              <textarea 
                rows={5}
                name="payload"
                required
                disabled={isTransmitting}
                placeholder="Detail your system requirements and architecture needs..."
                className="w-full bg-foreground/[0.02] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm p-4 outline-none transition-colors resize-none disabled:opacity-50"
              ></textarea>
            </div>

            {/* Status Messages */}
            {status === 'success' && (
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 text-emerald-500 font-mono text-xs flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> TRANSMISSION SUCCESSFUL. STAND BY FOR RESPONSE.
              </div>
            )}
            {status === 'error' && (
              <div className="p-4 bg-red-500/10 border border-red-500/30 text-red-500 font-mono text-xs flex items-center gap-2">
                <ServerCrash className="w-4 h-4" /> TRANSMISSION FAILED. NETWORK INTERFERENCE DETECTED.
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-foreground/10">
              <div className="flex items-center gap-2 text-foreground/30 font-mono text-[10px] tracking-widest uppercase">
                <ServerCrash className="w-3 h-3" /> End-to-end encrypted
              </div>
              
              <button 
                type="submit" 
                disabled={isTransmitting}
                className="group relative px-8 py-4 bg-primary/10 border border-primary text-primary font-mono text-sm tracking-widest uppercase overflow-hidden transition-all duration-300 hover:shadow-[0_0_20px_var(--color-glow)] disabled:opacity-50 disabled:hover:shadow-none"
              >
                <div className="absolute inset-0 w-0 bg-primary transition-all duration-300 ease-out group-hover:w-full z-0"></div>
                <span className="relative z-10 group-hover:text-background font-semibold transition-colors duration-300 flex items-center gap-2">
                  {isTransmitting ? (
                    <>TRANSMITTING <Loader2 className="w-4 h-4 animate-spin" /></>
                  ) : (
                    <>Transmit Data <Send className="w-4 h-4" /></>
                  )}
                </span>
              </button>
            </div>

          </div>
        </form>

      </div>
    </section>
  );
}

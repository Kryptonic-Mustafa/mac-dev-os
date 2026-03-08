"use client";

import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { Terminal, Lock, Loader2, ShieldAlert } from 'lucide-react';

export default function AdminLogin() {
  const router = useRouter();
  const containerRef = useRef<HTMLDivElement>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useGSAP(() => {
    gsap.from(".login-el", {
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: "power3.out",
      delay: 0.2
    });
  }, { scope: containerRef });

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        // Success animation before redirect
        gsap.to(containerRef.current, {
          scale: 0.95,
          opacity: 0,
          duration: 0.5,
          ease: "power2.inOut",
          onComplete: () => router.push('/admin/dashboard')
        });
      } else {
        const data = await res.json();
        setError(data.error || 'Access Denied.');
        // Error shake animation
        gsap.fromTo(containerRef.current, 
          { x: -10 }, 
          { x: 10, duration: 0.1, yoyo: true, repeat: 5, ease: "linear", clearProps: "x" }
        );
      }
    } catch (err) {
      setError('System malfunction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background Matrix Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_10%,transparent_100%)] pointer-events-none z-0" />
      
      <div ref={containerRef} className="w-full max-w-md relative z-10">
        
        <div className="login-el flex flex-col items-center mb-10">
          <div className="p-4 border border-primary/30 rounded-full bg-primary/5 shadow-neon mb-6">
            <Lock className="w-8 h-8 text-primary" />
          </div>
          <h1 className="font-display text-3xl text-foreground tracking-widest uppercase text-center mb-2">
            Restricted Area
          </h1>
          <p className="font-mono text-xs text-primary/60 tracking-widest uppercase">
            M.A.C.DevOS Command Center
          </p>
        </div>

        <form onSubmit={handleLogin} className="login-el bg-background/80 backdrop-blur-xl border border-foreground/10 p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
          
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Admin Identity</label>
              <div className="relative">
                <Terminal className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-primary/50" />
                <input 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@macdevos.com"
                  className="w-full bg-foreground/[0.03] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm py-3 pl-12 pr-4 outline-none transition-colors"
                  required
                />
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Passphrase</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-primary/50" />
                <input 
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-foreground/[0.03] border border-foreground/10 focus:border-primary/50 text-foreground font-sans text-sm py-3 pl-12 pr-4 outline-none transition-colors"
                  required
                />
              </div>
            </div>

            {error && (
              <div className="py-2 px-3 bg-red-500/10 border border-red-500/30 text-red-500 font-mono text-xs flex items-center gap-2">
                <ShieldAlert className="w-4 h-4" /> {error}
              </div>
            )}

            <button 
              type="submit" 
              disabled={loading}
              className="mt-4 group relative w-full py-4 bg-primary/10 border border-primary text-primary font-mono text-sm tracking-widest uppercase overflow-hidden transition-all duration-300 hover:shadow-[0_0_20px_var(--color-glow)] disabled:opacity-50"
            >
              <div className="absolute inset-0 w-0 bg-primary transition-all duration-300 ease-out group-hover:w-full z-0"></div>
              <span className="relative z-10 group-hover:text-background font-semibold transition-colors duration-300 flex items-center justify-center gap-2">
                {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Authenticating...</> : 'Bypass Firewall'}
              </span>
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}

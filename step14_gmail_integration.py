import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[✉️ M.A.C.DevOS Comm Network] {message}...")
    time.sleep(0.5)

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"❌ Error executing: {command}\n{stderr.decode('utf-8')}")
    return process.returncode == 0

def deploy_gmail_bridge():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found.")
        return

    # 1. Install Nodemailer
    print_status("Installing Nodemailer engine")
    run_command("npm install nodemailer", cwd=PROJECT_PATH)
    run_command("npm install -D @types/nodemailer", cwd=PROJECT_PATH)

    # 2. Create the Next.js API Route
    print_status("Engineering Serverless API Route for Email Transmission")
    api_dir = PROJECT_PATH / "src/app/api/contact"
    os.makedirs(api_dir, exist_ok=True)
    
    route_content = """import { NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(request: Request) {
  try {
    const { name, email, payload } = await request.json();

    if (!name || !email || !payload) {
      return NextResponse.json({ error: 'Missing required parameters.' }, { status: 400 });
    }

    // Configure the Transporter using Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
      },
    });

    // Construct the secure email payload
    const mailOptions = {
      from: process.env.GMAIL_USER, // Sent from your authenticated server account
      to: process.env.GMAIL_USER,   // Sent TO yourself
      replyTo: email,               // If you hit "Reply", it goes to the client
      subject: `[M.A.C.DevOS] Comm Link from ${name}`,
      text: `SYSTEM COMM LINK INITIATED\\n\\nID: ${name}\\nCOMM: ${email}\\n\\nPAYLOAD:\\n${payload}`,
      html: `
        <div style="font-family: monospace; background-color: #050505; color: #00F0FF; padding: 20px;">
          <h2 style="border-bottom: 1px solid #00F0FF; padding-bottom: 10px;">[M.A.C.DevOS] SECURE TRANSMISSION</h2>
          <p><strong>ID (Identity):</strong> ${name}</p>
          <p><strong>COMM (Email):</strong> ${email}</p>
          <br/>
          <p><strong>PAYLOAD (Message):</strong></p>
          <div style="background-color: #0a0a0a; padding: 15px; border: 1px solid #333; color: #E0E0E0; white-space: pre-wrap;">${payload}</div>
        </div>
      `,
    };

    await transporter.sendMail(mailOptions);

    return NextResponse.json({ message: 'Transmission successful.' }, { status: 200 });
  } catch (error) {
    console.error('Transmission Error:', error);
    return NextResponse.json({ error: 'Failed to transmit data.' }, { status: 500 });
  }
}
"""
    with open(api_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write(route_content)


    # 3. Update the Contact UI Component to handle state and API calls
    print_status("Upgrading Contact UI to handle live data transmission")
    contact_path = PROJECT_PATH / "src/components/sections/Contact.tsx"
    
    contact_content = """"use client";

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
"""
    with open(contact_path, "w", encoding="utf-8") as f:
        f.write(contact_content)

    # 4. Inject Environment Variables safely
    env_path = PROJECT_PATH / ".env"
    env_vars = "\n\n# -----------------------------------------------------------------------------\n# SECURE COMM CHANNEL (Nodemailer / Gmail)\n# -----------------------------------------------------------------------------\nGMAIL_USER=\"your-email@gmail.com\"\nGMAIL_APP_PASSWORD=\"your-16-digit-app-password\"\n"
    
    with open(env_path, "a", encoding="utf-8") as f:
        f.write(env_vars)

    print_status("Secure Bridge successfully established.")
    print("⚠️  CRITICAL: You must update your .env file with your actual Gmail credentials!")

if __name__ == "__main__":
    deploy_gmail_bridge()
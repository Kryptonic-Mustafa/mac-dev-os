import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔐 M.A.C.DevOS Security] {message}...")
    time.sleep(0.5)

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"❌ Error executing: {command}\n{stderr.decode('utf-8')}")
    return process.returncode == 0

def deploy_admin_auth():
    # 1. Install Auth Dependencies
    print_status("Injecting Encryption & JWT Dependencies (bcryptjs, jose)")
    run_command("npm install bcryptjs jose", cwd=PROJECT_PATH)
    run_command("npm install -D @types/bcryptjs", cwd=PROJECT_PATH)

    # 2. Add JWT Secret to .env
    env_path = PROJECT_PATH / ".env"
    with open(env_path, "r", encoding="utf-8") as f:
        env_content = f.read()
    
    if "JWT_SECRET" not in env_content:
        with open(env_path, "a", encoding="utf-8") as f:
            f.write('\n\n# -----------------------------------------------------------------------------\n# SECURITY PROTOCOLS\n# -----------------------------------------------------------------------------\nJWT_SECRET="super_secure_macdevos_secret_key_change_in_production"\n')

    # 3. Create Middleware for Route Protection
    print_status("Engineering Edge Middleware to lockdown /admin routes")
    middleware_content = """import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Only protect /admin routes, but allow access to the login page
  if (pathname.startsWith('/admin') && !pathname.startsWith('/admin/login')) {
    const token = request.cookies.get('macdevos_token')?.value;

    if (!token) {
      return NextResponse.redirect(new URL('/admin/login', request.url));
    }

    try {
      const secret = new TextEncoder().encode(process.env.JWT_SECRET);
      await jwtVerify(token, secret);
      return NextResponse.next();
    } catch (error) {
      // Token is invalid or expired
      const response = NextResponse.redirect(new URL('/admin/login', request.url));
      response.cookies.delete('macdevos_token');
      return response;
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*'],
};
"""
    with open(PROJECT_PATH / "src/middleware.ts", "w", encoding="utf-8") as f:
        f.write(middleware_content)

    # 4. Create Setup Route (To create your first admin account)
    print_status("Creating Initial Setup Sequence")
    setup_dir = PROJECT_PATH / "src/app/api/admin/setup"
    os.makedirs(setup_dir, exist_ok=True)
    
    setup_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export async function GET() {
  try {
    // Check if an admin already exists to prevent public exploits
    const existingAdmin = await db.admin.findFirst();
    if (existingAdmin) {
      return NextResponse.json({ error: 'SYSTEM LOCKED: Admin already exists.' }, { status: 403 });
    }

    // Create the master admin account
    const hashedPassword = await bcrypt.hash('admin123', 10);
    
    await db.admin.create({
      data: {
        email: 'admin@macdevos.com',
        password: hashedPassword,
      }
    });

    return NextResponse.json({ 
      message: 'Admin account created successfully.',
      email: 'admin@macdevos.com',
      password: 'admin123'
    }, { status: 201 });

  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Failed to initialize system.' }, { status: 500 });
  }
}
"""
    with open(setup_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write(setup_content)

    # 5. Create Login API Route
    print_status("Engineering Secure Login API")
    login_api_dir = PROJECT_PATH / "src/app/api/admin/login"
    os.makedirs(login_api_dir, exist_ok=True)
    
    login_api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';
import { SignJWT } from 'jose';

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();

    if (!email || !password) {
      return NextResponse.json({ error: 'Invalid parameters.' }, { status: 400 });
    }

    const admin = await db.admin.findUnique({ where: { email } });
    
    if (!admin) {
      return NextResponse.json({ error: 'Unauthorized access.' }, { status: 401 });
    }

    const isValid = await bcrypt.compare(password, admin.password);
    
    if (!isValid) {
      return NextResponse.json({ error: 'Unauthorized access.' }, { status: 401 });
    }

    // Generate JWT Token
    const secret = new TextEncoder().encode(process.env.JWT_SECRET);
    const alg = 'HS256';
    
    const token = await new SignJWT({ id: admin.id, email: admin.email })
      .setProtectedHeader({ alg })
      .setIssuedAt()
      .setExpirationTime('24h')
      .sign(secret);

    // Set HTTP-Only Cookie
    const response = NextResponse.json({ message: 'Access granted.' }, { status: 200 });
    response.cookies.set({
      name: 'macdevos_token',
      value: token,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 60 * 60 * 24, // 1 day
      path: '/',
    });

    return response;

  } catch (error) {
    console.error('Login Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
"""
    with open(login_api_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write(login_api_content)

    # 6. Create the UI Login Page
    print_status("Engineering GSAP Terminal Login Interface")
    login_page_dir = PROJECT_PATH / "src/app/admin/login"
    os.makedirs(login_page_dir, exist_ok=True)
    
    login_page_content = """"use client";

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
"""
    with open(login_page_dir / "page.tsx", "w", encoding="utf-8") as f:
        f.write(login_page_content)

    print_status("Security Protocols Deployed. Middleware active.")

if __name__ == "__main__":
    deploy_admin_auth()
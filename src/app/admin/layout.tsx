"use client";

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  Terminal, 
  LayoutDashboard, 
  FolderKanban, 
  MessageSquare, 
  LogOut, 
  Settings, 
  Quote 
} from 'lucide-react';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  // ISOLATION LOCK: Hide frontend navbar when in admin routes
  useEffect(() => {
    document.documentElement.classList.add('admin-mode');
    return () => document.documentElement.classList.remove('admin-mode');
  }, []);

  if (pathname === '/admin/login') {
    return <>{children}</>;
  }

  const handleLogout = async () => {
    await fetch('/api/admin/logout', { method: 'POST' });
    router.push('/admin/login');
  };

  const navLinks = [
    { name: 'Dashboard', href: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Matrix (Projects)', href: '/admin/projects', icon: FolderKanban },
    { name: 'Comm Channel', href: '/admin/messages', icon: MessageSquare },
    { name: 'Master Settings', href: '/admin/settings', icon: Settings },
    { name: 'Telemetry Logs', href: '/admin/reviews', icon: Quote },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground flex overflow-hidden selection:bg-primary/30">
      
      {/* Sidebar Matrix */}
      <aside className="w-64 border-r border-foreground/10 bg-background/50 backdrop-blur-md hidden md:flex flex-col relative z-20">
        <div className="h-20 border-b border-foreground/10 flex items-center px-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-6 h-6 text-primary" />
            <span className="font-display tracking-widest uppercase text-sm font-bold">M.A.C.DevOS</span>
          </div>
        </div>

        <nav className="flex-1 px-4 py-8 flex flex-col gap-2">
          {navLinks.map((link) => {
            const isActive = pathname.startsWith(link.href);
            return (
              <Link 
                key={link.name} 
                href={link.href}
                className={`flex items-center gap-3 px-4 py-3 font-mono text-xs uppercase tracking-widest transition-all duration-300 border-l-2 ${
                  isActive 
                    ? 'border-primary bg-primary/10 text-primary' 
                    : 'border-transparent text-foreground/50 hover:bg-foreground/5 hover:text-foreground'
                }`}
              >
                <link.icon className="w-4 h-4" />
                {link.name}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-foreground/10">
          <div className="flex items-center gap-2 mb-6 px-4">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-mono text-[10px] text-foreground/40 uppercase tracking-widest">System Online</span>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 font-mono text-xs uppercase tracking-widest text-red-500/70 hover:bg-red-500/10 hover:text-red-500 transition-colors border border-transparent hover:border-red-500/20"
          >
            <LogOut className="w-4 h-4" /> Disconnect
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 relative overflow-y-auto">
        <div className="h-16 border-b border-foreground/10 bg-background/80 backdrop-blur-md md:hidden flex items-center justify-between px-6 sticky top-0 z-30">
          <Terminal className="w-5 h-5 text-primary" />
          <button onClick={handleLogout} className="text-red-500/70 hover:text-red-500">
            <LogOut className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 pt-12 md:p-12 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

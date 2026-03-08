import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_ui_sync():
    # 1. UPDATE SETTINGS UI (Dynamic Dropdown List)
    print_status = lambda m: print(f"[🎨 M.A.C.DevOS UI] {m}...")
    
    settings_ui_path = PROJECT_PATH / "src/app/admin/settings/SettingsUI.tsx"
    settings_ui_content = """"use client";
import { useState } from 'react';
import { Save, Settings2, ShieldCheck, Loader2, CheckCircle2, Plus, Trash2, Github, Linkedin, Twitter, Instagram, Youtube, Globe } from 'lucide-react';

const PLATFORMS = [
  { id: 'github', name: 'GitHub', icon: Github },
  { id: 'linkedin', name: 'LinkedIn', icon: Linkedin },
  { id: 'twitter', name: 'X / Twitter', icon: Twitter },
  { id: 'instagram', name: 'Instagram', icon: Instagram },
  { id: 'youtube', name: 'YouTube', icon: Youtube },
  { id: 'website', name: 'Personal Website', icon: Globe },
];

export default function SettingsUI({ initialSettings }: { initialSettings: any }) {
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [socials, setSocials] = useState<any[]>(initialSettings.socialLinks || []);

  const addSocial = () => setSocials([...socials, { platform: 'github', url: '' }]);
  const removeSocial = (index: number) => setSocials(socials.filter((_, i) => i !== index));
  const updateSocial = (index: number, key: string, val: string) => {
    const next = [...socials];
    next[index][key] = val;
    setSocials(next);
  };

  const handleSave = async (e: any) => {
    e.preventDefault();
    setIsSaving(true);
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    await fetch('/api/admin/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...data, socialLinks: socials })
    });

    setIsSaving(false);
    setSuccess(true);
    setTimeout(() => setSuccess(false), 3000);
  };

  return (
    <div className="w-full flex flex-col gap-10">
      <h1 className="text-3xl font-display text-foreground">Master Settings</h1>

      <form onSubmit={handleSave} className="flex flex-col gap-8 max-w-3xl pb-20">
        <div className="bg-background border border-foreground/10 p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 pb-4 border-b border-foreground/10">
            <Settings2 className="w-5 h-5 text-primary" />
            <h2 className="font-display text-xl">System Identity</h2>
          </div>
          <div className="flex flex-col gap-2">
            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Contact Email</label>
            <input name="contactEmail" defaultValue={initialSettings.contactEmail} className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm text-foreground" />
          </div>
          <div className="flex flex-col gap-2">
            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Site Name</label>
            <input name="siteName" defaultValue={initialSettings.siteName} className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm text-foreground" />
          </div>
        </div>

        <div className="bg-background border border-foreground/10 p-8 flex flex-col gap-6">
          <div className="flex items-center justify-between pb-4 border-b border-foreground/10">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-primary" />
              <h2 className="font-display text-xl">Social Matrix</h2>
            </div>
            <button type="button" onClick={addSocial} className="text-primary hover:text-foreground transition-colors"><Plus className="w-5 h-5" /></button>
          </div>

          <div className="flex flex-col gap-4">
            {socials.map((social, idx) => (
              <div key={idx} className="flex gap-3 items-center animate-in fade-in slide-in-from-top-2">
                <select 
                  value={social.platform} 
                  onChange={(e) => updateSocial(idx, 'platform', e.target.value)}
                  className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary"
                >
                  {PLATFORMS.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
                <input 
                  placeholder="https://..." 
                  value={social.url} 
                  onChange={(e) => updateSocial(idx, 'url', e.target.value)}
                  className="flex-1 bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary" 
                />
                <button type="button" onClick={() => removeSocial(idx)} className="text-red-500/50 hover:text-red-500 transition-colors"><Trash2 className="w-5 h-5" /></button>
              </div>
            ))}
          </div>
        </div>

        <button type="submit" className="flex items-center justify-center gap-3 p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest hover:shadow-neon transition-all">
          {isSaving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
          Execute Sync
        </button>
      </form>
    </div>
  );
}
"""
    with open(settings_ui_path, "w", encoding="utf-8") as f:
        f.write(settings_ui_content)

    # 2. UPDATE FOOTER (Dynamic Icon Rendering)
    footer_path = PROJECT_PATH / "src/components/layout/Footer.tsx"
    footer_content = """"use client";
import { useState, useEffect } from 'react';
import { Terminal, Github, Linkedin, Twitter, Instagram, Youtube, Globe, Mail } from 'lucide-react';

const ICON_MAP: any = {
  github: Github,
  linkedin: Linkedin,
  twitter: Twitter,
  instagram: Instagram,
  youtube: Youtube,
  website: Globe
};

export default function Footer() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    fetch('/api/admin/settings').then(res => res.json()).then(data => setSettings(data));
  }, []);

  return (
    <footer className="w-full py-20 px-6 border-t border-foreground/5 bg-background z-20">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="md:col-span-2 flex flex-col gap-6">
          <div className="flex items-center gap-3">
            <Terminal className="w-5 h-5 text-primary" />
            <span className="font-display uppercase font-bold text-foreground">{settings?.siteName || "M.A.C.DevOS"}</span>
          </div>
          <p className="text-foreground/50 text-sm max-w-sm">Premium digital engineering and UI architecture.</p>
          <div className="flex items-center gap-2 px-3 py-1 border border-emerald-500/20 bg-emerald-500/5 text-emerald-500 w-max rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-mono text-[9px] uppercase tracking-widest">All Systems Operational</span>
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Social Matrix</h4>
          <div className="flex flex-col gap-4">
            {settings?.socialLinks?.map((link: any, i: number) => {
              const Icon = ICON_MAP[link.platform] || Globe;
              return (
                <a key={i} href={link.url} target="_blank" className="flex items-center gap-2 font-mono text-xs text-foreground/60 hover:text-primary transition-all">
                  <Icon className="w-4 h-4" /> {link.platform.toUpperCase()}
                </a>
              );
            })}
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Communicate</h4>
          <a href={`mailto:${settings?.contactEmail || 'macdevos53@gmail.com'}`} className="flex items-center gap-2 font-mono text-xs text-foreground/60 hover:text-primary transition-all">
            <Mail className="w-4 h-4" /> {settings?.contactEmail || "Initialize Link"}
          </a>
        </div>
      </div>
    </footer>
  );
}
"""
    with open(footer_path, "w", encoding="utf-8") as f:
        f.write(footer_content)

if __name__ == "__main__":
    deploy_ui_sync()
import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚀 M.A.C.DevOS Final Sync] {message}...")
    time.sleep(0.5)

def deploy_final_sync():
    # 1. ADD CONTACT EMAIL TO MASTER SETTINGS SCHEMA
    print_status("Updating Schema for Public Contact Email")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_content = f.read()
    
    if "contactEmail" not in schema_content:
        # Using a more robust replacement strategy for Prisma V5/V7
        old_line = "twitterUrl  String?"
        new_line = "twitterUrl  String?\n  contactEmail String?  @default(\"chhabrawalamustafa@gmail.com\")"
        schema_content = schema_content.replace(old_line, new_line)
        
        with open(schema_path, "w", encoding="utf-8") as f:
            f.write(schema_content)
        print("  ✓ Prisma schema updated with contactEmail field.")

    # 2. DYNAMIC FOOTER INTEGRATION
    print_status("Engineering Dynamic Footer with Social Matrix")
    footer_path = PROJECT_PATH / "src/components/layout/Footer.tsx"
    
    footer_content = r""""use client";

import { useState, useEffect } from 'react';
import { Terminal, Github, Linkedin, Twitter, Mail } from 'lucide-react';

export default function Footer() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    fetch('/api/admin/settings')
      .then(res => res.json())
      .then(data => setSettings(data));
  }, []);

  return (
    <footer className="relative w-full py-20 px-6 lg:px-12 border-t border-foreground/5 bg-background z-20">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-8">
        
        <div className="md:col-span-2 flex flex-col gap-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 border border-primary/20 rounded">
              <Terminal className="w-5 h-5 text-primary" />
            </div>
            <span className="font-display tracking-widest uppercase font-bold text-foreground">
              {settings?.siteName || "M.A.C.DevOS"}
            </span>
          </div>
          <p className="text-foreground/50 text-sm max-w-sm leading-relaxed">
            Premium digital engineering and UI architecture. Deploying scalable, high-performance web infrastructure for the modern internet.
          </p>
          <div className="flex items-center gap-2 px-3 py-1.5 border border-emerald-500/20 bg-emerald-500/5 text-emerald-500 w-max rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-mono text-[9px] uppercase tracking-widest">All Systems Operational</span>
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Network</h4>
          <div className="flex flex-col gap-4 font-mono text-xs text-foreground/60">
            {settings?.githubUrl && (
              <a href={settings.githubUrl} target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-primary transition-colors">
                <Github className="w-4 h-4" /> GitHub
              </a>
            )}
            {settings?.linkedinUrl && (
              <a href={settings.linkedinUrl} target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-primary transition-colors">
                <Linkedin className="w-4 h-4" /> LinkedIn
              </a>
            )}
            {settings?.twitterUrl && (
              <a href={settings.twitterUrl} target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-primary transition-colors">
                <Twitter className="w-4 h-4" /> X / Twitter
              </a>
            )}
          </div>
        </div>

        <div>
          <h4 className="font-mono text-[10px] text-foreground/30 uppercase tracking-[0.3em] mb-6">Communicate</h4>
          <a 
            href={`mailto:${settings?.contactEmail || 'chhabrawalamustafa@gmail.com'}`} 
            className="flex items-center gap-2 font-mono text-xs text-foreground/60 hover:text-primary transition-colors"
          >
            <Mail className="w-4 h-4" /> Initialize Link
          </a>
        </div>

      </div>
    </footer>
  );
}
"""
    with open(footer_path, "w", encoding="utf-8") as f:
        f.write(footer_content)

    # 3. SETTINGS UI UPDATE (Add Contact Email Field)
    print_status("Adding Contact Email Control to Master Settings UI")
    settings_ui_path = PROJECT_PATH / "src/app/admin/settings/SettingsUI.tsx"
    
    with open(settings_ui_path, "r", encoding="utf-8") as f:
        ui_content = f.read()
    
    if 'name="contactEmail"' not in ui_content:
        # Create the new input field block
        email_field_html = """
          <div className="flex flex-col gap-2">
            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Public Contact Email (Footer)</label>
            <input name="contactEmail" defaultValue={initialSettings.contactEmail} className="bg-foreground/[0.02] border border-foreground/10 p-3 outline-none focus:border-primary text-sm font-sans w-full" />
          </div>
"""
        # Insert it right before the siteName field
        ui_content = ui_content.replace('<div className="flex flex-col gap-2">\n            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Global Site Name</label>', 
                                        email_field_html + '\n          <div className="flex flex-col gap-2">\n            <label className="font-mono text-[10px] text-foreground/50 tracking-widest uppercase">Global Site Name</label>')
        
        with open(settings_ui_path, "w", encoding="utf-8") as f:
            f.write(ui_content)
        print("  ✓ Settings UI updated with Public Contact Email field.")

    print_status("System fully synchronized and operational.")

if __name__ == "__main__":
    deploy_final_sync()
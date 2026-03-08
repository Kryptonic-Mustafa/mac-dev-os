import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[✨ M.A.C.DevOS Polish] {message}...")
    time.sleep(0.5)

def deploy_polish():
    # 1. INSTALL SWEETALERT2
    print_status("Injecting SweetAlert2 into the System")
    subprocess.run("npm install sweetalert2", shell=True, cwd=PROJECT_PATH)

    # 2. CREATE UPLOAD DIRECTORY
    upload_dir = PROJECT_PATH / "public/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    print_status("Initialized /public/uploads directory")

    # 3. CREATE IMAGE UPLOAD API
    print_status("Engineering Image Upload API")
    api_upload_path = PROJECT_PATH / "src/app/api/admin/upload/route.ts"
    os.makedirs(api_upload_path.parent, exist_ok=True)
    
    upload_api_content = """import { NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import { join } from 'path';

export async function POST(req: Request) {
  try {
    const data = await req.formData();
    const file: File | null = data.get('file') as unknown as File;

    if (!file) {
      return NextResponse.json({ success: false }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Create a unique filename
    const filename = `${Date.now()}-${file.name.replace(/\s+/g, '-')}`;
    const path = join(process.cwd(), 'public/uploads', filename);
    
    await writeFile(path, buffer);
    
    return NextResponse.json({ 
      success: true, 
      url: `/uploads/${filename}` 
    });

  } catch (error) {
    console.error('Upload Error:', error);
    return NextResponse.json({ success: false }, { status: 500 });
  }
}
"""
    with open(api_upload_path, "w", encoding="utf-8") as f:
        f.write(upload_api_content)

    # 4. UPGRADE MASTER SETTINGS (Upload + Swal)
    print_status("Upgrading Master Settings with File Uploads & Alerts")
    settings_ui_path = PROJECT_PATH / "src/app/admin/settings/SettingsUI.tsx"
    
    settings_ui_content = """"use client";
import { useState } from 'react';
import Swal from 'sweetalert2';
import { Save, Settings2, ShieldCheck, Loader2, Plus, Trash2, Github, Linkedin, Twitter, Instagram, Youtube, Globe, Upload } from 'lucide-react';

const PLATFORMS = [
  { id: 'github', name: 'GitHub' },
  { id: 'linkedin', name: 'LinkedIn' },
  { id: 'twitter', name: 'X / Twitter' },
  { id: 'instagram', name: 'Instagram' },
  { id: 'youtube', name: 'YouTube' },
  { id: 'website', name: 'Website' },
];

export default function SettingsUI({ initialSettings }: { initialSettings: any }) {
  const [isSaving, setIsSaving] = useState(false);
  const [socials, setSocials] = useState<any[]>(initialSettings.socialLinks || []);

  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    background: '#0a0a0a',
    color: '#fff',
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  });

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, fieldName: string) => {
    if (!e.target.files?.[0]) return;
    
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/admin/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        const input = document.querySelector(`input[name="${fieldName}"]`) as HTMLInputElement;
        if (input) input.value = data.url;
        Toast.fire({ icon: 'success', title: 'Asset uploaded successfully' });
      }
    } catch (err) {
      Toast.fire({ icon: 'error', title: 'Upload failed' });
    }
  };

  const handleSave = async (e: any) => {
    e.preventDefault();
    setIsSaving(true);
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
      const res = await fetch('/api/admin/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...data, socialLinks: socials })
      });

      if (res.ok) {
        await Toast.fire({ icon: 'success', title: 'System Configuration Updated' });
        window.location.reload();
      }
    } catch (err) {
      Toast.fire({ icon: 'error', title: 'Critical Sync Error' });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="w-full flex flex-col gap-10 pb-20">
      <h1 className="text-3xl font-display text-foreground">Master Settings</h1>

      <form onSubmit={handleSave} className="flex flex-col gap-8 max-w-3xl">
        <div className="bg-background border border-foreground/10 p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 pb-4 border-b border-foreground/10">
            <Settings2 className="w-5 h-5 text-primary" />
            <h2 className="font-display text-xl">Identity Matrix</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 uppercase">Public Contact Email</label>
              <input name="contactEmail" defaultValue={initialSettings.contactEmail} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary" />
            </div>
            <div className="flex flex-col gap-2">
              <label className="font-mono text-[10px] text-foreground/50 uppercase">Global Site Name</label>
              <input name="siteName" defaultValue={initialSettings.siteName} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-sm text-foreground outline-none focus:border-primary" />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
             <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">System Logo</label>
                <div className="flex gap-2">
                  <input name="logoUrl" defaultValue={initialSettings.logoUrl} className="flex-1 bg-foreground/[0.05] border border-foreground/10 p-3 text-xs text-foreground outline-none" />
                  <label className="cursor-pointer p-3 bg-primary/10 border border-primary/30 text-primary hover:bg-primary hover:text-background transition-all">
                    <Upload className="w-4 h-4" />
                    <input type="file" className="hidden" onChange={(e) => handleFileUpload(e, 'logoUrl')} />
                  </label>
                </div>
             </div>
             <div className="flex flex-col gap-2">
                <label className="font-mono text-[10px] text-foreground/50 uppercase">Favicon</label>
                <div className="flex gap-2">
                  <input name="faviconUrl" defaultValue={initialSettings.faviconUrl} className="flex-1 bg-foreground/[0.05] border border-foreground/10 p-3 text-xs text-foreground outline-none" />
                  <label className="cursor-pointer p-3 bg-primary/10 border border-primary/30 text-primary hover:bg-primary hover:text-background transition-all">
                    <Upload className="w-4 h-4" />
                    <input type="file" className="hidden" onChange={(e) => handleFileUpload(e, 'faviconUrl')} />
                  </label>
                </div>
             </div>
          </div>
        </div>

        {/* Dynamic Social Matrix (Retained from previous step) */}
        <div className="bg-background border border-foreground/10 p-8 flex flex-col gap-6">
          <div className="flex items-center justify-between pb-4 border-b border-foreground/10">
            <h2 className="font-display text-xl flex items-center gap-3"><ShieldCheck className="w-5 h-5 text-primary" /> Social Matrix</h2>
            <button type="button" onClick={() => setSocials([...socials, { platform: 'github', url: '' }])} className="text-primary hover:text-foreground"><Plus className="w-5 h-5" /></button>
          </div>
          <div className="flex flex-col gap-4">
            {socials.map((s, i) => (
              <div key={i} className="flex gap-3">
                <select value={s.platform} onChange={(e) => { const n = [...socials]; n[i].platform = e.target.value; setSocials(n); }} className="bg-foreground/[0.05] border border-foreground/10 p-3 text-xs text-foreground outline-none">
                  {PLATFORMS.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
                <input value={s.url} onChange={(e) => { const n = [...socials]; n[i].url = e.target.value; setSocials(n); }} placeholder="https://..." className="flex-1 bg-foreground/[0.05] border border-foreground/10 p-3 text-xs text-foreground outline-none" />
                <button type="button" onClick={() => setSocials(socials.filter((_, idx) => idx !== i))} className="text-red-500/50 hover:text-red-500"><Trash2 className="w-4 h-4" /></button>
              </div>
            ))}
          </div>
        </div>

        <button type="submit" disabled={isSaving} className="w-full p-4 bg-primary text-background font-mono font-bold uppercase tracking-widest hover:shadow-neon transition-all flex items-center justify-center gap-3">
          {isSaving ? <Loader2 className="animate-spin w-5 h-5" /> : <Save className="w-5 h-5" />}
          Finalize Configuration
        </button>
      </form>
    </div>
  );
}
"""
    with open(settings_ui_path, "w", encoding="utf-8") as f:
        f.write(settings_ui_content)

    # 5. FRONTEND CONTACT FORM UPGRADE
    print_status("Polishing Frontend Contact Alerts")
    contact_path = PROJECT_PATH / "src/components/sections/Contact.tsx"
    
    # Check if contact file exists before writing
    if contact_path.exists():
        with open(contact_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Inject SweetAlert into the frontend contact form
        if 'Swal' not in content:
            content = "import Swal from 'sweetalert2';\n" + content
            content = content.replace(
                "alert('Message sent!');",
                "Swal.fire({ icon: 'success', title: 'Transmission Received', text: 'We have received your signal and will respond shortly.', background: '#0a0a0a', color: '#fff', confirmButtonColor: 'var(--color-primary)' }).then(() => window.location.reload());"
            )
            with open(contact_path, "w", encoding="utf-8") as f:
                f.write(content)

    print_status("System-wide alerts and image engine deployed.")

if __name__ == "__main__":
    deploy_polish()
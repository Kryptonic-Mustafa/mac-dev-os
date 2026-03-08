import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS System Patch] {message}...")
    time.sleep(0.5)

def fix_tailwind_v4():
    print_status("Detecting Tailwind v4 Environment")

    # 1. Delete the obsolete Tailwind v3 config file
    old_config = PROJECT_PATH / "tailwind.config.ts"
    if old_config.exists():
        os.remove(old_config)
        print("  ✓ Removed obsolete tailwind.config.ts")

    # 2. Rewrite globals.css with Tailwind v4 syntax
    globals_css_content = """@import "tailwindcss";

@theme {
  /* Colors mapped directly to our CSS Variables */
  --color-background: var(--color-bg-base);
  --color-foreground: var(--color-text-base);
  --color-primary: var(--color-primary);
  --color-secondary: var(--color-secondary);
  --color-glow: var(--color-glow);

  /* Fonts mapped to Next.js font variables */
  --font-sans: var(--font-inter), ui-sans-serif, system-ui, sans-serif;
  --font-display: var(--font-space-grotesk), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-jetbrains-mono), ui-monospace, monospace;

  /* Custom Neon Shadow */
  --shadow-neon: 0 0 20px var(--color-glow), 0 0 40px var(--color-glow);
}

@layer base {
  :root {
    /* Fallback to Neon Blue on SSR before JS injects custom tokens */
    --color-primary: #00F0FF;
    --color-secondary: #0055FF;
    --color-bg-base: #050505;
    --color-text-base: #E0E0E0;
    --color-glow: rgba(0, 240, 255, 0.4);
  }

  body {
    background-color: var(--color-background);
    color: var(--color-foreground);
    overflow-x: hidden;
    transition: background-color 0.5s ease, color 0.5s ease;
  }

  /* Premium OS Custom Scrollbar */
  ::-webkit-scrollbar {
    width: 6px;
  }
  ::-webkit-scrollbar-track {
    background: var(--color-bg-base);
  }
  ::-webkit-scrollbar-thumb {
    background: var(--color-secondary);
    border-radius: 10px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--color-primary);
  }
}
"""
    
    css_path = PROJECT_PATH / "src/app/globals.css"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(globals_css_content)
    print("  ✓ Upgraded globals.css to Tailwind v4 @theme engine")
    
    print_status("Patch applied successfully")

if __name__ == "__main__":
    fix_tailwind_v4()
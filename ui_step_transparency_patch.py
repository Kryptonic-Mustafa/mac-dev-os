import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def apply_transparency_patch():
    print("\n[🪟 M.A.C.DevOS UI Engine] Applying Glassmorphic Transparency Patch...")
    time.sleep(0.5)

    files_to_patch = [
        "src/components/sections/Architecture.tsx",
        "src/components/sections/Projects.tsx"
    ]

    for filepath in files_to_patch:
        full_path = PROJECT_PATH / filepath
        if full_path.exists():
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace solid background with transparent + subtle glass blur
            if "bg-background border-t" in content:
                content = content.replace(
                    "bg-background border-t", 
                    "bg-background/40 border-t backdrop-blur-sm"
                )
                
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✓ Patched: {filepath}")
        else:
            print(f"  ❌ File not found: {filepath}")

    print("\nTransparency patch applied. Global Nexus Background is now visible across all sectors.")

if __name__ == "__main__":
    apply_transparency_patch()
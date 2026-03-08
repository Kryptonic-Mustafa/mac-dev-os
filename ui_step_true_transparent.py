import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def apply_true_transparency():
    print("\n[🪟 M.A.C.DevOS UI Engine] Stripping blocking background layers...")
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

            # Remove the solid background entirely. Leave the border.
            content = content.replace("bg-background border-t", "border-t")
            content = content.replace("bg-background/40 border-t backdrop-blur-sm", "border-t")
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Transparency forced on: {filepath}")
        else:
            print(f"  ❌ File not found: {filepath}")

    print("\nPatch complete. The interactive nexus now flows through the entire system.")

if __name__ == "__main__":
    apply_true_transparency()
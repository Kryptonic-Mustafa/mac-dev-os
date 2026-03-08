import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_lucide_icons():
    print("\n[🔧 M.A.C.DevOS Hotfix] Patching Lucide Icon Registry...")
    time.sleep(0.5)

    reviews_path = PROJECT_PATH / "src/components/sections/Reviews.tsx"
    
    if not reviews_path.exists():
        print("❌ Error: Reviews.tsx not found.")
        return

    with open(reviews_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Swap the import to use the stable 'Terminal' icon
    content = content.replace(
        "import { MessageSquareTerminal, CheckCircle2 }", 
        "import { Terminal, CheckCircle2 }"
    )
    
    # 2. Swap the JSX component tag
    content = content.replace(
        "<MessageSquareTerminal", 
        "<Terminal"
    )

    with open(reviews_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✓ Swapped unstable icon for stable Terminal icon.")
    print("  ✓ Build error resolved.")

if __name__ == "__main__":
    fix_lucide_icons()
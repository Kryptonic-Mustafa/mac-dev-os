import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_missing_icon():
    print("\n[🔧 M.A.C.DevOS Hotfix] Patching missing Terminal icon import...")
    time.sleep(0.5)

    ui_path = PROJECT_PATH / "src/app/admin/dashboard/DashboardUI.tsx"
    
    with open(ui_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Inject Terminal into the lucide-react import
    content = content.replace(
        "import { Activity, FolderKanban, MessageSquare, Cpu } from 'lucide-react';",
        "import { Activity, FolderKanban, MessageSquare, Cpu, Terminal } from 'lucide-react';"
    )

    with open(ui_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✓ Terminal icon successfully imported into the HUD.")

if __name__ == "__main__":
    fix_missing_icon()
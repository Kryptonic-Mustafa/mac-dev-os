import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_layout_icons_final():
    print("\n[🔧 M.A.C.DevOS Hotfix] Repairing Admin Layout Icons...")
    time.sleep(0.5)

    layout_path = PROJECT_PATH / "src/app/admin/layout.tsx"
    
    if not layout_path.exists():
        print(f"❌ Error: {layout_path} not found.")
        return

    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define all required icons for the Phase 4 Admin HUD
    icons = ["Terminal", "LayoutDashboard", "FolderKanban", "MessageSquare", "LogOut", "Settings", "Quote"]
    new_import = f"import {{ {', '.join(icons)} }} from 'lucide-react';"
    
    # Locate the existing lucide-react import block and replace it entirely
    try:
        # This finds the start of the import and the closing of that specific import
        start_idx = content.find("import {")
        end_idx = content.find("} from 'lucide-react';") + len("} from 'lucide-react';")
        
        if start_idx != -1 and end_idx != -1:
            old_import = content[start_idx:end_idx]
            content = content.replace(old_import, new_import)
            
            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  ✓ Admin Layout icons successfully synchronized.")
        else:
            print("❌ Could not locate the import pattern to replace.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    fix_layout_icons_final()
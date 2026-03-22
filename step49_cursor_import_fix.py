import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def fix_cursor_import():
    print_status("Injecting 'useState' into CustomCursor imports")
    cursor_path = PROJECT_PATH / "src/components/ui/CustomCursor.tsx"
    
    if cursor_path.exists():
        with open(cursor_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Look for the line that imports from 'react'
        new_lines = []
        import_fixed = False
        
        for line in lines:
            if "from 'react'" in line and "useState" not in line:
                # Add useState to the list of imports
                if "{" in line and "}" in line:
                    line = line.replace("{", "{ useState, ")
                    import_fixed = True
            new_lines.append(line)
            
        # If we couldn't find a standard curly-brace import, prepend it
        if not import_fixed and "useState" not in "".join(new_lines):
            new_lines.insert(0, "import { useState, useEffect, useRef } from 'react';\n")

        with open(cursor_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print_status("Import successfully patched. Check your terminal for recompilation.")
    else:
        print_status("Error: Could not locate CustomCursor.tsx")

if __name__ == "__main__":
    fix_cursor_import()
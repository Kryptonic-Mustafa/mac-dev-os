import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def fix_advantages_imports():
    print_status("Injecting missing 'useState' and 'useEffect' into Advantages.tsx")
    advantages_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if advantages_path.exists():
        with open(advantages_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        import_fixed = False
        
        for line in lines:
            # Look for the react import line
            if "from 'react'" in line:
                # Ensure useState and useEffect are included
                if "useState" not in line:
                    line = line.replace("{", "{ useState, useEffect, ")
                import_fixed = True
            new_lines.append(line)
            
        # Fallback if the standard react import line wasn't found
        if not import_fixed:
            new_lines.insert(0, "import { useState, useEffect, useLayoutEffect, useRef } from 'react';\n")

        with open(advantages_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        print_status("Imports successfully patched. Ready for deployment.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    fix_advantages_imports()
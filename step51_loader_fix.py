import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def fix_loader_declaration():
    print_status("Declaring 'mounted' state and fixing imports in Loader.tsx")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    if loader_path.exists():
        with open(loader_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. Fix Imports: Ensure useState is included
        if "useState" not in content and "from 'react'" in content:
            content = content.replace("import { useEffect, useRef }", "import { useState, useEffect, useRef }")
            content = content.replace("import { useRef, useEffect }", "import { useState, useRef, useEffect }")
        
        # 2. Fix Function Body: Declare the 'mounted' variable
        if "const [mounted, setMounted] = useState(false);" not in content:
            pattern = "export default function Loader({ onComplete }: { onComplete: () => void }) {"
            # Injecting right at the start of the function body
            replacement = pattern + "\n  const [mounted, setMounted] = useState(false);"
            content = content.replace(pattern, replacement)

        # 3. Fix Effect: Ensure setMounted(true) is called
        if "setMounted(true)" not in content:
            # We add it to the start of the existing useEffect
            content = content.replace("useEffect(() => {", "useEffect(() => {\n    setMounted(true);")

        with open(loader_path, "w", encoding="utf-8") as f:
            f.write(content)
        print_status("Loader declaration patched successfully.")
    else:
        print_status("Error: Loader.tsx not found.")

if __name__ == "__main__":
    fix_loader_declaration()
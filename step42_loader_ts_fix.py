import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Compiler Patch] {message}...")
    time.sleep(0.5)

def apply_loader_fix():
    print_status("Enforcing void return type on Loader cleanup")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    if loader_path.exists():
        with open(loader_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the implicit return with an explicit void block
        old_cleanup = "return () => tl.kill();"
        new_cleanup = "return () => { tl.kill(); };"
        
        if old_cleanup in content:
            content = content.replace(old_cleanup, new_cleanup)
            with open(loader_path, "w", encoding="utf-8") as f:
                f.write(content)
            print_status("Loader cleanup patched successfully.")
        else:
            print_status("Target cleanup string not found. It might already be fixed.")
    else:
        print_status("Error: Loader component not found.")

if __name__ == "__main__":
    apply_loader_fix()
import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Compiler Patch] {message}...")
    time.sleep(0.5)

def apply_ts_fix():
    print_status("Overriding FormData strict types in ProjectsUI")
    ui_path = PROJECT_PATH / "src/app/admin/projects/ProjectsUI.tsx"
    
    if ui_path.exists():
        with open(ui_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the strict inferred type with an 'any' override
        old_string = "const data = Object.fromEntries(formData.entries());"
        new_string = "const data: any = Object.fromEntries(formData.entries());"
        
        if old_string in content:
            content = content.replace(old_string, new_string)
            with open(ui_path, "w", encoding="utf-8") as f:
                f.write(content)
            print_status("TypeScript bypass injected successfully.")
        else:
            print_status("Target string not found. It might already be fixed.")
    else:
        print_status("Error: ProjectsUI file not found.")

if __name__ == "__main__":
    apply_ts_fix()
import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🧹 M.A.C.DevOS Cleanup] {message}...")
    time.sleep(0.5)

def clean_syntax_error():
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            # If the line contains the illegal Python comment, skip adding it (delete it)
            if "# import { ScrollToPlugin }" in line:
                continue
            new_lines.append(line)

        with open(adv_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        print_status("Illegal syntax removed. The matrix is clean.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    clean_syntax_error()
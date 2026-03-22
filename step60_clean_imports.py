import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🧹 M.A.C.DevOS Cleanup] {message}...")
    time.sleep(0.5)

def clean_advantages_import():
    advantages_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if advantages_path.exists():
        with open(advantages_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            # If this is the react import line, replace it entirely with the correct, clean version
            if "from 'react'" in line:
                line = "import { useState, useEffect, useRef, useLayoutEffect } from 'react';\n"
            new_lines.append(line)

        with open(advantages_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        print_status("Duplicate 'useEffect' removed. Import line is perfectly clean.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    clean_advantages_import()
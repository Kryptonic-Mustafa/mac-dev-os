import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def fix_typescript_parse():
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Target the exact line causing the error
        old_line = "const currentProgress = gsap.utils.normalize(0, -maxScroll, sliderRef.current?.style.transform.match(/translate\(([-\\d.]+)/)?.[1] || 0);"
        
        # Wrap the regex result in parseFloat() to satisfy TypeScript
        new_line = "const currentProgress = gsap.utils.normalize(0, -maxScroll, parseFloat(sliderRef.current?.style.transform.match(/translate\\(([-\\d.]+)/)?.[1] || '0'));"
        
        # If the exact old line isn't found (maybe spacing differs), do a more general replace
        if old_line in content:
             content = content.replace(old_line, new_line)
        else:
             # Fallback replace for the specific problematic part
             content = content.replace(
                 "sliderRef.current?.style.transform.match(/translate\\(([-\\d.]+)/)?.[1] || 0",
                 "parseFloat(sliderRef.current?.style.transform.match(/translate\\(([-\\d.]+)/)?.[1] || '0')"
             )

        with open(adv_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print_status("TypeScript Type Error resolved. String successfully parsed to float.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    fix_typescript_parse()
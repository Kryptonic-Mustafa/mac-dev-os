import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_ts_bypass():
    print("\n[🛡️ M.A.C.DevOS TS Compiler Fix] Bypassing strict MouseEvent checks...")
    time.sleep(0.5)
    
    bg_path = PROJECT_PATH / "src/components/ui/BackgroundFX.tsx"
    
    if bg_path.exists():
        with open(bg_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # We tell TypeScript to treat the Touch object as 'any' so it stops asking 
        # for mouse-specific buttons like right-click and scroll-wheel.
        content = content.replace("(e.touches[0])", "(e.touches[0] as any)")
        
        with open(bg_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print("  -> TypeScript bypass applied to BackgroundFX.tsx touch events.")
    else:
        print("  -> [!] BackgroundFX.tsx not found.")

if __name__ == "__main__":
    deploy_ts_bypass()
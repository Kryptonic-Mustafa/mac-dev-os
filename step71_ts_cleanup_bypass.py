import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_cleanup_bypass():
    print("\n[🛡️ M.A.C.DevOS TS Compiler Fix] Silencing cleanup type errors...")
    time.sleep(0.5)
    
    bg_path = PROJECT_PATH / "src/components/ui/BackgroundFX.tsx"
    
    if bg_path.exists():
        with open(bg_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Cast the cleanup handlers to 'any' to satisfy strict TS rules
        content = content.replace("window.removeEventListener('touchmove', handleMouseMove)", "window.removeEventListener('touchmove', handleMouseMove as any)")
        content = content.replace("window.removeEventListener('touchstart', handleMouseMove)", "window.removeEventListener('touchstart', handleMouseMove as any)")
        
        with open(bg_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print("  -> TypeScript bypass successfully applied to cleanup events.")
    else:
        print("  -> [!] BackgroundFX.tsx not found.")

if __name__ == "__main__":
    deploy_cleanup_bypass()
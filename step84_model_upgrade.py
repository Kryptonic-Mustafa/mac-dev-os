import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_model_upgrade():
    print("\n[🧠 M.A.C.DevOS Neural Engine] Upgrading to Gemini 2.5 Flash Architecture...")
    time.sleep(0.5)
    
    route_path = PROJECT_PATH / "src/app/api/chat/route.ts"
    
    if route_path.exists():
        with open(route_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Swap the deprecated 1.5 model for the active 2.5 model
        if 'model: "gemini-1.5-flash"' in content:
            content = content.replace('model: "gemini-1.5-flash"', 'model: "gemini-2.5-flash"')
            
            with open(route_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            print("  -> Backend successfully routed to gemini-2.5-flash!")
        else:
            print("  -> [!] Could not find 'gemini-1.5-flash' in route.ts.")
    else:
        print("  -> [!] route.ts not found.")

if __name__ == "__main__":
    deploy_model_upgrade()
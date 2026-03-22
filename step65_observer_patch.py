import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🛠️ M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def fix_gsap_observer():
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Import Observer alongside ScrollTrigger
        if "Observer" not in content and "from 'gsap/ScrollTrigger'" in content:
            content = content.replace("import { ScrollTrigger } from 'gsap/ScrollTrigger';", 
                                      "import { ScrollTrigger } from 'gsap/ScrollTrigger';\nimport { Observer } from 'gsap/Observer';")

        # 2. Register the plugin
        if "gsap.registerPlugin(ScrollTrigger);" in content and "Observer" not in content.split("gsap.registerPlugin")[1].split(";")[0]:
             content = content.replace("gsap.registerPlugin(ScrollTrigger);", 
                                       "gsap.registerPlugin(ScrollTrigger, Observer);")
             
        # 3. Fix the syntax from gsap.addObserver to Observer.create
        if "gsap.addObserver({" in content:
             content = content.replace("gsap.addObserver({", "Observer.create({")

        with open(adv_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print_status("GSAP Observer successfully imported and registered.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    fix_gsap_observer()
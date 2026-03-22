import os
import re
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_touch_mastery():
    print("\n[🔥 M.A.C.DevOS Emergency Unlock] Deploying...")
    time.sleep(0.5)
    
    # 1. UNLOCK THE SLIDER
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            adv_content = f.read()
        
        # The culprit: touch-pan-y. We replace it with touch-auto.
        adv_content = adv_content.replace("touch-pan-y", "touch-auto")
        
        with open(adv_path, "w", encoding="utf-8") as f:
            f.write(adv_content)
        print("  -> [1/2] Advantages Slider UNLOCKED (CSS touch constraints destroyed).")

    # 2. RESTORE THE 8-LEGGED MATRIX
    bg_path = PROJECT_PATH / "src/components/ui/BackgroundFX.tsx"
    if bg_path.exists():
        with open(bg_path, "r", encoding="utf-8") as f:
            bg_content = f.read()
        
        # Revert the faulty pointermove back to mousemove for stable desktop
        bg_content = bg_content.replace("'pointermove'", "'mousemove'")
        
        # Dynamically find the mousemove handler and inject explicit touch events
        match = re.search(r"addEventListener\(['\"]mousemove['\"],\s*([a-zA-Z0-9_]+)\)", bg_content)
        if match:
            handler = match.group(1)
            if "'touchmove'" not in bg_content:
                # Inject touch listeners that extract the exact finger coordinates
                bg_content = re.sub(
                    rf"addEventListener\(['\"]mousemove['\"],\s*{handler}\);?",
                    f"addEventListener('mousemove', {handler});\n    window.addEventListener('touchmove', (e) => {handler}(e.touches[0]), {{ passive: true }});\n    window.addEventListener('touchstart', (e) => {handler}(e.touches[0]), {{ passive: true }});",
                    bg_content
                )
                # Inject cleanup
                bg_content = re.sub(
                    rf"removeEventListener\(['\"]mousemove['\"],\s*{handler}\);?",
                    f"removeEventListener('mousemove', {handler});\n      window.removeEventListener('touchmove', {handler});\n      window.removeEventListener('touchstart', {handler});",
                    bg_content
                )
                with open(bg_path, "w", encoding="utf-8") as f:
                    f.write(bg_content)
                print("  -> [2/2] 8-Legged Canvas wired directly to native Touch API.")
            else:
                print("  -> [2/2] Touch events already present in BackgroundFX.")
        else:
            print("  -> [!] Could not auto-detect the mouse handler. If spider still fails, please share BackgroundFX.tsx.")

if __name__ == "__main__":
    deploy_touch_mastery()
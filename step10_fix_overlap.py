import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_gsap_overlap():
    print("\n[🔧 M.A.C.DevOS UI Engine] Patching GSAP Pin Spacer Collision...")
    time.sleep(0.5)

    # 1. Fix globals.css (Remove the conflicting overflow rule)
    css_path = PROJECT_PATH / "src/app/globals.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        # Strip out the problematic rule
        if "overflow-x: hidden;" in css_content:
            css_content = css_content.replace("overflow-x: hidden;", "/* overflow-x removed for GSAP pin compatibility */")
            with open(css_path, "w", encoding="utf-8") as f:
                f.write(css_content)
            print("  ✓ Removed conflicting overflow-x from globals.css")

    # 2. Reinforce the Advantages GSAP Logic
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            adv_content = f.read()

        # We will add invalidateOnRefresh to ensure it recalculates properly on any screen size change
        old_trigger = """scrollTrigger: {
        trigger: containerRef.current,
        pin: true,
        scrub: 1,
        snap: 1 / (sections.length - 1),
        end: () => "+=" + scrollTrackRef.current?.offsetWidth,
      }"""
        
        new_trigger = """scrollTrigger: {
        trigger: containerRef.current,
        pin: true,
        scrub: 1,
        pinSpacing: true,
        invalidateOnRefresh: true,
        snap: 1 / (sections.length - 1),
        end: () => "+=" + scrollTrackRef.current?.offsetWidth,
      }"""

        if old_trigger in adv_content:
            adv_content = adv_content.replace(old_trigger, new_trigger)
            with open(adv_path, "w", encoding="utf-8") as f:
                f.write(adv_content)
            print("  ✓ Reinforced GSAP ScrollTrigger config in Advantages.tsx")

    print("\nPatch complete. The horizontal matrix should now securely push the System Matrix down.")

if __name__ == "__main__":
    fix_gsap_overlap()
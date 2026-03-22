import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📐 M.A.C.DevOS Layout Engine] {message}...")
    time.sleep(0.5)

def fix_gsap_overlap():
    adv_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if adv_path.exists():
        with open(adv_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Fortify the Section Container (Add relative z-30 to block overlapping elements)
        content = content.replace(
            'className="py-20 bg-background text-foreground overflow-hidden"',
            'className="py-20 bg-background text-foreground overflow-hidden relative z-30"'
        )

        # 2. Upgrade the Desktop GSAP Logic with strict pinSpacing and dynamic bounds
        old_desktop_logic = """    // DESKTOP ONLY: Cinematic ScrollTrigger
    mm.add("(min-width: 768px)", () => {
      let sections = gsap.utils.toArray(".adv-card");
      const totalWidth = sliderRef.current?.offsetWidth || 0;
      
      gsap.to(sections, {
        xPercent: -100 * (sections.length - 1),
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          pin: true,
          scrub: 1,
          snap: 1 / (sections.length - 1),
          end: () => "+=" + totalWidth,
          onUpdate: (self) => setProgress(Math.round(self.progress * 100))
        }
      });
    });"""

        new_desktop_logic = """    // DESKTOP ONLY: Cinematic ScrollTrigger
    mm.add("(min-width: 768px)", () => {
      let sections = gsap.utils.toArray(".adv-card");
      
      gsap.to(sections, {
        xPercent: -100 * (sections.length - 1),
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          pin: true,
          pinSpacing: true, // Strictly enforces the spacer to push next sections down
          scrub: 1,
          snap: 1 / (sections.length - 1),
          // Dynamically grab the true scroll width to prevent math errors
          end: () => "+=" + (sliderRef.current?.scrollWidth || window.innerWidth),
          invalidateOnRefresh: true, // Recalculate spacer if layout shifts
          onUpdate: (self) => setProgress(Math.round(self.progress * 100))
        }
      });
    });"""

        # Replace the logic block if the exact old logic is found
        if "end: () => \"+=\" + totalWidth," in content:
            content = content.replace(old_desktop_logic, new_desktop_logic)
        else:
            # Fallback if spacing is slightly different
            content = content.replace("end: () => \"+=\" + totalWidth,", "end: () => \"+=\" + (sliderRef.current?.scrollWidth || window.innerWidth),\n          pinSpacing: true,\n          invalidateOnRefresh: true,")

        with open(adv_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print_status("GSAP Boundaries recalculated. Z-Index fortified.")
    else:
        print_status("Error: Advantages.tsx not found.")

if __name__ == "__main__":
    fix_gsap_overlap()
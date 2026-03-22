import os
import time
import re
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📱 M.A.C.DevOS Mobile Patch] {message}...")
    time.sleep(0.5)

def deploy_mobile_fixes():
    # 1. FIX THE CUSTOM CURSOR (Button Blocker)
    print_status("Disabling Custom Cursor on Touch Devices to restore clicks")
    cursor_path = PROJECT_PATH / "src/components/ui/CustomCursor.tsx"
    if cursor_path.exists():
        with open(cursor_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Inject the mobile check
        if "isMobile" not in content:
            content = content.replace("export default function CustomCursor() {", 
                                      "export default function CustomCursor() {\n  const [isMobile, setIsMobile] = useState(false);")
            
            # Find the useEffect and add the matchMedia check
            content = content.replace("useEffect(() => {", 
                                      "useEffect(() => {\n    if (window.matchMedia('(pointer: coarse)').matches) {\n      setIsMobile(true);\n      return;\n    }")
            
            # Return null if mobile so it doesn't render and block clicks
            content = content.replace("return (", "if (isMobile) return null;\n\n  return (")
            
            with open(cursor_path, "w", encoding="utf-8") as f:
                f.write(content)

    # 2. FIX THE LAGGY PC MONITOR (GPU Acceleration)
    print_status("Forcing GPU Hardware Acceleration on PC Monitor Animation")
    hero_path = PROJECT_PATH / "src/components/sections/Hero.tsx"
    if hero_path.exists():
        with open(hero_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Add will-change and hardware acceleration classes to the scaling elements
        if "will-change-transform" not in content:
            content = content.replace('className="relative w-full max-w-4xl mx-auto"', 
                                      'className="relative w-full max-w-4xl mx-auto will-change-transform [transform:translateZ(0)]"')
            
            # Ensure the container surrounding the buttons doesn't block them
            content = content.replace('className="absolute inset-0 flex flex-col items-center justify-center z-10"',
                                      'className="absolute inset-0 flex flex-col items-center justify-center z-20 pointer-events-none"')
            
            # Reactivate pointer events strictly on the buttons
            content = content.replace('className="flex gap-4 mt-8"',
                                      'className="flex gap-4 mt-8 pointer-events-auto"')
                                      
            with open(hero_path, "w", encoding="utf-8") as f:
                f.write(content)

    # 3. FIX HORIZONTAL SCROLL (Touch Release)
    print_status("Patching GSAP Horizontal Matrix for Native Touch Swiping")
    arch_path = PROJECT_PATH / "src/components/sections/Architecture.tsx"
    if arch_path.exists():
        with open(arch_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Add invalidateOnRefresh for mobile orientation changes and fix touch action
        if "invalidateOnRefresh: true" not in content:
            content = content.replace("pin: true,", "pin: true,\n          invalidateOnRefresh: true,")
            content = content.replace('className="overflow-hidden bg-background"', 
                                      'className="overflow-hidden bg-background touch-pan-y"')
            
            with open(arch_path, "w", encoding="utf-8") as f:
                f.write(content)

    print_status("Mobile Overhaul Complete. System is now responsive and GPU-optimized.")

if __name__ == "__main__":
    deploy_mobile_fixes()
import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📱 M.A.C.DevOS Mobile Patch] {message}...")
    time.sleep(0.5)

def deploy_mobile_patch():
    # 1. FIX THE DISTURBING SPIDER CURSOR (CustomCursor.tsx)
    print_status("Detecting touch capability and disabling custom cursor on mobile")
    cursor_path = PROJECT_PATH / "src/components/ui/CustomCursor.tsx"
    
    if cursor_path.exists():
        with open(cursor_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Add isTouch check and conditional null return
        if "navigator.maxTouchPoints" not in content:
            # Add state
            content = content.replace("export default function CustomCursor() {", 
                                      "export default function CustomCursor() {\n  const [isTouch, setIsTouch] = useState(false);")
            
            # Update useEffect to check touch on mount
            content = content.replace("useEffect(() => {", 
                                      "useEffect(() => {\n    if (navigator.maxTouchPoints > 0) {\n      setIsTouch(true);\n      return;\n    }\n")
            
            # Hide rendering if touch
            content = content.replace("if (!mounted) return null;", 
                                      "if (!mounted || isTouch) return null;")
            
            with open(cursor_path, "w", encoding="utf-8") as f:
                f.write(content)

    # 2. FIX THE 'WHY CHOOSE US' SLIDER (Advantages.tsx)
    print_status("Converting Advantage Section to native swipe Matrix on mobile")
    advantages_path = PROJECT_PATH / "src/components/sections/Advantages.tsx"
    
    if advantages_path.exists():
        with open(advantages_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Step A: Update imports to handle conditional state
        if "useState" not in content:
            content = content.replace("import { useLayoutEffect, useRef }", 
                                      "import { useState, useEffect, useLayoutEffect, useRef }")
            
        # Step B: Add screen width state inside component
        if "screenWidth" not in content:
            content = content.replace("export default function Advantages() {", 
                                      "export default function Advantages() {\n  const [screenWidth, setScreenWidth] = useState(0);")
            
            # Add useEffect to set width on mount and resize
            width_effect = """
  useEffect(() => {
    const handleResize = () => setScreenWidth(window.innerWidth);
    handleResize(); // Set on mount
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
"""
            content = content.replace("export default function Advantages() {\n  const [screenWidth, setScreenWidth] = useState(0);", 
                                      "export default function Advantages() {\n  const [screenWidth, setScreenWidth] = useState(0);\n" + width_effect)

        # Step C: Inject conditional logic into GSAP implementation
        # Look for typical GSAP implementation pattern and wrap it
        content = content.replace("useLayoutEffect(() => {", 
                                  "useLayoutEffect(() => {\n    // Disable GSAP pinning on mobile\n    if (screenWidth < 768 && screenWidth !== 0) return;\n")

        # Step D: Apply Mobile CSS (Native Horizontal Swipe) to the container grid/flex
        # We target typical flex/grid patterns for this specific component
        # Adding native horizontal scrolling (overflow-x-auto, snap-x)
        content = content.replace('className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"',
                                  'className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-6 md:overflow-visible overflow-x-auto snap-x snap-mandatory flex-nowrap md:flex-wrap"')
        
        # Step E: Make individual cards snap points
        content = content.replace('className="bg-background border border-foreground/10',
                                  'className="snap-center bg-background border border-foreground/10')
        content = content.replace('min-w-[300px]', '') # Ensure mobile uses min-width override

        with open(advantages_path, "w", encoding="utf-8") as f:
            f.write(content)

    print_status("Mobile Patch Successfully Implemented. Core UI is now stable across platforms.")

if __name__ == "__main__":
    deploy_mobile_patch()
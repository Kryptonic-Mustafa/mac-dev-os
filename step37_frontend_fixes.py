import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS UI Patch] {message}...")
    time.sleep(0.5)

def apply_frontend_fixes():
    # 1. FIX THE REVIEW RENDERER (GSAP fromTo override)
    print_status("Fixing GSAP Opacity Conflict in Telemetry Logs")
    reviews_path = PROJECT_PATH / "src/components/sections/Reviews.tsx"
    
    if reviews_path.exists():
        with open(reviews_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the broken gsap.from with a forceful gsap.fromTo
        old_gsap = """gsap.from(".log-card", {
      opacity: 0, y: 50, stagger: 0.1, duration: 0.8,
      scrollTrigger: { trigger: containerRef.current, start: "top 80%" }
    });"""
        new_gsap = """gsap.fromTo(".log-card", 
      { opacity: 0, y: 50 }, 
      { opacity: 1, y: 0, stagger: 0.1, duration: 0.8,
        scrollTrigger: { trigger: containerRef.current, start: "top 80%" }
      }
    );"""
        
        content = content.replace(old_gsap, new_gsap)
        
        with open(reviews_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 2. FIX THE CURSOR TARGET IN LOADER
    print_status("Re-calibrating Mouse Target Coordinates")
    loader_path = PROJECT_PATH / "src/components/ui/Loader.tsx"
    
    if loader_path.exists():
        with open(loader_path, "r", encoding="utf-8") as f:
            loader_content = f.read()
        
        # Adjust the 'y' coordinate from 20 (too low) to -5 (centered vertically on text)
        # Adjust the 'x' coordinate to move slightly right into the button body
        old_mouse = """{ x: 0, y: 20, opacity: 1, scale: 1, duration: 1.5, ease: "power3.inOut" }"""
        new_mouse = """{ x: 25, y: -2, opacity: 1, scale: 1, duration: 1.5, ease: "power3.inOut" }"""
        
        loader_content = loader_content.replace(old_mouse, new_mouse)
        
        with open(loader_path, "w", encoding="utf-8") as f:
            f.write(loader_content)

    print_status("UI Glitches Patched Successfully.")

if __name__ == "__main__":
    apply_frontend_fixes()
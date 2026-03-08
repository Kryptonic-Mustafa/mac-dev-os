import os
import time
import re
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[⏪ M.A.C.DevOS Rollback] {message}...")
    time.sleep(0.5)

def execute_rollback():
    # 1. FIX CSS (RESTORE SCROLL)
    print_status("Removing broken CSS locks to restore mouse scroll")
    css_path = PROJECT_PATH / "src/app/globals.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        # Regex to target and remove the exact block added in Step 38
        css_content = re.sub(r'/\* OS OPTIMIZATIONS \*/.*?perspective: 1000px;\n}\n', '', css_content, flags=re.DOTALL)
        
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)

    # 2. REMOVE LAGGY COMPONENT FROM PAGE
    print_status("Extracting experimental parallax engine from main page")
    page_path = PROJECT_PATH / "src/app/page.tsx"
    if page_path.exists():
        with open(page_path, "r", encoding="utf-8") as f:
            page_content = f.read()

        # Remove the import and the component tag
        page_content = page_content.replace("import InteractiveBackground from '@/components/ui/InteractiveBackground';\n", "")
        page_content = page_content.replace("      <InteractiveBackground />\n", "")
        page_content = page_content.replace("<InteractiveBackground />", "")

        with open(page_path, "w", encoding="utf-8") as f:
            f.write(page_content)

    # 3. DELETE THE FILE
    print_status("Purging experimental background file")
    bg_path = PROJECT_PATH / "src/components/ui/InteractiveBackground.tsx"
    if bg_path.exists():
        os.remove(bg_path)

    print_status("Rollback complete. The OS has been restored to the stable checkpoint.")

if __name__ == "__main__":
    execute_rollback()
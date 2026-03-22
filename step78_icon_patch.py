import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def patch_chatbot_icon():
    print("\n[🎨 M.A.C.DevOS UI Patch] Swapping missing icon for universal fallback...")
    time.sleep(0.5)
    
    chatbot_path = PROJECT_PATH / "src/components/ui/Chatbot.tsx"
    
    if chatbot_path.exists():
        with open(chatbot_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. Fix the import statement
        content = content.replace("MessageSquareTerminal", "MessageSquare")
        
        # 2. Fix the actual JSX component tag
        content = content.replace("<MessageSquareTerminal", "<MessageSquare")
        
        with open(chatbot_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print("  -> Icon successfully patched to 'MessageSquare'. Compiler should now pass.")
    else:
        print("  -> [!] Chatbot.tsx not found in src/components/ui/")

if __name__ == "__main__":
    patch_chatbot_icon()
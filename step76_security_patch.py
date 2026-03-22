import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_security_patch():
    print("\n[🛡️ M.A.C.DevOS Security Patch] Patching vault script to ignore secrets...")
    time.sleep(0.5)
    
    step57_path = PROJECT_PATH / "step57_backup_and_push.py"
    
    if step57_path.exists():
        with open(step57_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add .env and .env.local to the ignore list during zipping
        old_ignore = "ignore_dirs = {'.git', 'node_modules', '.next', '.vercel', '__pycache__', 'bkp', 'from_server'}"
        new_ignore = "ignore_dirs = {'.git', 'node_modules', '.next', '.vercel', '__pycache__', 'bkp', 'from_server', '.env', '.env.local'}"
        
        if old_ignore in content:
            content = content.replace(old_ignore, new_ignore)
            with open(step57_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  -> Vault script patched. Secrets will no longer be zipped.")
        else:
            print("  -> Warning: Could not find the exact ignore_dirs line to replace.")
    else:
         print("  -> [!] step57_backup_and_push.py not found.")

if __name__ == "__main__":
    deploy_security_patch()
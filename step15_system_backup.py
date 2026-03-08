import os
import time
import zipfile
from pathlib import Path

PROJECT_PATH = Path.cwd()
# We will place the backup ONE folder level UP so it doesn't clutter your project workspace
BACKUP_DIR = PROJECT_PATH.parent / "MACDevOS_Backups"

def print_status(message):
    print(f"\n[💾 M.A.C.DevOS Storage Matrix] {message}...")
    time.sleep(0.5)

def create_system_snapshot():
    if not (PROJECT_PATH / "package.json").exists():
        print("❌ Error: 'package.json' not found. Ensure you are in the correct directory.")
        return

    print_status("Initializing System Snapshot")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    zip_filename = BACKUP_DIR / f"mac-dev-os_v1_frontend_stable_{timestamp}.zip"
    
    # Directories we DO NOT want to zip (they are huge and easily rebuilt via npm install)
    ignore_dirs = {'.next', 'node_modules', '.git'}

    print_status(f"Compressing architecture (Excluding {', '.join(ignore_dirs)})")
    
    file_count = 0
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_PATH):
            # Mutate the dirs list in-place to prevent os.walk from entering ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file.endswith('.zip'): 
                    continue # Prevent inception
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PROJECT_PATH)
                zipf.write(file_path, arcname)
                file_count += 1

    print_status(f"Snapshot Complete! {file_count} files secured.")
    print(f"  ✓ Archive saved to: {zip_filename}")

if __name__ == "__main__":
    create_system_snapshot()
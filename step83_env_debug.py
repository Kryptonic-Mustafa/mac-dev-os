import os
import time
import shutil
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_env_debug():
    print("\n[🛠️ M.A.C.DevOS Diagnostics] Injecting Environment Debugger...")
    time.sleep(0.5)
    
    # 1. Inject the Debug Log into the API Route
    route_path = PROJECT_PATH / "src/app/api/chat/route.ts"
    if route_path.exists():
        with open(route_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        debug_log = """
    // --- DEBUG CHECK ---
    console.log("====== NEURAL ENGINE DIAGNOSTICS ======");
    console.log("API Key Exists?:", !!process.env.GEMINI_API_KEY);
    console.log("API Key Length:", process.env.GEMINI_API_KEY ? process.env.GEMINI_API_KEY.length : 0);
    console.log("=======================================");
    """
        # Inject right after try {
        if "try {" in content and "DIAGNOSTICS" not in content:
            content = content.replace("try {", f"try {{{debug_log}")
            with open(route_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("  -> Debugger injected into /api/chat/route.ts")
    
    # 2. Obliterate the Next.js Cache
    next_cache = PROJECT_PATH / ".next"
    if next_cache.exists():
        try:
            shutil.rmtree(next_cache)
            print("  -> Turbopack build cache obliterated. Forced hard reset.")
        except Exception as e:
            print(f"  -> [!] Could not delete .next folder. Is the dev server still running? Stop it first.")

if __name__ == "__main__":
    deploy_env_debug()
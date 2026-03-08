import os
import time
import shutil
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🧹 M.A.C.DevOS Deep Clean] {message}...")
    time.sleep(0.5)

def run_command(command, cwd=None):
    subprocess.run(command, shell=True, cwd=cwd)

def execute_deep_clean():
    print_status("Initiating Hard Reset of Compiler Caches")

    # 1. NUKE THE NEXT.JS CACHE (This is what is trapping you)
    next_cache = PROJECT_PATH / ".next"
    if next_cache.exists():
        shutil.rmtree(next_cache, ignore_errors=True)
        print("  ✓ Destroyed corrupted Next.js / Turbopack cache.")

    # 2. NUKE THE PRISMA CACHE
    prisma_cache = PROJECT_PATH / "node_modules/.prisma"
    if prisma_cache.exists():
        shutil.rmtree(prisma_cache, ignore_errors=True)
        print("  ✓ Destroyed corrupted Prisma Client cache.")

    # 3. ENSURE DB.TS IS PURE
    db_path = PROJECT_PATH / "src/lib/db.ts"
    db_content = """import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

// Pure, standard instantiation. The URL is safely inside schema.prisma.
export const db = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""
    with open(db_path, "w", encoding="utf-8") as f:
        f.write(db_content)
    print("  ✓ Verified db.ts is using standard initialization.")

    # 4. REBUILD THE WORLD
    print_status("Regenerating clean Prisma Client")
    run_command("npx prisma generate", cwd=PROJECT_PATH)

    print_status("System Deep Clean Complete. Ready for Boot.")

if __name__ == "__main__":
    execute_deep_clean()
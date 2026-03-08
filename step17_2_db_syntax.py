import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_db_syntax():
    print("\n[🔧 M.A.C.DevOS Hotfix] Updating Prisma Client to strict V7 syntax...")
    time.sleep(0.5)

    db_path = PROJECT_PATH / "src/lib/db.ts"
    
    db_content = """import { PrismaClient } from '@prisma/client';

// Cache the Prisma instance in development to prevent connection exhaustion
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

// V7 requires the strict 'datasourceUrl' property instead of the legacy nested object
export const db = globalForPrisma.prisma ?? new PrismaClient({
  datasourceUrl: process.env.DATABASE_URL,
});

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""
    with open(db_path, "w", encoding="utf-8") as f:
        f.write(db_content)

    print("  ✓ Prisma Client successfully updated to V7 syntax.")

if __name__ == "__main__":
    fix_db_syntax()
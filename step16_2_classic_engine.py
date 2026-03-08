import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def deploy_classic_engine():
    # 1. Create/Update prisma.config.ts to use the Classic Engine
    print_status("Configuring Prisma to use the stable Classic Engine")
    config_content = """import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  engine: "classic",
  datasource: {
    url: env("DATABASE_URL"),
  },
});
"""
    with open(PROJECT_PATH / "prisma.config.ts", "w", encoding="utf-8") as f:
        f.write(config_content)

    # 2. Revert db.ts to standard initialization
    print_status("Re-architecting Database Singleton")
    db_content = """import { PrismaClient } from '@prisma/client';

// Cache the Prisma instance in development to prevent connection exhaustion
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""
    with open(PROJECT_PATH / "src/lib/db.ts", "w", encoding="utf-8") as f:
        f.write(db_content)

    print_status("Classic Engine Patch Complete!")

if __name__ == "__main__":
    deploy_classic_engine()
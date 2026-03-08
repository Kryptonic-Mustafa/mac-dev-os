import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS Social Matrix] {message}...")
    time.sleep(0.5)

def deploy_social_matrix():
    # 1. UPGRADE PRISMA SCHEMA (Using JSON for flexibility)
    print_status("Re-architecting System Settings Schema")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    
    schema_content = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

model Admin {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   
  createdAt DateTime @default(now())
}

model Project {
  id          String   @id @default(uuid())
  systemId    String   @unique 
  title       String
  description String   @db.Text
  tech        String   
  repoLink    String?
  liveLink    String?
  order       Int      @default(0)
  isVisible   Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Message {
  id        String   @id @default(uuid())
  name      String
  email     String
  payload   String   @db.Text
  isRead    Boolean  @default(false)
  createdAt DateTime @default(now())
}

model SystemSettings {
  id           String   @id @default("master_config")
  siteName     String   @default("M.A.C.DevOS")
  logoUrl      String?  
  faviconUrl   String?
  contactEmail String?  @default("macdevos53@gmail.com")
  socialLinks  Json?    // Storing as [{ platform: 'github', url: '...' }]
  updatedAt    DateTime @updatedAt
}
"""
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(schema_content)

    # Sync Database
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # 2. UPDATE PUBLIC API (Force Fresh Data)
    print_status("Updating Public API for Zero-Latency Fetch")
    api_path = PROJECT_PATH / "src/app/api/admin/settings/route.ts"
    api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET() {
  const settings = await db.systemSettings.findUnique({ where: { id: 'master_config' } });
  return NextResponse.json(settings || { siteName: "M.A.C.DevOS", contactEmail: "macdevos53@gmail.com", socialLinks: [] });
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const settings = await db.systemSettings.upsert({
      where: { id: 'master_config' },
      update: data,
      create: { id: 'master_config', ...data }
    });
    return NextResponse.json(settings);
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Internal Error' }, { status: 500 });
  }
}
"""
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(api_content)

    print_status("Backend logic updated.")

if __name__ == "__main__":
    deploy_social_matrix()
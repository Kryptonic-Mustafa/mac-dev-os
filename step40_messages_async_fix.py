import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚀 M.A.C.DevOS API Patch] {message}...")
    time.sleep(0.5)

def deploy_message_fix():
    print_status("Awaiting Params: Fixing Messages API for Next.js 16")
    api_path = PROJECT_PATH / "src/app/api/admin/messages/[id]/route.ts"
    
    if api_path.exists():
        api_content = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PUT(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const body = await req.json();
    
    await db.message.update({
      where: { id: id },
      data: { isRead: body.isRead }
    });
    
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.message.delete({ where: { id: id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}
"""
        with open(api_path, "w", encoding="utf-8") as f:
            f.write(api_content)
        print_status("Message API Async compliance achieved.")
    else:
        print_status(f"Error: Could not find {api_path}")

if __name__ == "__main__":
    deploy_message_fix()
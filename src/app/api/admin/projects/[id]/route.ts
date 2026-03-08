import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    // UNWRAP PARAMS FIRST
    const { id } = await params;
    const data = await req.json();

    const project = await db.project.update({
      where: { id: id },
      data: data
    });
    return NextResponse.json(project);
  } catch (error) {
    console.error("Patch Error:", error);
    return NextResponse.json({ error: 'Update Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.project.delete({ where: { id: id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Deletion Failed' }, { status: 500 });
  }
}

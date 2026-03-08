import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const data = await req.json();
    const review = await db.review.update({
      where: { id },
      data: { ...data, priority: parseInt(data.priority) || 0 }
    });
    return NextResponse.json(review);
  } catch (error) {
    return NextResponse.json({ error: 'Update Failed' }, { status: 500 });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.review.delete({ where: { id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Deletion Failed' }, { status: 500 });
  }
}

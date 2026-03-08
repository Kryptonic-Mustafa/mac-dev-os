import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export const dynamic = 'force-dynamic'; // BREAKS THE CACHE

export async function GET() {
  const reviews = await db.review.findMany({ 
    orderBy: [ { priority: 'desc' }, { createdAt: 'desc' } ] 
  });
  return NextResponse.json(reviews);
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const logId = `LOG-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
    const review = await db.review.create({
      data: { ...data, logId, priority: parseInt(data.priority) || 0 }
    });
    return NextResponse.json(review);
  } catch (error) {
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}

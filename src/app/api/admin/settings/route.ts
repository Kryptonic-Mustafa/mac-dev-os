import { NextResponse } from 'next/server';
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

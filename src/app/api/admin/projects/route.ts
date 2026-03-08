import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  const projects = await db.project.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(projects);
}

export async function POST(req: Request) {
  try {
    const data = await req.json();
    const systemId = `SYS-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
    const project = await db.project.create({
      data: { systemId, title: data.title, description: data.description, tech: data.tech, repoLink: data.repoLink, liveLink: data.liveLink }
    });
    return NextResponse.json(project);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create project' }, { status: 500 });
  }
}

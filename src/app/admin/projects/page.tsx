import { db } from '@/lib/db';
import ProjectsUI from './ProjectsUI';

export const dynamic = 'force-dynamic';

export default async function ProjectsPage() {
  const projects = await db.project.findMany({ orderBy: { createdAt: 'desc' } });
  return <ProjectsUI initialProjects={projects} />;
}

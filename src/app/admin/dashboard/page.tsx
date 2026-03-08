import { db } from '@/lib/db';
import DashboardUI from './DashboardUI';

// Force dynamic rendering so stats are always fresh
export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  // Fetch live telemetry from MySQL
  const projectCount = await db.project.count();
  const messageCount = await db.message.count();
  const unreadMessages = await db.message.count({ where: { isRead: false } });

  const stats = {
    projects: projectCount,
    messages: messageCount,
    unread: unreadMessages,
  };

  return <DashboardUI stats={stats} />;
}

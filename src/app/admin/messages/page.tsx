import { db } from '@/lib/db';
import MessagesUI from './MessagesUI';

export const dynamic = 'force-dynamic';

export default async function MessagesPage() {
  const messages = await db.message.findMany({ orderBy: { createdAt: 'desc' } });
  return <MessagesUI initialMessages={messages} />;
}

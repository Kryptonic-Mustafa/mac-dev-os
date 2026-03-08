// @ts-nocheck
import { db } from '@/lib/db';
import SettingsUI from './SettingsUI';

export const dynamic = 'force-dynamic';

export default async function SettingsPage() {
  let settings = await db.systemSettings.findUnique({ where: { id: 'master_config' } });
  
  if (!settings) {
    settings = {
      id: 'master_config',
      siteName: 'M.A.C.DevOS',
      logoUrl: '',
      faviconUrl: '',
      githubUrl: '',
      linkedinUrl: '',
      twitterUrl: '',
      updatedAt: new Date()
    };
  }
  
  return <SettingsUI initialSettings={settings} />;
}

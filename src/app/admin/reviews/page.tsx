import { db } from '@/lib/db';
import ReviewsUI from './ReviewsUI';

export const dynamic = 'force-dynamic';

export default async function ReviewsPage() {
  const reviews = await db.review.findMany({ orderBy: { createdAt: 'desc' } });
  return <ReviewsUI initialReviews={reviews} />;
}

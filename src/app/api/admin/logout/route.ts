import { NextResponse } from 'next/server';

export async function POST() {
  const response = NextResponse.json({ message: 'Comm channel closed.' }, { status: 200 });
  response.cookies.delete('macdevos_token');
  return response;
}

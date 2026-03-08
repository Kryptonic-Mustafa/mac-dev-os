import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';
import { SignJWT } from 'jose';

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();

    if (!email || !password) {
      return NextResponse.json({ error: 'Invalid parameters.' }, { status: 400 });
    }

    const admin = await db.admin.findUnique({ where: { email } });
    
    if (!admin) {
      return NextResponse.json({ error: 'Unauthorized access.' }, { status: 401 });
    }

    const isValid = await bcrypt.compare(password, admin.password);
    
    if (!isValid) {
      return NextResponse.json({ error: 'Unauthorized access.' }, { status: 401 });
    }

    // Generate JWT Token
    const secret = new TextEncoder().encode(process.env.JWT_SECRET);
    const alg = 'HS256';
    
    const token = await new SignJWT({ id: admin.id, email: admin.email })
      .setProtectedHeader({ alg })
      .setIssuedAt()
      .setExpirationTime('24h')
      .sign(secret);

    // Set HTTP-Only Cookie
    const response = NextResponse.json({ message: 'Access granted.' }, { status: 200 });
    response.cookies.set({
      name: 'macdevos_token',
      value: token,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 60 * 60 * 24, // 1 day
      path: '/',
    });

    return response;

  } catch (error) {
    console.error('Login Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

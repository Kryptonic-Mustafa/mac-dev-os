import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export async function GET() {
  try {
    // Check if an admin already exists to prevent public exploits
    const existingAdmin = await db.admin.findFirst();
    if (existingAdmin) {
      return NextResponse.json({ error: 'SYSTEM LOCKED: Admin already exists.' }, { status: 403 });
    }

    // Create the master admin account
    const hashedPassword = await bcrypt.hash('admin123', 10);
    
    await db.admin.create({
      data: {
        email: 'admin@macdevos.com',
        password: hashedPassword,
      }
    });

    return NextResponse.json({ 
      message: 'Admin account created successfully.',
      email: 'admin@macdevos.com',
      password: 'admin123'
    }, { status: 201 });

  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Failed to initialize system.' }, { status: 500 });
  }
}

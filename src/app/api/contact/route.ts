import { NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(request: Request) {
  try {
    const { name, email, payload } = await request.json();

    if (!name || !email || !payload) {
      return NextResponse.json({ error: 'Missing required parameters.' }, { status: 400 });
    }

    // Configure the Transporter using Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
      },
    });

    // Construct the secure email payload
    const mailOptions = {
      from: process.env.GMAIL_USER, // Sent from your authenticated server account
      to: process.env.GMAIL_USER,   // Sent TO yourself
      replyTo: email,               // If you hit "Reply", it goes to the client
      subject: `[M.A.C.DevOS] Comm Link from ${name}`,
      text: `SYSTEM COMM LINK INITIATED\n\nID: ${name}\nCOMM: ${email}\n\nPAYLOAD:\n${payload}`,
      html: `
        <div style="font-family: monospace; background-color: #050505; color: #00F0FF; padding: 20px;">
          <h2 style="border-bottom: 1px solid #00F0FF; padding-bottom: 10px;">[M.A.C.DevOS] SECURE TRANSMISSION</h2>
          <p><strong>ID (Identity):</strong> ${name}</p>
          <p><strong>COMM (Email):</strong> ${email}</p>
          <br/>
          <p><strong>PAYLOAD (Message):</strong></p>
          <div style="background-color: #0a0a0a; padding: 15px; border: 1px solid #333; color: #E0E0E0; white-space: pre-wrap;">${payload}</div>
        </div>
      `,
    };

    await transporter.sendMail(mailOptions);

    return NextResponse.json({ message: 'Transmission successful.' }, { status: 200 });
  } catch (error) {
    console.error('Transmission Error:', error);
    return NextResponse.json({ error: 'Failed to transmit data.' }, { status: 500 });
  }
}

import type { Metadata } from 'next';
import React from 'react';
import './globals.css';

export const metadata: Metadata = {
  title: 'AGENTX — AI Resume Intelligence & Autonomous Career Platform',
  description: 'Next-generation AI resume scoring, ATS analysis, job matching & career intelligence',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-[#060812] text-slate-100 min-h-screen font-['Plus_Jakarta_Sans',sans-serif] antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}

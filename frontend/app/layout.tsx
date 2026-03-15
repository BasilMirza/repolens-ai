import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'RepoLens AI',
  description: 'AI-inspired GitHub repository analyzer',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

'use client'

import "./globals.css"
import { AuthProvider, useAuth } from "@/app/context/AuthContext"
import Link from "next/link"

// Component hat nicht funktioniert
function DirectNavigation() {
  const { user, isAdmin, isOrganizer, loading } = useAuth()
  if (loading) return <div className="h-16 bg-gray-900" />

  return (
    <nav className="flex items-center justify-between p-4 bg-gray-900 text-white">
      <div className="flex gap-6">
        <Link href="/dashboard" className="font-bold text-xl">EventApp</Link>
        <Link href="/dashboard/visitor" className="hover:text-blue-400">Events</Link>
        

        {isAdmin && (
          <Link href="/dashboard/admin" className="text-red-400">Admin</Link>
        )}
      </div>

      <div className="flex items-center gap-4">
        {user && <span className="text-xs">{user.username} ({user.role})</span>}
        <button className="bg-red-600 px-3 py-1 rounded text-sm" onClick={() => {
          localStorage.removeItem('token')
          window.location.href = '/frontend/login'
        }}>Logout</button>
      </div>
    </nav>
  )
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body>
        <AuthProvider>
          <DirectNavigation />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  )
}
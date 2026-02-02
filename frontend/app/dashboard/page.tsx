'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/context/AuthContext'

export default function DashboardPage() {
  const { user, loading, isAdmin, isOrganizer } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading) {
      if (!user) router.push('/frontend/login')
      else if (isAdmin) router.push('/dashboard/admin')
      else if (isOrganizer) router.push('/dashboard/tickets')
      else router.push('/dashboard/visitor')
    }
  }, [user, loading, isAdmin, isOrganizer, router])

  return <div className="p-10 text-center">Wird geladen...</div>
}
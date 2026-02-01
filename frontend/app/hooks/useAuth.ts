import { useState, useEffect } from 'react'
import axios from 'axios'

export function useAuth() {
  const [user, setUser] = useState<{ id: number; username: string; role: string } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const { data } = await axios.post('http://localhost/api/login/me')
        setUser(data)
      } catch (error) {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    fetchUser()
  }, [])

  return { user, loading, isAdmin: user?.role === 'ADMIN', isOrganizer: user?.role === 'ORGANIZER' }
}
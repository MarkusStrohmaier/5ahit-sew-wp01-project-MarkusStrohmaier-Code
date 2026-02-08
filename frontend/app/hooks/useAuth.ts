import { useState, useEffect } from 'react'
import axios from 'axios'

export function useAuth() {
  const [user, setUser] = useState<{ id: number; username: string; role: string } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        setLoading(false)
        return
      }

      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

      try {
        const { data } = await axios.post('http://localhost/api/login/me')
        setUser(data)
      } catch (error) {
        delete axios.defaults.headers.common['Authorization']
        localStorage.removeItem('token')
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    fetchUser()
  }, [])

  return { user, loading, isAdmin: user?.role === 'ADMIN', isOrganizer: user?.role === 'ORGANIZER' }
}
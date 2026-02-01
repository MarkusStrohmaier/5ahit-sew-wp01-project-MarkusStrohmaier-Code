'use client'
import React, { createContext, useContext, useEffect, useState } from 'react'
import axios from 'axios'

const AuthContext = createContext<any>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          const { data } = await axios.post('http://localhost/api/login/me')
          setUser(data)
        }
      } catch (e) { setUser(null) }
      finally { setLoading(false) }
    }
    fetchUser()
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, isAdmin: user?.role === 'ADMIN', isOrganizer: user?.role === 'ORGANIZER' }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
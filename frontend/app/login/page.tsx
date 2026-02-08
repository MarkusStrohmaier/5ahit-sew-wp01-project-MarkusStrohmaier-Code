'use client'

import { useState } from 'react'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

const LOGIN_API_URL = 'http://localhost/api/login/login'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    try {
      const response = await axios.post(LOGIN_API_URL, formData, {
         headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
         }
      })

      const token = response.data.access_token
      localStorage.setItem('token', token)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

      console.log('Login erfolgreich.')
      
      router.push('/dashboard') 
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login fehlgeschlagen. Prüfe deine Daten.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm space-y-6 rounded-lg bg-white p-8 shadow-md"
      >
        <h2 className="text-2xl font-semibold text-center text-gray-800">Anmelden</h2>

        {error && (
          <div className="text-red-600 text-sm p-2 border border-red-300 bg-red-50 rounded">
            {error}
          </div>
        )}

        <div className="space-y-2">
          <Label htmlFor="username">Benutzername</Label>
          <Input
            id="username"
            type="text"
            placeholder="Dein Benutzername"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="password">Passwort</Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Anmeldung läuft...' : 'Login'}
        </Button>

        <div className="text-center text-sm text-gray-600 mt-4">
          Noch kein Konto?{' '}
          <Link href="/register" className="text-blue-600 hover:underline font-medium">
            Jetzt registrieren
          </Link>
        </div>
      </form>
    </div>
  )
}
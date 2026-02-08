'use client'

import { useState } from 'react'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

const REGISTER_API_URL = 'http://localhost/api/users/users/register' 

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('VISITOR') //Default
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      await axios.post(REGISTER_API_URL, {
        username,
        email,
        password,
        role
      })

      router.push('/login')
    } catch (err: any) {
      const detail = err.response?.data?.detail
      setError(Array.isArray(detail) ? detail[0].msg : (detail || 'Registrierung fehlgeschlagen.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4 rounded-lg bg-white p-8 shadow-md">
        <h2 className="text-2xl font-semibold text-center text-gray-800">Account erstellen</h2>

        {error && (
          <div className="text-red-600 text-sm p-2 border border-red-300 bg-red-50 rounded">{error}</div>
        )}

        <div className="space-y-1">
          <Label htmlFor="username">Benutzername</Label>
          <Input id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>

        <div className="space-y-1">
          <Label htmlFor="email">E-Mail</Label>
          <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>

        <div className="space-y-1">
          <Label htmlFor="role">Rolle</Label>
          <select
            id="role"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 text-gray-900"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="VISITOR">Besucher (Visitor)</option>
            <option value="ORGANIZER">Veranstalter (Organizer)</option>
            <option value="ADMIN">Administrator</option>
          </select>
        </div>

        <div className="space-y-1">
          <Label htmlFor="password">Passwort</Label>
          <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>

        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Wird registriert...' : 'Registrieren'}
        </Button>

        <p className="text-center text-sm">
          <Link href="/login" className="text-blue-600 hover:underline font-medium">Zurück zum Login</Link>
        </p>
      </form>
    </div>
  )
}
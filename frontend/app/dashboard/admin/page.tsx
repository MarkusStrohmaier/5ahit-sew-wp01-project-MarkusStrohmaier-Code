'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '@/app/context/AuthContext'
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table'
import { Input } from '@/components/ui/input'

interface User {
  id: number
  username: string
  role: string
}

export default function AdminPage() {
  const { isAdmin, loading: authLoading } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [search, setSearch] = useState('')

  useEffect(() => { // Admin prüfung
    const fetchUsers = async () => {
      try {
        const { data } = await axios.get('http://localhost/api/users/users/')
        setUsers(data)
      } catch (e) {
        console.error("Fehler beim Laden der Benutzerliste")
      }
    }
    
    if (isAdmin) fetchUsers()
  }, [isAdmin])

  // Ladezustand 
  if (authLoading) return <p className="p-10 text-gray-500">Prüfe Berechtigungen...</p>
  if (!isAdmin) return <p className="p-10 text-red-500 font-bold">Zugriff verweigert: Du benötigst Admin-Rechte.</p>

  const filteredUsers = users.filter(user => 
    user.username.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Admin-Benutzerverwaltung</h1>
      
      <div className="flex items-center space-x-4">
        <Input 
          placeholder="Nach Benutzernamen suchen..." 
          className="max-w-sm"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="rounded-md border bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">ID</TableHead>
              <TableHead>Benutzername</TableHead>
              <TableHead>Rolle</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell className="font-mono text-gray-500">{user.id}</TableCell>
                <TableCell className="font-medium">{user.username}</TableCell>
                <TableCell>
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    user.role === 'ADMIN' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {user.role}
                  </span>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {filteredUsers.length === 0 && (
          <div className="p-10 text-center text-gray-400">Keine Benutzer gefunden.</div>
        )}
      </div>
    </div>
  )
}
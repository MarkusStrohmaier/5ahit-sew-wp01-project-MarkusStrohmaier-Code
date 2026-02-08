'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '@/app/context/AuthContext'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Button } from '@/components/ui/button'

export default function AdminPage() {
  const { isAdmin, loading: authLoading } = useAuth()
  const [users, setUsers] = useState([])

  const fetchUsers = async () => {
    try {
      const { data } = await axios.get('http://localhost/api/users/users/')
      setUsers(data)
    } catch (e) { console.error(e) }
  }

  useEffect(() => {
    if (isAdmin) fetchUsers()
  }, [isAdmin])

  const handleDelete = async (id: number) => {
    if (confirm(`User ${id} wirklich löschen?`)) {
      try {
        await axios.delete(`http://localhost/api/users/${id}`)
        fetchUsers()
      } catch (e) {
        alert("Fehler beim Löschen.")
      }
    }
  }

  if (authLoading) return <p className="p-8">Lade...</p>
  if (!isAdmin) return <p className="p-8 text-red-500">Zugriff verweigert.</p>

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Benutzerliste</h1>
      <div className="border rounded-lg bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Username</TableHead>
              <TableHead>Rolle</TableHead>
              <TableHead className="text-right w-[50px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((u: any) => (
              <TableRow key={u.id} className="hover:bg-gray-50">
                <TableCell>#{u.id}</TableCell>
                <TableCell className="font-medium">{u.username}</TableCell>
                <TableCell>{u.role}</TableCell>
                <TableCell className="text-right">
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
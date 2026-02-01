'use client'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export default function TicketsPage() {
  const [tickets, setTickets] = useState([])

  useEffect(() => {
    axios.get('http://localhost/api/tickets/')
      .then(res => setTickets(res.data))
      .catch(err => console.error("Ticket-Fehler:", err))
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Ticket-Verwaltung</h1>
      <div className="border rounded-lg bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Event-ID</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tickets.map((t: any) => (
              <TableRow key={t.id}>
                <TableCell>#{t.id}</TableCell>
                <TableCell>{t.status}</TableCell>
                <TableCell>Event {t.event_id}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
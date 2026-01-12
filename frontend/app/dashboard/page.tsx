'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

// Events
interface Event {
  id: number
  title: string
  date: string
  time: string
  description: string
  ticket_capacity: number
  location_id: number
}

export default function DashboardPage() {
  const [search, setSearch] = useState('')
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)

  // Filter
  const filteredData = events.filter((item) =>
    item.title.toLowerCase().includes(search.toLowerCase()) ||
    item.description.toLowerCase().includes(search.toLowerCase())
  )

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const { data } = await axios.get<Event[]>('http://localhost/api/events/')
        setEvents(data)
      } catch (error) {
        console.error('Error fetching events:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchEvents()
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading Events...</p>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Event Dashboard</h1>

      <Input
        placeholder="Search by title or description..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="max-w-md"
      />

      <div className="overflow-hidden rounded-lg border border-gray-200 shadow-sm">
        <Table>
          <TableHeader className="bg-gray-100">
            <TableRow>
              <TableHead className="text-gray-700 w-[50px]">ID</TableHead>
              <TableHead className="text-gray-700">Title</TableHead>
              <TableHead className="text-gray-700 w-[120px]">Date</TableHead>
              <TableHead className="text-gray-700 w-[80px]">Time</TableHead>
              <TableHead className="text-gray-700 w-[100px]">Capacity</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredData.map((event, index) => (
              <TableRow
                key={event.id}
                className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
              >
                <TableCell>{event.id}</TableCell>
                <TableCell className="font-medium">{event.title}</TableCell>
                <TableCell>{event.date}</TableCell>
                <TableCell>{event.time}</TableCell>
                <TableCell>{event.ticket_capacity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        {filteredData.length === 0 && (
          <div className="p-4 text-center text-gray-500">
            No events found matching your search.
          </div>
        )}
      </div>
    </div>
  )
}
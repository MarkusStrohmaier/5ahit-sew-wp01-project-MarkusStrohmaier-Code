'use client'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function VisitorPage() {
  const [events, setEvents] = useState([])

  useEffect(() => {
    axios.get('http://localhost/api/events/').then(res => setEvents(res.data))
  }, [])

  const handleBook = (id: number) => {
    axios.post('http://localhost/api/bookings/', { event_id: id })
      .then(() => alert("Ticket gebucht!"))
      .catch(() => alert("Fehler beim Buchen."))
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Events entdecken</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {events.map((e: any) => (
          <Card key={e.id}>
            <CardHeader><CardTitle>{e.title}</CardTitle></CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500 mb-4">{e.description}</p>
              <Button onClick={() => handleBook(e.id)} className="w-full">Jetzt buchen</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
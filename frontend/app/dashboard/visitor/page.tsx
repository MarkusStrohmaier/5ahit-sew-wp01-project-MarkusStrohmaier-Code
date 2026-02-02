'use client'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '@/app/context/AuthContext'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function VisitorPage() {
  const { isAdmin, isOrganizer } = useAuth()
  const [events, setEvents] = useState([])

  const fetchEvents = async () => {
    const { data } = await axios.get('http://localhost/api/events/')
    setEvents(data)
  }

  useEffect(() => { fetchEvents() }, [])

  const handleBooking = async (eventId: number) => {
    try {
      await axios.post('http://localhost/api/bookings/', { event_id: eventId })
      alert("Gebucht!")
    } catch (e) { alert("Fehler beim Buchen.") }
  }

  const handleDeleteEvent = async (id: number) => {
    if (confirm("Event wirklich löschen?")) {
      try {
        await axios.delete(`http://localhost/api/events/${id}`)
        fetchEvents()
      } catch (e) { alert("Fehler beim Löschen.") }
    }
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Events</h1>
        {(isAdmin || isOrganizer) && (
             <Button size="sm" onClick="">+ Neu</Button>
        )}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {events.map((e: any) => (
          <Card key={e.id} className="relative">
            <CardHeader className="flex flex-row justify-between items-start pr-10">
              <CardTitle className="text-xl">{e.title}</CardTitle>
              
              {(isAdmin || isOrganizer) && (
                <Button 
                    variant="destructive" 
                    size="sm" 
                    className="absolute top-4 right-4 h-8 w-8 p-0 font-bold" 
                    onClick={() => handleDeleteEvent(e.id)}
                    title="Event löschen"
                  >
                    X
                </Button>
              )}
            </CardHeader>
            <CardContent>
              <p className="text-gray-500 mb-4 line-clamp-3">{e.description}</p>
              <Button className="w-full" onClick={() => handleBooking(e.id)}>Buchen</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label' // Label wird für das Dialog-Formular benötigt
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'


import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

import { Button } from '@/components/ui/button'


// Neue Schnittstelle für Events, basierend auf der Annahme Ihres Backend-Modells
interface Event {
  id: number
  title: string
  date: string // Datum als String
  time: string // Zeit als String
  description: string
  ticket_capacity: number
  location_id: number
}

export default function DashboardPage() {
  const [search, setSearch] = useState('')
  // Zustand von 'users' auf 'events' umbenannt
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)

  // Zustand von 'selectedUser' auf 'selectedEvent' umbenannt
  const [selectedEvent, setSelectedEvent] = useState<Event>();
  const [open, setOpen] = useState(false);

  // Funktion zum Öffnen des Dialogs für ein Event
  const openDialog = (event: Event) => {
    setSelectedEvent({ ...event });
    setOpen(true);
  };

  // Funktion zum Speichern der Änderungen (noch lokal im Frontend)
  const handleSave = () => {
    if (!selectedEvent) return;
    
    // Annahme: PUT-Anfrage an die API zum Speichern der Änderungen
    // Hier nur die lokale Zustandsaktualisierung
    setEvents((prev) =>
      prev.map((e) => (e.id === selectedEvent.id ? selectedEvent : e))
    );
    setOpen(false);
  };


  // Filterlogik auf Event-Titel und Beschreibung umgestellt
  const filteredData = events.filter((item) =>
    item.title.toLowerCase().includes(search.toLowerCase()) ||
    item.description.toLowerCase().includes(search.toLowerCase())
  )


  useEffect(() => {
    const fetchEvents = async () => {
      try {
        // Endpunkt auf Events umgestellt
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
              <p>Loading Events...</p>
          </div>
      );
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Event Dashboard</h1>

      <Input
        // Platzhalter für die Event-Suche angepasst
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
            {/* Iteriere über die gefilterten Event-Daten */}
            {filteredData.map((event, index) => (
              <TableRow
                key={event.id}
                className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50 cursor-pointer'}
                onClick={() => openDialog(event)}
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
          <div className="p-4 text-center text-gray-500">No events found.</div>
        )}
      </div>
      
      {/* Dialog zur Bearbeitung von Events */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Event: {selectedEvent?.title}</DialogTitle>
          </DialogHeader>
          
          {selectedEvent && (
            <div className="space-y-4 mt-4">
              
              {/* Titel bearbeiten */}
              <div className="space-y-1">
                <Label htmlFor="title">Title</Label>
                <Input
                  id="title"
                  value={selectedEvent.title}
                  onChange={(e) =>
                    setSelectedEvent({ ...selectedEvent, title: e.target.value })
                  }
                  placeholder="Event Title"
                />
              </div>

              {/* Datum bearbeiten */}
              <div className="space-y-1">
                <Label htmlFor="date">Date</Label>
                <Input
                  id="date"
                  type="date"
                  value={selectedEvent.date}
                  onChange={(e) =>
                    setSelectedEvent({ ...selectedEvent, date: e.target.value })
                  }
                />
              </div>

              {/* Beschreibung bearbeiten (Optional: könnte auch ein Textarea sein) */}
              <div className="space-y-1">
                <Label htmlFor="description">Description</Label>
                <Input
                  id="description"
                  value={selectedEvent.description}
                  onChange={(e) =>
                    setSelectedEvent({ ...selectedEvent, description: e.target.value })
                  }
                  placeholder="Description"
                />
              </div>

            </div>
          )}

          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSave}>Save Changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
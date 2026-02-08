'use client'
import { useEffect, useState, useCallback } from 'react'
import axios from 'axios'
import { useAuth } from '@/app/context/AuthContext'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { AlertCircle, CheckCircle2 } from "lucide-react" // Icon

export default function Dashboard() {
  const { isAdmin, isOrganizer } = useAuth()
  const [events, setEvents] = useState([])
  const [myTickets, setMyTickets] = useState([])
  const [locations, setLocations] = useState([])
  const [openEvent, setOpenEvent] = useState(false)
  const [openLocation, setOpenLocation] = useState(false)
  const [loading, setLoading] = useState(false)

  const [status, setStatus] = useState<{ msg: string; type: 'success' | 'error' | null }>({ msg: '', type: null })
  const [formError, setFormError] = useState<string | null>(null)

  const showStatus = (msg: string, type: 'success' | 'error') => {
    setStatus({ msg, type })
    setTimeout(() => setStatus({ msg: '', type: null }), 5000)
  }

  const fetchData = useCallback(async () => {
    const token = localStorage.getItem('token')
    try {
      const [evRes, locRes] = await Promise.all([
        axios.get('http://localhost/api/events/'),
        axios.get('http://localhost/api/locations/')
      ])
      setEvents(evRes.data)
      setLocations(locRes.data)

      if (token) {
        const tickRes = await axios.get('http://localhost/api/tickets/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setMyTickets(tickRes.data)
      }
    } catch (e) {
      console.error("Ladefehler:", e)
    }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const handleBooking = async (eventId: number) => {
    const token = localStorage.getItem('token')
    if (!token) return showStatus("Bitte logge dich zuerst ein.", "error")

    try {
      setLoading(true)
      await axios.post('http://localhost/api/bookings/', { event_id: eventId }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      showStatus("Buchung erfolgreich abgeschlossen!", "success")
      fetchData()
    } catch (e) {
      showStatus("Buchung fehlgeschlagen. Event Ausgebucht!", "error")
    } finally {
      setLoading(false)
    }
  }

  const handleCreateLocation = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    const token = localStorage.getItem('token')
    try {
      await axios.post('http://localhost/api/locations/', locationData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setOpenLocation(false)
      setLocationData({ name: '', address: '', capacity: 1 })
      fetchData()
      showStatus("Location wurde erfolgreich angelegt.", "success")
    } catch (e) {
      setFormError("Fehler: Location konnte nicht erstellt werden.")
    }
  }

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    const token = localStorage.getItem('token')
    try {
      const payload = {
        ...eventData,
        location_id: parseInt(eventData.location_id),
        ticket_capacity: parseInt(eventData.ticket_capacity.toString()),
        date: new Date(eventData.date).toISOString()
      }
      await axios.post('http://localhost/api/events/', payload, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setOpenEvent(false)
      setEventData({ title: '', date: '', time: '18:00', description: '', ticket_capacity: 1, location_id: '' })
      fetchData()
      showStatus("Event wurde erfolgreich erstellt!", "success")
    } catch (e) {
      setFormError("Fehler beim Erstellen des Events. Prüfe bitte alle Felder.")
    }
  }

  const [eventData, setEventData] = useState({ title: '', date: '', time: '18:00', description: '', ticket_capacity: 1, location_id: '' })
  const [locationData, setLocationData] = useState({ name: '', address: '', capacity: 1 })

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-12 relative">

      {status.type && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center gap-3 border transition-all animate-in fade-in slide-in-from-top-4 
          ${status.type === 'success' ? 'bg-green-50 border-green-200 text-green-800' : 'bg-red-50 border-red-200 text-red-800'}`}>
          {status.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
          <p className="text-sm font-medium">{status.msg}</p>
        </div>
      )}

      {/* TICKET LISTE */}
      <section>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">Meine Tickets</h2>
        <div className="border rounded-md divide-y bg-white shadow-sm">
          {myTickets.length > 0 ? myTickets.map((t: any) => (
            <div key={t.id} className="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
              <div>
                <p className="font-semibold text-sm">{t.event?.title || `Event #${t.event_id}`}</p>
                <p className="text-xs text-gray-400 font-mono uppercase">ID: {t.id}</p>
              </div>
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-700 uppercase">{t.status}</span>
            </div>
          )) : (
            <p className="p-4 text-sm text-gray-400 italic">Noch keine Tickets gebucht.</p>
          )}
        </div>
      </section>

      {/* EVENT LISTE */}
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold italic decoration-blue-500">Verfügbare Events</h2>
          <div className="flex gap-2">
            {(isAdmin || isOrganizer) && (
              <>
                {/* LOCATION */}
                <Dialog open={openLocation} onOpenChange={(val) => { setOpenLocation(val); setFormError(null); }}>
                  <DialogTrigger asChild><Button variant="outline" size="sm">Location +</Button></DialogTrigger>
                  <DialogContent>
                    <DialogHeader><DialogTitle>Neue Location</DialogTitle></DialogHeader>
                    <form onSubmit={handleCreateLocation} className="space-y-4 pt-2">
                      <Input placeholder="Name" required onChange={e => setLocationData({ ...locationData, name: e.target.value })} />
                      <Input placeholder="Adresse" required onChange={e => setLocationData({ ...locationData, address: e.target.value })} />
                      <Input type="number" min="1" placeholder="Max. Kapazität" required onChange={e => setLocationData({ ...locationData, capacity: parseInt(e.target.value) })} />
                      {formError && <p className="text-sm text-red-600 bg-red-50 p-2 rounded">{formError}</p>}
                      <Button type="submit" className="w-full">Speichern</Button>
                    </form>
                  </DialogContent>
                </Dialog>

                {/* EVENT DIALOG */}
                <Dialog open={openEvent} onOpenChange={(val) => { setOpenEvent(val); setFormError(null); }}>
                  <DialogTrigger asChild><Button size="sm">+ Event hinzufügen</Button></DialogTrigger>
                  <DialogContent className="max-w-md">
                    <DialogHeader><DialogTitle>Neues Event erstellen</DialogTitle></DialogHeader>
                    <form onSubmit={handleCreateEvent} className="space-y-4 pt-4">
                      <div>
                        <Label>Titel</Label>
                        <Input required value={eventData.title} onChange={e => setEventData({ ...eventData, title: e.target.value })} />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label>Datum</Label>
                          <Input type="date" required value={eventData.date} onChange={e => setEventData({ ...eventData, date: e.target.value })} />
                        </div>
                        <div>
                          <Label>Uhrzeit</Label>
                          <Input type="time" required value={eventData.time} onChange={e => setEventData({ ...eventData, time: e.target.value })} />
                        </div>
                      </div>
                      <div>
                        <Label>Beschreibung</Label>
                        <Input value={eventData.description} onChange={e => setEventData({ ...eventData, description: e.target.value })} />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label>Ticket-Anzahl</Label>
                          <Input type="number" min="1" required value={eventData.ticket_capacity} onChange={e => setEventData({ ...eventData, ticket_capacity: parseInt(e.target.value) })} />
                        </div>
                        <div>
                          <Label>Location</Label>
                          <select className="w-full border p-2 rounded text-sm h-10 bg-white" required value={eventData.location_id} onChange={e => setEventData({ ...eventData, location_id: e.target.value })}>
                            <option value="">Wählen...</option>
                            {locations.map((loc: any) => (<option key={loc.id} value={loc.id}>{loc.name}</option>))}
                          </select>
                        </div>
                      </div>
                      {formError && <p className="text-sm text-red-600 bg-red-50 p-2 rounded">{formError}</p>}
                      <Button type="submit" className="w-full">Event speichern</Button>
                    </form>
                  </DialogContent>
                </Dialog>
              </>
            )}
          </div>
        </div>

        {/* EVENT TABELLE */}
        <div className="border rounded-md bg-white shadow-sm overflow-hidden">
          <Table>
            <TableHeader className="bg-gray-50">
              <TableRow>
                <TableHead>Event</TableHead>
                <TableHead>Datum</TableHead>
                <TableHead className="text-right">Aktion</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {events.length > 0 ? events.map((e: any) => (
                <TableRow key={e.id}>
                  <TableCell className="font-medium">
                    <div>
                      {e.title}
                      {e.description && <p className="text-xs text-gray-400 font-normal truncate max-w-[200px]">{e.description}</p>}
                    </div>
                  </TableCell>
                  <TableCell className="text-sm">
                    {new Date(e.date).toLocaleDateString('de-DE')} {e.time && `@ ${e.time}`}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="outline" onClick={() => handleBooking(e.id)} disabled={loading}>
                      {loading ? "..." : "Buchen"}
                    </Button>
                  </TableCell>
                </TableRow>
              )) : (
                <TableRow><TableCell colSpan={3} className="text-center py-6 text-gray-400">Keine Events verfügbar.</TableCell></TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </section>
    </div>
  )
}
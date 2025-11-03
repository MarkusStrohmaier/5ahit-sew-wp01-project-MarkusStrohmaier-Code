# Klassendiagramm

@startuml
!theme plain
skinparam classAttributeIconSize 0
skinparam classFontStyle bold

' ==== Enums ====
enum UserRole {
  ADMIN
  ORGANIZER
  VISITOR
}

enum TicketStatus {
  AVAILABLE
  SOLD
  CANCELLED
}

' ==== Benutzerverwaltung ====
class User {
  - id: int
  - name: string
  - email: string
  - password_hash: string
  - phone_number: string
  - role: UserRole

  + list_all()
  + find_by_id(id: int)
  + find_by_email(email: string)
  + find_by_role(role: UserRole)
  + create(user_data)
  + update(id: int, user_data)
  + delete(id: int)
}

' ==== Eventverwaltung ====
class Location {
  - id: int
  - name: string
  - address: string
  - capacity: int

  + list_all()
  + find_by_id(id: int)
  + create(location_data)
  + update(id: int, location_data)
  + delete(id: int)
}

class Event {
  - id: int
  - title: string
  - date: date
  - time: string
  - description: string
  - ticket_capacity: int

  + list_all()
  + find_by_id(id: int)
  + find_by_location(location_id: int)
  + find_by_organizer(user_id: int)
  + list_available()
  + create(event_data)
  + update(id: int, event_data)
  + delete(id: int)
  + count_available_tickets()
}

' ==== Ticketverwaltung ====
class Ticket {
  - id: int
  - seat_num: string
  - price: decimal
  - status: TicketStatus

  + list_all()
  + find_by_id(id: int)
  + find_by_event(event_id: int)
  + list_available_by_event(event_id: int)
  + create(ticket_data)
  + update(id: int, ticket_data)
  + delete(id: int)
}

class Booking {
  - booking_number: int
  - booking_date: date

  + list_all()
  + find_by_id(booking_number: int)
  + find_by_user(user_id: int)
  + find_by_ticket(ticket_id: int)
  + create(booking_data)
  + cancel(booking_number: int)
}

' ==== Beziehungen ====
User "1" --> "0..*" Event : erstellt >
User "1" --> "0..*" Booking : bucht >
Location "1" --> "0..*" Event : findet statt an >
Event "1" --> "0..*" Ticket : enthält >
Ticket "0..1" --> "0..1" Booking : ist gebucht in >

User --> UserRole
Ticket --> TicketStatus

@enduml


# ER-Diagramm

@startchen

' ==== Entities ====
entity USER {
  id <<key>>
  name
  email
  password_hash
  phone_number
  role
}

entity LOCATION {
  id <<key>>
  name
  address
  capacity
}

entity EVENT {
  id <<key>>
  title
  date
  time
  description
  location_id
  organizer_id
  ticket_capacity
}

entity TICKET {
  id <<key>>
  event_id
  seat_num
  price
  status
}

entity BOOKING {
  booking_number <<key>>
  user_id
  ticket_id
  date
}

' ==== Relationships ====
relationship ORGANIZES {
}
ORGANIZES -1- USER
ORGANIZES -N- EVENT

relationship MAKES_BOOKING {
}
MAKES_BOOKING -1- USER
MAKES_BOOKING -N- BOOKING

relationship HELD_AT {
}
HELD_AT -1- LOCATION
HELD_AT -N- EVENT

relationship HAS_TICKETS {
}
HAS_TICKETS -1- EVENT
HAS_TICKETS -N- TICKET

relationship BOOKS {
}
BOOKS -1- TICKET
BOOKS -M- BOOKING

@endchen

import React, { useState } from 'react'
import Calendar from './Calendar'

function App() {
  // Sample events
  const [events] = useState([
    {
      name: "Weekly Meeting",
      startTime: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(), // Tomorrow
      endTime: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString()
    },
    {
      name: "Project Deadline",
      startTime: new Date(new Date().setDate(new Date().getDate() + 3)).toISOString(), // 3 days from now
      endTime: new Date(new Date().setDate(new Date().getDate() + 3)).toISOString()
    },
    {
      name: "Long Event",
      startTime: new Date().toISOString(),
      endTime: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString() // Spans 2 days
    },
    {
      name: "Past Event",
      startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString(),
      endTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
    }
  ]);

  return (
    <div className="w-full">
      <header className="p-4 bg-gray-800 text-white shadow">
        <h1 className="text-2xl font-bold">Event Calendar</h1>
      </header>
      <main>
        <Calendar events={events} />
      </main>
    </div>
  )
}

export default App
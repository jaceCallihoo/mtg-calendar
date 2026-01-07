import React, { useState, useEffect } from 'react'
import Calendar from './Calendar'

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/events')
      .then(response => response.json())
      .then(data => setEvents(data))
      .catch(error => console.error('Error fetching events:', error));
  }, []);

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

import React, { useMemo } from 'react';

const DAYS_OF_WEEK = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

const EVENT_COLORS = [
  'bg-blue-600',
  'bg-indigo-600',
  'bg-violet-600',
  'bg-purple-600',
  'bg-pink-600',
  'bg-red-600',
  'bg-orange-600',
  'bg-amber-600',
  'bg-yellow-600',
  'bg-lime-600',
  'bg-green-600',
  'bg-emerald-600',
  'bg-teal-600',
  'bg-cyan-600',
  'bg-sky-600',
];

const Calendar = ({ events }) => {
  const { days, headers } = useMemo(() => {
    const today = new Date();
    // Calculate start date (previous Saturday)
    const dayOfWeek = today.getDay(); // 0=Sun, 6=Sat
    // We want 0=Sat, 1=Sun, ..., 6=Fri
    // Current mapping: Sun(0)->1, Mon(1)->2, ..., Sat(6)->0
    // Offset to subtract from today:
    // Sat(6): 0
    // Sun(0): 1
    // Mon(1): 2
    // ...
    // Fri(5): 6
    // Formula: (dayOfWeek + 1) % 7
    const offset = (dayOfWeek + 1) % 7;
    
    const startDate = new Date(today);
    startDate.setDate(today.getDate() - offset);
    startDate.setHours(0, 0, 0, 0);

    const daysList = [];
    const daysInWeek = 7;
    const numWeeks = 10;
    for (let i = 0; i < numWeeks * daysInWeek; i++) {
      const current = new Date(startDate);
      current.setDate(startDate.getDate() + i);
      daysList.push(current);
    }

    return { days: daysList, headers: DAYS_OF_WEEK };
  }, []);

  const getEventsForDay = (date) => {
    return events.filter(event => {
      const eventStart = new Date(event.startTime);
      const eventEnd = new Date(event.endTime);
      
      // Check if the event overlaps with the day (00:00 to 23:59)
      const dayStart = new Date(date);
      dayStart.setHours(0, 0, 0, 0);
      
      const dayEnd = new Date(date);
      dayEnd.setHours(23, 59, 59, 999);

      return eventStart <= dayEnd && eventEnd >= dayStart;
    });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className="p-4 bg-gray-900 min-h-screen text-white">
      <div className="grid grid-cols-7 gap-2 mb-2">
        {headers.map(day => (
          <div key={day} className="text-center font-bold text-gray-400 py-2 border-b border-gray-700">
            {day}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-2">
        {days.map((day, index) => {
            const dayEvents = getEventsForDay(day);
            const isToday = new Date().toDateString() === day.toDateString();
            
            return (
              <div 
                key={index} 
                className={`min-h-[120px] p-2 border border-gray-700 rounded bg-gray-800 ${isToday ? 'ring-2 ring-blue-500' : ''}`}
              >
                <div className={`text-sm mb-2 ${isToday ? 'text-blue-400 font-bold' : 'text-gray-400'}`}>
                  {formatDate(day)}
                </div>
                <div className="space-y-1">
                  {dayEvents.map((event, idx) => {
                    const colorClass = EVENT_COLORS[events.indexOf(event) % EVENT_COLORS.length];
                    return (
                      <div 
                        key={idx} 
                        className={`${colorClass} text-[10px] sm:text-xs p-1 rounded text-white truncate font-bold shadow-sm border border-white/10`} 
                        title={`${event.name} (${new Date(event.startTime).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})})`}
                      >
                        <div className="bg-black/20 w-full px-1 py-0.5 rounded-sm truncate">
                          {event.name}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
        })}
      </div>
    </div>
  );
};

export default Calendar;

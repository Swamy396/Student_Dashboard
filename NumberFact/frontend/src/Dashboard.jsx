import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedDay, setSelectedDay] = useState(new Date().getDate());
  const [fact, setFact] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const months = [
    { name: 'January', days: 31 },
    { name: 'February', days: 29 }, // Assuming leap year for simplicity, or handle dynamically
    { name: 'March', days: 31 },
    { name: 'April', days: 30 },
    { name: 'May', days: 31 },
    { name: 'June', days: 30 },
    { name: 'July', days: 31 },
    { name: 'August', days: 31 },
    { name: 'September', days: 30 },
    { name: 'October', days: 31 },
    { name: 'November', days: 30 },
    { name: 'December', days: 31 },
  ];

  const handleFetchFact = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Please log in to access this feature.');
      navigate('/login');
      return;
    }

    try {
      const response = await axios.post(
        'http://localhost:8888/',
        { month: selectedMonth, day: selectedDay },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );
      if (response.data.status) {
        setMessage(response.data.status);
        if (response.data.status === "Session Expired please login again") {
          localStorage.removeItem('token');
          navigate('/login');
        }
      } else {
        setFact(response.data.result);
        setMessage('');
      }
    } catch (error) {
      setMessage('Error fetching fact.');
      console.error('Fact fetch error:', error);
    }
  };

  const handleMonthChange = (e) => {
    const newMonth = parseInt(e.target.value);
    setSelectedMonth(newMonth);
    if (selectedDay > months[newMonth - 1].days) {
      setSelectedDay(1);
    }
  };

  const handleDayClick = (day) => {
    setSelectedDay(day);
  };

  const daysInMonth = months[selectedMonth - 1].days;
  const daysArray = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  return (
    <div className="dashboard-container">
      <h2>Select a Date to Get a Number Fact</h2>
      <div className="calendar-selector">
        <div className="month-selector">
          <label>Month:</label>
          <select value={selectedMonth} onChange={handleMonthChange}>
            {months.map((month, index) => (
              <option key={index} value={index + 1}>
                {month.name}
              </option>
            ))}
          </select>
        </div>
        <div className="day-grid">
          {daysArray.map((day) => (
            <div
              key={day}
              className={`day-cell ${selectedDay === day ? 'selected' : ''}`}
              onClick={() => handleDayClick(day)}
            >
              {day}
            </div>
          ))}
        </div>
      </div>
      <button onClick={handleFetchFact}>Get Fact</button>
      {message && <p className="message">{message}</p>}
      {fact && <p className="fact-result"><strong>Fact:</strong> {fact}</p>}
    </div>
  );
}

export default Dashboard;

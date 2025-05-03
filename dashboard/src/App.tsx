import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SubscriptionsPage from './pages/SubscriptionsPage';
import EventPage from './pages/EventPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<SubscriptionsPage />} />
          <Route path="/events/:eventId" element={<EventPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
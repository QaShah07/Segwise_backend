import React from 'react';
import { useParams } from 'react-router-dom';
import { useEventStatus } from '../api';

export default function EventPage() {
  const { eventId } = useParams<{ eventId: string }>();
  const { data, isLoading } = useEventStatus(eventId!);

  if (isLoading) return <div>Loading event…</div>;
  return (
    <div className="p-4">
      <h1 className="text-xl">Event {data.event.id}</h1>
      <p>Status: {data.event.status}</p>
      <h2 className="mt-4 text-lg">Attempts</h2>
      <ul>
        {data.attempts.map((a: any) => (
          <li key={a.id}>{a.attempt_number} — {a.http_status} at {new Date(a.attempted_at).toLocaleString()}</li>
        ))}
      </ul>
    </div>
  );
}
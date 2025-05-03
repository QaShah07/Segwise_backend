import React from 'react';

interface EventStatusProps {
  event: { id: string; status: string; payload: any };
}

export default function EventStatus({ event }: EventStatusProps) {
  return (
    <div className="mb-4">
      <h2 className="text-lg">Event ID: {event.id}</h2>
      <p>Status: <span className="font-mono">{event.status}</span></p>
      <details className="mt-2 p-2 border rounded">
        <summary className="cursor-pointer">Payload</summary>
        <pre className="text-xs">{JSON.stringify(event.payload, null, 2)}</pre>
      </details>
    </div>
  );
}
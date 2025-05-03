import React from 'react';

interface AttemptLogsProps {
  attempts: Array<{ id: string; attempt_number: number; http_status: number; attempted_at: string }>;
}

export default function AttemptLogs({ attempts }: AttemptLogsProps) {
  if (!attempts.length) return <p>No attempts logged.</p>;
  return (
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr>
          <th className="border p-2">#</th>
          <th className="border p-2">HTTP Status</th>
          <th className="border p-2">Time</th>
        </tr>
      </thead>
      <tbody>
        {attempts.map(a => (
          <tr key={a.id}>
            <td className="border p-2">{a.attempt_number}</td>
            <td className="border p-2">{a.http_status}</td>
            <td className="border p-2">{new Date(a.attempted_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
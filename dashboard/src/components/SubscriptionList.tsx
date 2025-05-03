import React from 'react';
import { Link } from 'react-router-dom';

interface SubscriptionListProps {
  subs: Array<{ id: string; target_url: string; event_types: string[] }>;
}

export default function SubscriptionList({ subs }: SubscriptionListProps) {
  if (!subs.length) return <p>No subscriptions yet.</p>;
  return (
    <ul>
      {subs.map(sub => (
        <li key={sub.id} className="py-2">
          <Link to={`/events/${sub.id}`} className="text-blue-600 hover:underline">
            {sub.target_url}
          </Link>
          <span className="text-sm text-gray-500"> events: {sub.event_types.join(', ')}</span>
        </li>
      ))}
    </ul>
  );
}
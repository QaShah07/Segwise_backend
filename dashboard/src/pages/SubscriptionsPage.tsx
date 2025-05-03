import React from 'react';
import { useSubscriptions, useCreateSubscription } from '../api';
import SubscriptionForm from '../components/SubscriptionForm';

export default function SubscriptionsPage() {
  const { data, isLoading } = useSubscriptions();
  const create = useCreateSubscription();

  if (isLoading) return <div>Loading…</div>;

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Subscriptions</h1>
      <SubscriptionForm onCreate={create.mutate} />
      <ul className="mt-4">
        {data.results.map((sub: any) => (
          <li key={sub.id}>{sub.target_url} (events: {sub.event_types.join(',')})</li>
        ))}
      </ul>
    </div>
  );
}
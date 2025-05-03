import React, { useState } from 'react';

interface SubscriptionFormProps {
  onCreate: (data: { target_url: string; event_types: string[] }) => void;
}

export default function SubscriptionForm({ onCreate }: SubscriptionFormProps) {
  const [url, setUrl] = useState('');
  const [types, setTypes] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const event_types = types.split(',').map(s => s.trim());
    onCreate({ target_url: url, event_types });
    setUrl('');
    setTypes('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="mb-2">
        <label className="block text-sm">Target URL</label>
        <input
          type="url"
          value={url}
          onChange={e => setUrl(e.target.value)}
          required
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="mb-2">
        <label className="block text-sm">Event Types (comma-separated)</label>
        <input
          type="text"
          value={types}
          onChange={e => setTypes(e.target.value)}
          className="w-full p-2 border rounded"
        />
      </div>
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">Create</button>
    </form>
  );
}
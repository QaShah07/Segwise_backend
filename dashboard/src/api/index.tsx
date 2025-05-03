import axios from 'axios';
import { useQuery, useMutation, useQueryClient } from 'react-query';

const api = axios.create({ baseURL: '/api' });

// Subscriptions
export const useSubscriptions = () => useQuery('subs', () => api.get('/subscriptions/').then(res => res.data));
export const useCreateSubscription = () => {
  const qc = useQueryClient();
  return useMutation(
    (newSub: any) => api.post('/subscriptions/', newSub),
    { onSuccess: () => qc.invalidateQueries('subs') }
  );
};
// Event status
export const useEventStatus = (eventId: string) =>
    useQuery(['event', eventId], () => api.get(`/events/${eventId}/status/`).then(res => res.data));
  
  // Attempts
  export const useAttempts = (subId: string, page = 1) =>
    useQuery(['attempts', subId, page], () =>
      api.get(`/subscriptions/${subId}/attempts/?limit=20&page=${page}`).then(res => res.data)
    );
  
  export default api;
import type { Ticket, TicketFilters } from '~/types/ticket'

export function useTicketList(filters: TicketFilters) {
  const config = useRuntimeConfig()

  const query = computed(() => {
    const q: Record<string, string> = {}
    if (filters.status) q.status = filters.status
    if (filters.priority) q.priority = filters.priority
    return q
  })

  const { data: tickets, status, error, refresh } = useFetch<Ticket[]>('/api/tickets/', {
    baseURL: config.public.apiBase,
    query,
    default: () => []
  })

  const loading = computed(() => status.value === 'pending')
  const errorMessage = computed(() =>
    error.value ? 'Could not load tickets. Is the API running?' : ''
  )

  return { tickets, loading, error: errorMessage, refresh }
}

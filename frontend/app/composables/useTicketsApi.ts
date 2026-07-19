import type { NewTicket, Status, Ticket } from '~/types/ticket'

function extractErrorMessage(error: unknown): string {
  const data = (error as { data?: unknown } | undefined)?.data

  if (data && typeof data === 'object') {
    const [firstValue] = Object.values(data as Record<string, unknown>)
    if (Array.isArray(firstValue) && typeof firstValue[0] === 'string') {
      return firstValue[0]
    }
    if (typeof firstValue === 'string') {
      return firstValue
    }
  }

  return 'Something went wrong. Please try again.'
}

export function useTicketsApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  async function createTicket(payload: NewTicket): Promise<Ticket> {
    try {
      return await $fetch<Ticket>('/api/tickets/', {
        baseURL,
        method: 'POST',
        body: payload
      })
    } catch (error) {
      throw new Error(extractErrorMessage(error))
    }
  }

  async function updateTicketStatus(id: number, status: Status): Promise<Ticket> {
    try {
      return await $fetch<Ticket>(`/api/tickets/${id}/`, {
        baseURL,
        method: 'PATCH',
        body: { status }
      })
    } catch (error) {
      throw new Error(extractErrorMessage(error))
    }
  }

  return { createTicket, updateTicketStatus }
}

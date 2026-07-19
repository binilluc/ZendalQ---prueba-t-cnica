export type Priority = 'low' | 'medium' | 'high'
export type Status = 'open' | 'in_progress' | 'closed'

export interface Ticket {
  id: number
  title: string
  description: string
  priority: Priority
  status: Status
  created_at: string
  updated_at: string
}

export interface TicketFilters {
  status: Status | ''
  priority: Priority | ''
}

export interface NewTicket {
  title: string
  description: string
  priority: Priority
}

export const PRIORITIES: Priority[] = ['low', 'medium', 'high']
export const STATUSES: Status[] = ['open', 'in_progress', 'closed']

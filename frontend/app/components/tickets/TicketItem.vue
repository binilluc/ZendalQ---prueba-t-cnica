<script setup lang="ts">
import type { Status, Ticket } from '~/types/ticket'
import { STATUSES } from '~/types/ticket'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits<{ updated: [ticket: Ticket] }>()

const { updateTicketStatus } = useTicketsApi()

const isUpdating = ref(false)
const error = ref('')

async function onStatusChange(event: Event) {
  const select = event.target as HTMLSelectElement
  const newStatus = select.value as Status
  if (newStatus === props.ticket.status) return

  error.value = ''
  isUpdating.value = true
  try {
    const updated = await updateTicketStatus(props.ticket.id, newStatus)
    emit('updated', updated)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not update status.'
    select.value = props.ticket.status
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <tr class="ticket-row">
    <td>{{ ticket.title }}</td>
    <td><span class="badge" :class="`priority-${ticket.priority}`">{{ ticket.priority }}</span></td>
    <td>
      <select :value="ticket.status" :disabled="isUpdating" @change="onStatusChange">
        <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
      </select>
      <p v-if="error" class="error-text">{{ error }}</p>
    </td>
    <td>{{ new Date(ticket.created_at).toLocaleString() }}</td>
  </tr>
</template>

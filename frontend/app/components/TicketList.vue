<script setup lang="ts">
import type { Ticket } from '~/types/ticket'

defineProps<{
  tickets: Ticket[]
  loading: boolean
  error: string
}>()

const emit = defineEmits<{ updated: [ticket: Ticket] }>()
</script>

<template>
  <div class="ticket-list">
    <p v-if="loading">Loading tickets…</p>
    <p v-else-if="error" class="error-text">{{ error }}</p>
    <p v-else-if="tickets.length === 0">No tickets match the current filters.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Title</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <TicketItem
          v-for="ticket in tickets"
          :key="ticket.id"
          :ticket="ticket"
          @updated="emit('updated', $event)"
        />
      </tbody>
    </table>
  </div>
</template>

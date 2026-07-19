<script setup lang="ts">
import type { TicketFilters as TicketFiltersType } from '~/types/ticket'

const filters = reactive<TicketFiltersType>({ status: '', priority: '' })
const { tickets, loading, error, refresh } = useTicketList(filters)
</script>

<template>
  <main class="container">
    <h1>Ticket manager</h1>

    <section>
      <h2>New ticket</h2>
      <TicketForm @created="() => refresh()" />
    </section>

    <section>
      <div class="list-header">
        <h2>Tickets</h2>
        <TicketFilters v-model="filters" />
      </div>
      <TicketList :tickets="tickets" :loading="loading" :error="error" @updated="() => refresh()" />
    </section>
  </main>
</template>

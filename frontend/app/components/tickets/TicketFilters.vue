<script setup lang="ts">
import type { TicketFilters } from '~/types/ticket'
import { PRIORITIES, STATUSES } from '~/types/ticket'

const model = defineModel<TicketFilters>({ required: true })
</script>

<template>
  <div class="filters">
    <label>
      Status
      <select v-model="model.status">
        <option value="">All</option>
        <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
      </select>
    </label>
    <label>
      Priority
      <select v-model="model.priority">
        <option value="">All</option>
        <option v-for="p in PRIORITIES" :key="p" :value="p">{{ p }}</option>
      </select>
    </label>
  </div>
</template>

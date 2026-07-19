<script setup lang="ts">
import type { NewTicket, Ticket } from '~/types/ticket'
import { PRIORITIES } from '~/types/ticket'

const emit = defineEmits<{ created: [ticket: Ticket] }>()

const { createTicket } = useTicketsApi()

const form = reactive<NewTicket>({ title: '', description: '', priority: 'medium' })
const submitting = ref(false)
const error = ref('')

async function onSubmit() {
  error.value = ''

  if (!form.title.trim()) {
    error.value = 'Title is required.'
    return
  }

  submitting.value = true
  try {
    const ticket = await createTicket({ ...form, title: form.title.trim() })
    emit('created', ticket)
    form.title = ''
    form.description = ''
    form.priority = 'medium'
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Could not create the ticket.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="ticket-form" @submit.prevent="onSubmit">
    <div class="field">
      <label for="title">Title *</label>
      <input id="title" v-model="form.title" maxlength="120" required />
    </div>
    <div class="field">
      <label for="description">Description</label>
      <textarea id="description" v-model="form.description" rows="2" />
    </div>
    <div class="field">
      <label for="priority">Priority</label>
      <select id="priority" v-model="form.priority">
        <option v-for="p in PRIORITIES" :key="p" :value="p">{{ p }}</option>
      </select>
    </div>
    <button type="submit" :disabled="submitting">
      {{ submitting ? 'Creating…' : 'Create ticket' }}
    </button>
    <p v-if="error" class="error-text">{{ error }}</p>
  </form>
</template>

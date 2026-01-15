<template>
  <div class="container">
    <h1>Game Backlog Manager</h1>

    <div v-if="loading" class="loading">Loading tickets...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <ul v-else class="tickets-list">
      <li v-for="ticket in tickets" :key="ticket.id" class="ticket">
        <div class="ticket-header">
          <strong>{{ ticket.title }}</strong>
          <span class="ticket-id">#{{ ticket.id }}</span>
        </div>

        <div class="ticket-info">
          <span class="badge type">{{ ticket.type }}</span>
        </div>

        <div class="ticket-fields">
          <div class="field">
            <label>Status:</label>
            <select v-model="ticket.status" @change="saveTicket(ticket)">
              <option>open</option>
              <option>in_progress</option>
              <option>testing</option>
              <option>done</option>
            </select>
          </div>

          <div class="field">
            <label>Severity:</label>
            <select v-model="ticket.severity" @change="saveTicket(ticket)">
              <option>low</option>
              <option>medium</option>
              <option>high</option>
              <option>critical</option>
            </select>
          </div>

          <div class="field">
            <label>Assignee:</label>
            <input v-model="ticket.assignee" @change="saveTicket(ticket)" placeholder="none" />
          </div>
        </div>

        <div v-if="ticket.saving" class="saving">Saving...</div>
        <div v-if="ticket.error" class="field-error">{{ ticket.error }}</div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const tickets = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:8000/tickets")
    if (!res.ok) throw new Error("Failed to load tickets")
    tickets.value = await res.json()
    tickets.value.forEach(t => {
      t.saving = false
      t.error = null
    })
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

async function saveTicket(ticket) {
  ticket.saving = true
  ticket.error = null

  try {
    const res = await fetch(`http://localhost:8000/tickets/${ticket.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ticket)
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || "Failed to save")
    }
  } catch (e) {
    ticket.error = e.message
  } finally {
    ticket.saving = false
  }
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
}

.loading, .error {
  padding: 20px;
  text-align: center;
  font-weight: bold;
}

.error {
  color: #d32f2f;
  background: #ffebee;
  border-radius: 4px;
}

.tickets-list {
  list-style: none;
  padding: 0;
}

.ticket {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background: #fafafa;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.ticket-id {
  color: #666;
  font-size: 12px;
}

.ticket-info {
  margin-bottom: 12px;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge.type {
  background: #e3f2fd;
  color: #1976d2;
}

.ticket-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 8px;
}

.field {
  display: flex;
  flex-direction: column;
}

.field label {
  font-weight: bold;
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.field select,
.field input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.field select:focus,
.field input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 4px rgba(25, 118, 210, 0.3);
}

.saving {
  font-size: 12px;
  color: #1976d2;
  font-weight: bold;
}

.field-error {
  font-size: 12px;
  color: #d32f2f;
  margin-top: 8px;
}
</style>

<template>
  <div class="container">
    <h1>Game Backlog Manager</h1>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <div class="create-form">
        <h2>Create Ticket</h2>
        <div class="form-row">
          <input v-model="newTicket.title" placeholder="Title" />
          <select v-model="newTicket.type">
            <option value="">Type</option>
            <option value="bug">bug</option>
            <option value="feature">feature</option>
            <option value="test">test</option>
          </select>
          <button @click="createNewTicket" :disabled="createLoading">
            {{ createLoading ? "..." : "Create" }}
          </button>
        </div>
        <div v-if="createError" class="error-text">{{ createError }}</div>
      </div>

      <div v-for="t in tickets" :key="t.id" class="ticket">
        <div class="ticket-header">
          <strong>{{ t.title }}</strong>
          <span class="id">#{{ t.id }}</span>
        </div>
        <span class="badge">{{ t.type }}</span>

        <div class="fields">
          <select v-model="t.status" @change="saveTicket(t)">
            <option>open</option>
            <option>in_progress</option>
            <option>testing</option>
            <option>done</option>
          </select>
          <select v-model="t.severity" @change="saveTicket(t)">
            <option>low</option>
            <option>medium</option>
            <option>high</option>
            <option>critical</option>
          </select>
          <input v-model="t.assignee" @change="saveTicket(t)" placeholder="assignee" />
        </div>

        <div v-if="t.saving" class="saving">Saving...</div>
        <div v-if="t.error" class="error-text">{{ t.error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const tickets = ref([])
const loading = ref(true)
const error = ref(null)
const createLoading = ref(false)
const createError = ref(null)
const newTicket = ref({ title: "", type: "" })

onMounted(loadTickets)

async function loadTickets() {
  try {
    const res = await fetch("http://localhost:8000/tickets")
    if (!res.ok) throw new Error("Failed to load")
    tickets.value = await res.json()
    tickets.value.forEach(t => ({ ...t, saving: false, error: null }))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function createNewTicket() {
  if (!newTicket.value.title || !newTicket.value.type) {
    createError.value = "Fill all fields"
    return
  }

  createLoading.value = true
  createError.value = null

  try {
    const res = await fetch("http://localhost:8000/tickets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTicket.value)
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Failed")
    
    const ticket = await res.json()
    ticket.saving = false
    ticket.error = null
    tickets.value.push(ticket)
    newTicket.value = { title: "", type: "" }
  } catch (e) {
    createError.value = e.message
  } finally {
    createLoading.value = false
  }
}

async function saveTicket(t) {
  t.saving = true
  t.error = null

  try {
    const res = await fetch(`http://localhost:8000/tickets/${t.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(t)
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Failed")
  } catch (e) {
    t.error = e.message
  } finally {
    t.saving = false
  }
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: sans-serif;
}

h1, h2 {
  color: #333;
}

.loading, .error {
  padding: 15px;
  text-align: center;
  background: #fff3cd;
  border-radius: 4px;
}

.error {
  background: #f8d7da;
  color: #721c24;
}

.create-form {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 120px 80px;
  gap: 10px;
  margin-bottom: 10px;
}

input, select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input:focus, select:focus {
  outline: none;
  border-color: #1976d2;
}

button {
  background: #1976d2;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button:hover:not(:disabled) {
  background: #1565c0;
}

button:disabled {
  background: #ccc;
}

.ticket {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background: #fafafa;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.id {
  color: #999;
  font-size: 12px;
}

.badge {
  display: inline-block;
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 10px;
}

.fields {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 8px;
}

.saving {
  font-size: 12px;
  color: #1976d2;
  font-weight: bold;
}

.error-text {
  font-size: 12px;
  color: #d32f2f;
  margin-top: 5px;
}
</style>

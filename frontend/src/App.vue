<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">🎮 Game Backlog Manager</h1>

      <div v-if="loading" class="p-4 text-center bg-yellow-100 text-yellow-800 rounded-lg">Loading...</div>
      <div v-else-if="error" class="p-4 text-center bg-red-100 text-red-800 rounded-lg">{{ error }}</div>

      <div v-else class="space-y-6">
        <div class="bg-white shadow-md rounded-lg p-6 border border-gray-200">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Create Ticket</h2>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
            <input 
              v-model="newTicket.title" 
              placeholder="Title" 
              class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <select 
              v-model="newTicket.type"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Type</option>
              <option value="bug">bug</option>
              <option value="feature">feature</option>
              <option value="test">test</option>
            </select>
            <button 
              @click="createNewTicket" 
              :disabled="createLoading"
              class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg cursor-pointer transition-colors"
            >
              {{ createLoading ? "..." : "Create" }}
            </button>
          </div>
          <div v-if="createError" class="text-sm text-red-600 mt-2">{{ createError }}</div>
        </div>

        <div class="space-y-4">
          <div v-for="t in tickets" :key="t.id" class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-gray-900">{{ t.title }}</h3>
              <span class="text-xs text-gray-500 font-mono">#{{ t.id }}</span>
            </div>
            
            <span class="inline-block bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-medium mb-4">{{ t.type }}</span>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
              <select 
                v-model="t.status" 
                @change="saveTicket(t)"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option>open</option>
                <option>in_progress</option>
                <option>testing</option>
                <option>done</option>
              </select>
              <select 
                v-model="t.severity" 
                @change="saveTicket(t)"
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option>low</option>
                <option>medium</option>
                <option>high</option>
                <option>critical</option>
              </select>
              <input 
                v-model="t.assignee" 
                @change="saveTicket(t)" 
                placeholder="assignee" 
                class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div v-if="t.saving" class="text-xs text-blue-600 font-bold">⏳ Saving...</div>
            <div v-if="t.error" class="text-xs text-red-600 mt-1">❌ {{ t.error }}</div>
          </div>
        </div>
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
<style></style>
<template>
  <h1>Game Backlog</h1>

  <ul>
    <li v-for="t in tickets" :key="t.id">
      <strong>{{ t.title }}</strong>
      — {{ t.type }} | {{ t.status }} | {{ t.severity }}
    </li>
  </ul>
  
</template>

<script setup>
import { ref, onMounted } from "vue"

const tickets = ref([])

onMounted(async () => {
  const res = await fetch("http://localhost:8000/tickets")
  tickets.value = await res.json()
})
</script>

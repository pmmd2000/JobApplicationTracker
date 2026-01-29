<template>
  <div class="app-container">
    <Toast />
    <header class="app-header">
      <div class="header-content">
        <h1>
          <i class="pi pi-briefcase"></i>
          Job Application Tracker
        </h1>
        <p class="subtitle">Track your job applications with ease</p>
      </div>
    </header>
    
    <main class="app-main">
      <JobList />
    </main>
  </div>
</template>

<script setup>
import Toast from 'primevue/toast'
import JobList from './components/JobList.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8f9fa;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.app-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.app-header h1 .pi {
  font-size: 1.75rem;
}

.subtitle {
  font-size: 1rem;
  opacity: 0.95;
  font-weight: 400;
}

.app-main {
  flex: 1;
  padding: 2rem 1.5rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
</style>

<template>
  <div class="login-container">
    <Card class="login-card">
      <template #title>
        <div class="login-title">
          Job Tracker
        </div>
      </template>
      <template #subtitle>
        <div class="login-subtitle">
          Sign in to manage your applications
        </div>
      </template>
      <template #content>
        <div class="login-content">
          <Button 
            label="Sign in with Google" 
            icon="pi pi-google" 
            class="p-button-lg google-btn"
            @click="loginWithGoogle"
          />
          <div class="secure-text">
            Private &amp; Secure. Your data belongs to you.
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import Card from 'primevue/card'
import Button from 'primevue/button'

function loginWithGoogle() {
  window.location.href = '/api/auth/login'
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 70px);
  background: var(--surface-ground);
  padding: 2rem 1rem;
}

.login-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.login-subtitle {
  text-align: center;
  color: var(--text-color-secondary);
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.login-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.google-btn {
  background-color: #3b82f6 !important;
  border-color: #3b82f6 !important;
  width: 100%;
  justify-content: center;
  font-weight: 500;
}

.google-btn:hover {
  background-color: #2563eb !important;
  border-color: #2563eb !important;
}

.secure-text {
  font-size: 0.85rem;
  color: var(--text-color-secondary);
  text-align: center;
  margin-top: 1rem;
}
</style>

<!-- Unscoped styles to properly override PrimeVue Card internals -->
<style>
.login-card.p-card {
  width: 100%;
  max-width: 400px;
  border-radius: 16px;
  overflow: hidden;
}

/* Light mode — soft off-white, not harsh pure white */
.login-card.p-card,
.login-card.p-card .p-card-body {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

/* Dark mode — hardcoded slate-800 for guaranteed contrast against black ground */
.app-dark .login-card.p-card,
.app-dark .login-card.p-card .p-card-body {
  background: #1e293b !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}
</style>

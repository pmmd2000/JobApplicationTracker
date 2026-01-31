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
            Private & Secure. Your data belongs to you.
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
  min-height: 100vh;
  background: var(--surface-ground);
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  border: 1px solid var(--surface-border);
  background: var(--surface-card);
}

:global(.app-dark) .login-card {
  box-shadow: 0 10px 40px rgba(10, 2, 34, 0);
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

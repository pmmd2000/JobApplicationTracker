<template>
  <div class="app-container" :class="{ 'app-dark': isDarkMode }">
    <Toast />
    <ConfirmDialog />
    <header class="app-header">
      <div class="header-content">
        <!-- Logo Section -->
        <div class="header-left">
            <h1>
                <i class="pi pi-briefcase"></i>
                Job Application Tracker
            </h1>
            <p class="subtitle">Track your job applications with ease</p>
        </div>

        <!-- Right Section: Theme Toggle + User -->
        <div class="header-right">
            <!-- Theme Toggle -->
            <button class="theme-toggle" @click="toggleTheme" :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'">
                <i :class="isDarkMode ? 'pi pi-sun' : 'pi pi-moon'"></i>
            </button>

            <!-- User Menu -->
            <div class="user-chip" v-if="user" @click="toggleMenu" aria-haspopup="true" aria-controls="user_menu">
                <Avatar 
                    :image="user.avatar_url" 
                    :label="!user.avatar_url ? user.name[0] : null"
                    shape="circle" 
                    class="user-avatar"
                />
                <div class="user-details">
                    <span class="user-name">{{ user.name }}</span>
                    <span class="user-action">View Profile</span>
                </div>
                <i class="pi pi-angle-down"></i>
            </div>
            
            <Menu ref="menu" id="user_menu" :model="menuItems" :popup="true" />
        </div>
      </div>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import api from './services/api'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const user = ref(null)
const menu = ref(null)

// Dark mode state
const isDarkMode = ref(false)


const menuItems = ref([
    {
        label: 'Profile',
        items: [
            {
                label: 'Sign Out',
                icon: 'pi pi-sign-out',
                command: () => logout()
            }
        ]
    }
])

function toggleMenu(event) {
    menu.value.toggle(event)
}

function toggleTheme() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    applyTheme()
}

function applyTheme() {
    if (isDarkMode.value) {
        document.documentElement.classList.add('app-dark')
    } else {
        document.documentElement.classList.remove('app-dark')
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
        isDarkMode.value = savedTheme === 'dark'
    } else {
        // Auto-detect system preference
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        isDarkMode.value = mediaQuery.matches
        
        // Listen for system changes
        mediaQuery.addEventListener('change', handleSystemThemeChange)
    }
    applyTheme()
}

function handleSystemThemeChange(e) {
    if (!localStorage.getItem('theme')) {
        isDarkMode.value = e.matches
        applyTheme()
    }
}

onMounted(() => {
    initTheme()
    checkUser()
})

onUnmounted(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.removeEventListener('change', handleSystemThemeChange)
})

async function checkUser() {
    const auth = await api.checkAuth()
    if (auth.authenticated) {
        user.value = auth.user
    } else {
        user.value = null
    }
}

async function logout() {
    try {
        await axios.post('/api/auth/logout')
        user.value = null
        router.push('/login')
    } catch (e) {
        console.error('Logout failed', e)
    }
}

onMounted(() => {
    initTheme()
    checkUser()
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--surface-ground);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Light mode defaults */
:root {
  --header-bg: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  --header-accent: #3b82f6;
}

/* Dark mode overrides */
.app-dark {
  --header-bg: linear-gradient(135deg, #0f172a 0%, #020617 100%);
  --header-accent: #60a5fa;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--header-bg);
  color: white;
  padding: 1rem 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 10;
  border-bottom: 1px solid rgba(59, 130, 246, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.header-left h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 i {
  font-size: 1.75rem;
  color: var(--header-accent);
}

.subtitle {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 4px;
  margin-left: 2px;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Theme Toggle Button */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.1rem;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.theme-toggle:active {
  transform: scale(0.95);
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px 6px 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.user-chip:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}

.user-details {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-right: 4px;
}

.user-name {
  font-weight: 600;
  color: white;
  font-size: 0.95rem;
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-action {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.pi-angle-down {
  color: white;
  font-size: 0.9rem;
  opacity: 0.7;
}

.app-main {
  flex: 1;
  padding: 2rem 1.5rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Scrollbar styling - Light mode */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: var(--surface-100); 
}
::-webkit-scrollbar-thumb {
  background: var(--surface-400); 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--surface-500); 
}

/* Dark mode scrollbar */
.app-dark ::-webkit-scrollbar-track {
  background: var(--surface-800);
}
.app-dark ::-webkit-scrollbar-thumb {
  background: var(--surface-600);
}
.app-dark ::-webkit-scrollbar-thumb:hover {
  background: var(--surface-500);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  .header-left h1 {
    justify-content: center;
  }
  .header-right {
    width: 100%;
    justify-content: center;
  }
  .user-details {
    display: none;
  }
}

</style>

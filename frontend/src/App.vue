<template>
  <div class="app-container">
    <Toast />
    <ConfirmDialog />
    <header class="app-header" v-if="!isLoginPage">
      <div class="header-content">
        <!-- Logo Section -->
        <div class="header-left">
            <h1>
                <i class="pi pi-briefcase"></i>
                Job Application Tracker
            </h1>
            <p class="subtitle">Track your job applications with ease</p>
        </div>

        <!-- User Section -->
        <div class="header-right" v-if="user">
            <div class="user-chip" @click="toggleMenu" aria-haspopup="true" aria-controls="user_menu">
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
import { computed, ref, onMounted } from 'vue'
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

const isLoginPage = computed(() => route.path === '/login')

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
    checkUser()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8fafc;
  color: #1e293b;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  color: white;
  padding: 1rem 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 10;
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
}

.subtitle {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.85);
  margin-top: 4px;
  margin-left: 2px;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px 6px 6px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.user-chip:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.pi-angle-down {
  color: white;
  font-size: 0.9rem;
  opacity: 0.8;
}

.app-main {
  flex: 1;
  padding: 2rem 1.5rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9; 
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8; 
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
}
</style>

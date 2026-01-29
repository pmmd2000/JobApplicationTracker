<template>
  <div class="job-list-container">
    <Card>
      <template #title>
        <div class="card-header">
          <h2>My Applications</h2>
          <Button 
            label="Add New Job" 
            icon="pi pi-plus" 
            @click="openAddDialog"
            severity="success"
          />
        </div>
      </template>
      
      <template #content>
        <DataTable 
          :value="applications" 
          :loading="loading"
          stripedRows
          sortField="application_date" 
          :sortOrder="-1"
          paginator 
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20, 50]"
          tableStyle="min-width: 50rem"
        >
          <template #empty>
            <div class="empty-state">
              <i class="pi pi-inbox"></i>
              <p>No job applications yet. Click "Add New Job" to get started!</p>
            </div>
          </template>
          
          <Column field="company_name" header="Company" sortable></Column>
          <Column field="position_title" header="Position" sortable></Column>
          <Column field="location" header="Location" sortable></Column>
          <Column field="status" header="Status" sortable>
            <template #body="slotProps">
              <Tag 
                :value="slotProps.data.status" 
                :severity="getStatusSeverity(slotProps.data.status)"
              />
            </template>
          </Column>
          <Column field="application_date" header="Applied Date" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.application_date) }}
            </template>
          </Column>
          <Column header="Actions" :exportable="false">
            <template #body="slotProps">
              <div class="action-buttons">
                <Button 
                  icon="pi pi-pencil" 
                  text 
                  rounded 
                  @click="openEditDialog(slotProps.data)"
                  v-tooltip.top="'Edit'"
                />
                <Button 
                  icon="pi pi-trash" 
                  text 
                  rounded 
                  severity="danger"
                  @click="confirmDelete(slotProps.data)"
                  v-tooltip.top="'Delete'"
                />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
    
    <JobForm 
      v-model:visible="showDialog"
      :application="selectedApplication"
      @saved="onJobSaved"
    />
    
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ConfirmDialog from 'primevue/confirmdialog'
import Tooltip from 'primevue/tooltip'
import JobForm from './JobForm.vue'
import api from '../services/api'

const toast = useToast()
const confirm = useConfirm()

const applications = ref([])
const loading = ref(false)
const showDialog = ref(false)
const selectedApplication = ref(null)

// Load applications on mount
onMounted(() => {
  loadApplications()
})

async function loadApplications() {
  loading.value = true
  try {
    applications.value = await api.getApplications()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load job applications',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

function openAddDialog() {
  selectedApplication.value = null
  showDialog.value = true
}

function openEditDialog(application) {
  selectedApplication.value = { ...application }
  showDialog.value = true
}

function confirmDelete(application) {
  confirm.require({
    message: `Are you sure you want to delete the application for ${application.position_title} at ${application.company_name}?`,
    header: 'Confirm Deletion',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined',
    rejectLabel: 'Cancel',
    acceptLabel: 'Delete',
    acceptClass: 'p-button-danger',
    accept: () => deleteApplication(application.id)
  })
}

async function deleteApplication(id) {
  try {
    await api.deleteApplication(id)
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Application deleted successfully',
      life: 3000
    })
    await loadApplications()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete application',
      life: 3000
    })
  }
}

function onJobSaved() {
  loadApplications()
  showDialog.value = false
}

function getStatusSeverity(status) {
  const severityMap = {
    'Applied': 'secondary',
    'Interviewing': 'info',
    'Offered': 'success',
    'Rejected': 'danger',
    'Withdrawn': 'warn'
  }
  return severityMap[status] || 'secondary'
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}
</script>

<style scoped>
.job-list-container {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #334155;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #64748b;
}

.empty-state .pi {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1rem;
  margin: 0;
}
</style>

<template>
  <Dialog 
    v-model:visible="dialogVisible"
    :header="isEdit ? 'Edit Job Application' : 'Add New Job Application'"
    :modal="true"
    :style="{ width: '600px' }"
    @hide="resetForm"
  >
    <div class="form-container">
      <div class="field">
        <label for="company_name">Company Name *</label>
        <InputText 
          id="company_name"
          v-model="formData.company_name"
          :class="{ 'p-invalid': submitted && !formData.company_name }"
          placeholder="Enter company name"
        />
        <small class="p-error" v-if="submitted && !formData.company_name">
          Company name is required
        </small>
      </div>

      <div class="field">
        <label for="position_title">Position Title *</label>
        <InputText 
          id="position_title"
          v-model="formData.position_title"
          :class="{ 'p-invalid': submitted && !formData.position_title }"
          placeholder="Enter position title"
        />
        <small class="p-error" v-if="submitted && !formData.position_title">
          Position title is required
        </small>
      </div>

      <div class="field">
        <label for="location">Location</label>
        <InputText 
          id="location"
          v-model="formData.location"
          placeholder="e.g., Remote, New York, NY"
        />
      </div>

      <div class="field-group">
        <div class="field">
          <label for="job_type">Job Type</label>
          <Select 
            id="job_type"
            v-model="formData.job_type"
            :options="jobTypes"
            placeholder="Select job type"
            showClear
          />
        </div>

        <div class="field">
          <label for="job_level">Job Level</label>
          <Select 
            id="job_level"
            v-model="formData.job_level"
            :options="jobLevels"
            placeholder="Select job level"
            showClear
          />
        </div>
      </div>

      <div class="field-group">
        <div class="field">
          <label for="application_date">Application Date *</label>
          <DatePicker 
            id="application_date"
            v-model="formData.application_date"
            dateFormat="yy-mm-dd"
            showIcon
            :showButtonBar="true"
          />
        </div>

        <div class="field">
          <label for="status">Status</label>
          <Select 
            id="status"
            v-model="formData.status"
            :options="statuses"
            placeholder="Select status"
          />
        </div>
      </div>

      <div class="field">
        <label for="job_description">Job Description</label>
        <Textarea 
          id="job_description"
          v-model="formData.job_description"
          rows="4"
          placeholder="Paste the job description here..."
        />
      </div>

      <div class="col-span-2">
          <label for="notes" class="block font-bold mb-2 text-surface-700 dark:text-surface-200">Notes (Optional)</label>
          <Textarea 
              id="notes" 
              v-model="formData.notes" 
              rows="3" 
              class="w-full"
              placeholder="Key contacts, salary info, specific requirements..."
          />
      </div>

      <!-- Phase 2: Document Uploads -->
      <div class="col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <FileUpload
              v-model="resumeFile"
              :existing-file="existingResume"
              label="Resume"
              accept=".pdf,.docx,.doc"
              :required="false"
              :download-url="getResumeUrl(application?.id)"
              @remove-existing="deleteResumeFile"
          />
          
          <FileUpload
              v-model="coverLetterFile"
              :existing-file="existingCoverLetter"
              label="Cover Letter"
              accept=".pdf,.docx,.doc"
              :required="false"
              :download-url="getCoverLetterUrl(application?.id)"
              @remove-existing="deleteCoverLetterFile"
          />
      </div>
    </div>

    <template #footer>
      <Button 
        label="Cancel" 
        icon="pi pi-times" 
        @click="closeDialog"
        severity="secondary"
        outlined
      />
      <Button 
        label="Save" 
        icon="pi pi-check" 
        @click="saveApplication"
        :loading="saving"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import FileUpload from './FileUpload.vue'
import api from '../services/api'

const props = defineProps({
  visible: Boolean,
  application: Object
})

const emit = defineEmits(['update:visible', 'saved'])

const toast = useToast()

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEdit = computed(() => !!props.application?.id)

// File Upload State
const resumeFile = ref(null)
const coverLetterFile = ref(null)

const existingResume = computed(() => props.application?.resume_filename)
const existingCoverLetter = computed(() => props.application?.cover_letter_filename)

function getResumeUrl(id) {
    if (!id) return '#'
    return api.getResumeUrl(id)
}

function getCoverLetterUrl(id) {
    if (!id) return '#'
    return api.getCoverLetterUrl(id)
}

async function deleteResumeFile() {
    if (!props.application?.id) return
    try {
        await api.deleteResume(props.application.id)
        emit('saved') // Refresh parent data
        toast.add({ severity: 'success', summary: 'Success', detail: 'Resume deleted', life: 3000 })
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete resume', life: 3000 })
    }
}

async function deleteCoverLetterFile() {
    if (!props.application?.id) return
    try {
        await api.deleteCoverLetter(props.application.id)
        emit('saved') // Refresh parent data
        toast.add({ severity: 'success', summary: 'Success', detail: 'Cover letter deleted', life: 3000 })
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete cover letter', life: 3000 })
    }
}

const jobTypes = ref([
  'Full-time',
  'Part-time',
  'Contract',
  'Temporary',
  'Internship',
  'Freelance'
])

const jobLevels = ref([
  'Entry',
  'Junior',
  'Mid',
  'Senior',
  'Lead',
  'Principal',
  'Manager',
  'Director',
  'Executive'
])

const statuses = ref([
  'Applied',
  'Interviewing',
  'Offered',
  'Rejected',
  'Withdrawn'
])

const formData = ref({
  company_name: '',
  position_title: '',
  location: '',
  job_type: null,
  job_level: null,
  application_date: new Date(),
  status: 'Applied',
  job_description: '',
  notes: ''
})

const submitted = ref(false)
const saving = ref(false)

// Watch for application prop changes to populate form
watch(() => props.application, (newVal) => {
  if (newVal) {
    formData.value = {
      company_name: newVal.company_name || '',
      position_title: newVal.position_title || '',
      location: newVal.location || '',
      job_type: newVal.job_type || null,
      job_level: newVal.job_level || null,
      application_date: newVal.application_date ? new Date(newVal.application_date) : new Date(),
      status: newVal.status || 'Applied',
      job_description: newVal.job_description || '',
      notes: newVal.notes || ''
    }
  } else {
    resetForm()
  }
  // Reset file inputs when dialog opens/application changes
  resumeFile.value = null
  coverLetterFile.value = null
}, { immediate: true })

function resetForm() {
  formData.value = {
    company_name: '',
    position_title: '',
    location: '',
    job_type: null,
    job_level: null,
    application_date: new Date(),
    status: 'Applied',
    job_description: '',
    notes: ''
  }
  submitted.value = false
  resumeFile.value = null
  coverLetterFile.value = null
}

function closeDialog() {
  dialogVisible.value = false
}

async function saveApplication() {
  submitted.value = true

  // Validate required fields
  if (!formData.value.company_name || !formData.value.position_title) {
    return
  }

  saving.value = true

  try {
    const payload = {
      ...formData.value,
      application_date: formData.value.application_date instanceof Date 
        ? formData.value.application_date.toISOString().split('T')[0]
        : formData.value.application_date
    }

    let appId = props.application?.id
    let isNew = false

    if (isEdit.value) {
      await api.updateApplication(appId, payload)
    } else {
      const response = await api.createApplication(payload)
      appId = response.id
      isNew = true
    }

    // Handle File Uploads
    const uploadPromises = []
    if (resumeFile.value) {
        uploadPromises.push(api.uploadResume(appId, resumeFile.value))
    }
    if (coverLetterFile.value) {
        uploadPromises.push(api.uploadCoverLetter(appId, coverLetterFile.value))
    }
    
    if (uploadPromises.length > 0) {
        await Promise.all(uploadPromises)
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: isNew ? 'Application created successfully' : 'Application updated successfully',
      life: 3000
    })

    emit('saved')
    closeDialog()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.error || 'Failed to save application',
      life: 3000
    })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.form-container {
  padding: 1rem 0;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.field-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.p-inputtext,
.p-textarea,
.p-select,
.p-datepicker {
  width: 100%;
}

.p-error {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>

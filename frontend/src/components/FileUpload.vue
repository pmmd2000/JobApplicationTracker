<template>
    <div class="file-upload-wrapper">
        <label v-if="label" class="upload-label">{{ label }} <span v-if="required" class="required-star">*</span></label>
        
        <div class="upload-controls">
            <!-- Hidden File Input -->
            <input 
                type="file" 
                :accept="accept"
                @change="handleFileChange"
                class="hidden-input"
                ref="fileInput" 
                :id="inputId"
            />
            
            <!-- Custom Trigger Button -->
            <div 
                class="upload-box" 
                :class="{'has-error': error, 'has-file': fileName}"
                @click="triggerUpload"
            >
                <div class="file-info">
                    <i :class="getIcon()" class="file-icon"></i>
                    <span class="file-name">
                        {{ fileName || 'Choose a file...' }}
                    </span>
                </div>
                <span class="file-types">{{ acceptedExtensions }}</span>
            </div>

            <!-- Actions -->
            <div class="actions">
                <Button 
                    v-if="modelValue || existingFile" 
                    icon="pi pi-trash" 
                    severity="danger" 
                    text 
                    rounded 
                    @click="clearFile"
                    v-tooltip.top="'Remove File'"
                />
                
                <a 
                    v-if="!modelValue && existingFile" 
                    :href="downloadUrl" 
                    target="_blank"
                    class="download-link"
                    v-tooltip.top="'Download Current'"
                >
                    <i class="pi pi-download"></i>
                </a>
            </div>
        </div>
        
        <small v-if="error" class="error-msg">{{ error }}</small>
        <small v-else class="help-msg">Max 10MB. Allowed: {{ acceptedExtensions }}</small>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Button from 'primevue/button'; // Import Button component

const props = defineProps({
    modelValue: {
        type: [File, null],
        default: null
    },
    existingFile: { // Flag or filename if file already exists on server
        type: String,
        default: null
    },
    downloadUrl: {
        type: String,
        default: '#'
    },
    label: {
        type: String,
        default: ''
    },
    required: {
        type: Boolean,
        default: false
    },
    accept: {
        type: String,
        default: '.pdf,.docx,.doc'
    },
    maxSize: { // in bytes, default 10MB
        type: Number,
        default: 10485760 
    }
});

const emit = defineEmits(['update:modelValue', 'remove-existing']);

const fileInput = ref(null);
const error = ref('');
const inputId = `file-upload-${Math.random().toString(36).substr(2, 9)}`;

const fileName = computed(() => {
    if (props.modelValue) return props.modelValue.name;
    if (props.existingFile) return props.existingFile; // Show existing filename
    return '';
});

const acceptedExtensions = computed(() => {
    return props.accept.split(',').join(', ');
});

const getIcon = () => {
    if (!fileName.value) return 'pi pi-upload';
    if (fileName.value.endsWith('.pdf')) return 'pi pi-file-pdf';
    return 'pi pi-file-word'; // simplified for doc/docx
};

const triggerUpload = () => {
    fileInput.value.click();
};

const handleFileChange = (event) => {
    const file = event.target.files[0];
    error.value = '';

    if (!file) return;

    // Validate size
    if (file.size > props.maxSize) {
        error.value = `File size must be less than ${Math.round(props.maxSize / 1024 / 1024)}MB`;
        event.target.value = ''; // reset input
        return;
    }

    // Validate type (basic extension check)
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    const allowed = props.accept.split(',').map(e => e.trim().toLowerCase());
    
    // Simple check if extension is in list or wildcard
    if (!props.accept.includes('*') && !allowed.includes(extension)) {
        error.value = 'Invalid file type';
        event.target.value = '';
        return;
    }

    emit('update:modelValue', file);
};

const clearFile = () => {
    if (fileInput.value) fileInput.value.value = ''; // reset input
    emit('update:modelValue', null); // Clear selected file
    
    if (props.existingFile) {
        emit('remove-existing'); // Signal parent to delete server file
    }
    
    error.value = '';
};
</script>

<style scoped>
.file-upload-wrapper {
    margin-bottom: 1rem;
}

.upload-label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--surface-700);
}

.dark .upload-label {
    color: var(--surface-200);
}

.required-star {
    color: #ef4444;
}

.upload-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hidden-input {
    display: none;
}

.upload-box {
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border: 1px solid var(--surface-300);
    border-radius: 6px;
    background-color: var(--surface-0);
    cursor: pointer;
    transition: all 0.2s;
    overflow: hidden;
}

.dark .upload-box {
    border-color: var(--surface-700);
    background-color: var(--surface-900);
}

.upload-box:hover {
    border-color: var(--primary-500);
}

.upload-box.has-error {
    border-color: #ef4444;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    overflow: hidden;
}

.file-icon {
    font-size: 1.25rem;
    color: var(--primary-500);
}

.file-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--surface-700);
}

.dark .file-name {
    color: var(--surface-200);
}

.file-types {
    font-size: 0.75rem;
    color: var(--surface-500);
    margin-left: 0.5rem;
    white-space: nowrap;
}

.actions {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.download-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    color: var(--surface-500);
    transition: background-color 0.2s;
    text-decoration: none;
}

.download-link:hover {
    background-color: var(--surface-100);
    color: var(--surface-700);
}

.dark .download-link:hover {
    background-color: var(--surface-800);
    color: var(--surface-200);
}

.error-msg {
    color: #ef4444;
    display: block;
    margin-top: 0.25rem;
    font-size: 0.875rem;
}

.help-msg {
    color: var(--surface-500);
    display: block;
    margin-top: 0.25rem;
    font-size: 0.875rem;
}
</style>

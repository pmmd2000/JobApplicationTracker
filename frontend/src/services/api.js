import axios from 'axios'

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Response error interceptor
apiClient.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
    }
)

export default {
    /**
     * Get all job applications
     */
    async getApplications() {
        const response = await apiClient.get('/applications')
        return response.data
    },

    /**
     * Get a single job application by ID
     */
    async getApplication(id) {
        const response = await apiClient.get(`/applications/${id}`)
        return response.data
    },

    /**
     * Create a new job application
     */
    async createApplication(data) {
        const response = await apiClient.post('/applications', data)
        return response.data
    },

    /**
     * Update an existing job application
     */
    async updateApplication(id, data) {
        const response = await apiClient.put(`/applications/${id}`, data)
        return response.data
    },

    /**
     * Delete a job application
     */
    async deleteApplication(id) {
        const response = await apiClient.delete(`/applications/${id}`)
        return response.data
    },

    // --- Document Management ---

    async uploadResume(id, file) {
        const formData = new FormData()
        formData.append('file', file)
        const response = await apiClient.post(`/applications/${id}/resume`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return response.data
    },

    async deleteResume(id) {
        const response = await apiClient.delete(`/applications/${id}/resume`)
        return response.data
    },

    async uploadCoverLetter(id, file) {
        const formData = new FormData()
        formData.append('file', file)
        const response = await apiClient.post(`/applications/${id}/cover-letter`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return response.data
    },

    async deleteCoverLetter(id) {
        const response = await apiClient.delete(`/applications/${id}/cover-letter`)
        return response.data
    },

    getResumeUrl(id) {
        return `/api/applications/${id}/resume`
    },

    getCoverLetterUrl(id) {
        return `/api/applications/${id}/cover-letter`
    },

    async checkAuth() {
        try {
            const response = await apiClient.get('/auth/me');
            return response.data;
        } catch (error) {
            return { authenticated: false };
        }
    }
}

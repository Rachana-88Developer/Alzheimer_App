const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function authHeaders() {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function login(username, password) {
  const body = new URLSearchParams()
  body.append('username', username)
  body.append('password', password)
  const res = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })
  if (!res.ok) throw new Error('Invalid credentials')
  return res.json()
}

export async function apiGet(path) {
  const res = await fetch(`${BASE}${path}`, { headers: { ...authHeaders() } })
  if (!res.ok) throw new Error(`GET ${path} failed`)
  return res.json()
}

export async function apiPost(path, data) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `POST ${path} failed`)
  }
  return res.json()
}

export async function fetchPatients() {
  return apiGet('/api/patients')
}

export async function fetchSampleMRIs() {
  return apiGet('/api/mri/samples')
}

export async function fetchPatientMRIs(patientId) {
  return apiGet(`/api/mri/patient/${patientId}`)
}

export async function uploadMRI(patientId, file) {
  const formData = new FormData()
  formData.append('patient_id', patientId)
  formData.append('file', file)

  const res = await fetch(`${BASE}/api/mri/upload`, {
    method: 'POST',
    headers: { ...authHeaders() },
    body: formData,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'MRI upload failed')
  }
  return res.json()
}

export async function analyzeSampleMRI(patientId, sampleKey) {
  const formData = new FormData()
  formData.append('patient_id', patientId)
  formData.append('sample_key', sampleKey)

  const res = await fetch(`${BASE}/api/mri/analyze-sample`, {
    method: 'POST',
    headers: { ...authHeaders() },
    body: formData,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Sample MRI analysis failed')
  }
  return res.json()
}

export function reportUrl(assessmentId) {
  return `${BASE}/api/assessments/${assessmentId}/report`
}

export { BASE }



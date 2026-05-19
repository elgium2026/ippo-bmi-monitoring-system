const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

function getErrorMessage(errorData) {
  if (!errorData) return 'Server error.'
  if (typeof errorData === 'string') return errorData
  if (typeof errorData.detail === 'string') return errorData.detail
  if (typeof errorData.message === 'string') return errorData.message
  if (typeof errorData === 'object') {
    for (const key of Object.keys(errorData)) {
      const value = errorData[key]
      if (Array.isArray(value)) {
        return `${key}: ${value.join(', ')}`
      }
      if (typeof value === 'string') {
        return `${key}: ${value}`
      }
    }
  }
  return 'Server error.'
}

async function request(path, options = {}) {
  const { headers, ...fetchOptions } = options
  const response = await fetch(`${API_URL}${path}`, {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  })
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Server error.' }))
    const message = getErrorMessage(errorData)
    const error = new Error(message)
    error.data = errorData
    throw error
  }
  return response.json()
}

export function signup(data) {
  return request('/signup/', { method: 'POST', body: JSON.stringify(data) })
}

export function personnelLogin(data) {
  return request('/personnel/login/', { method: 'POST', body: JSON.stringify(data) })
}

export function computeBMI(data, token) {
  return request('/personnel/compute/', { method: 'POST', body: JSON.stringify(data), headers: { Authorization: `Bearer ${token}` } })
}

export function adminLogin(data) {
  return request('/admin/login/', { method: 'POST', body: JSON.stringify(data) })
}

export function adminChangePassword(data, token) {
  return request('/admin/change-password/', { method: 'POST', body: JSON.stringify(data), headers: { Authorization: `Bearer ${token}` } })
}

export function adminForgotPassword(data) {
  return request('/admin/forgot-password/', { method: 'POST', body: JSON.stringify(data) })
}

export function adminVerifyOtp(data) {
  return request('/admin/verify-otp/', { method: 'POST', body: JSON.stringify(data) })
}

export function fetchPersonnel(token) {
  return request('/admin/personnel/', { headers: { Authorization: `Bearer ${token}` } })
}

export function fetchLoginHistory(token) {
  return request('/admin/login-history/', { headers: { Authorization: `Bearer ${token}` } })
}

export function updatePersonnel(id, data, token) {
  return request(`/admin/personnel/${id}/`, { method: 'PUT', body: JSON.stringify(data), headers: { Authorization: `Bearer ${token}` } })
}

export function resetPersonnelPassword(id, data, token) {
  return request(`/admin/personnel/${id}/reset-password/`, { method: 'POST', body: JSON.stringify(data), headers: { Authorization: `Bearer ${token}` } })
}

export function deletePersonnel(id, token) {
  return request(`/admin/personnel/${id}/`, { method: 'DELETE', headers: { Authorization: `Bearer ${token}` } })
}

export function exportPersonnel(token) {
  return fetch(`${API_URL}/admin/export/`, { headers: { Authorization: `Bearer ${token}` } })
    .then(async response => {
      if (!response.ok) throw new Error('Export failed')
      const blob = await response.blob()
      return blob
    })
}

import { useEffect, useState } from 'react'
import {
  fetchPersonnel,
  fetchLoginHistory,
  updatePersonnel,
  resetPersonnelPassword,
  deletePersonnel,
  exportPersonnel,
} from '../api.js'

const reportColumns = [
  { label: 'UNIT', value: user => (user.unit === 'Other Units (Please Specify)' ? user.unit_other : user.unit) },
  { label: 'RANK', value: user => user.rank },
  { label: 'LAST NAME', value: user => user.last_name },
  { label: 'FIRST NAME', value: user => user.first_name },
  { label: 'MIDDLE NAME', value: user => user.middle_name },
  { label: 'QLFR', value: user => user.qualifier },
  { label: 'BIRTHDATE', value: user => user.birthdate },
  { label: 'AGE', value: user => user.age },
  { label: 'SEX', value: user => user.sex },
  { label: 'WEIGHT (kg)', value: user => user.weight_kg },
  { label: 'HEIGHT (cm)', value: user => user.height_cm },
  { label: 'WAIST (cm)', value: user => user.waist_cm },
  { label: 'HIP (cm)', value: user => user.hip_cm },
  { label: 'WRIST (cm)', value: user => user.wrist_cm },
  { label: 'BMI', value: user => user.bmi },
  { label: 'PNP BMI ACCEPTABLE STANDARD', value: user => user.pnp_bmi_classification },
  { label: 'WHO STANDARD', value: user => user.who_bmi_classification },
  { label: 'Weight to Lose (Kg)', value: user => user.weight_to_lose },
  { label: 'Normal Weight (Kg)', value: user => user.max_normal_weight },
  { label: 'REMARKS', value: user => user.remarks, className: 'remarks-cell' },
]

function displayValue(value) {
  return value === null || value === undefined || value === '' ? '-' : value
}

function formatTimestamp(value) {
  if (!value) return '-'
  return new Date(value).toLocaleString()
}

function getErrorMessage(error, fallback) {
  if (error.detail) return error.detail
  const firstField = Object.keys(error)[0]
  const firstValue = firstField ? error[firstField] : null
  if (Array.isArray(firstValue)) return `${firstField}: ${firstValue[0]}`
  if (typeof firstValue === 'string') return `${firstField}: ${firstValue}`
  return fallback
}

export default function AdminDashboard({ admin, token, onLogout }) {
  const [personnel, setPersonnel] = useState([])
  const [history, setHistory] = useState([])
  const [selected, setSelected] = useState(null)
  const [resetUser, setResetUser] = useState(null)
  const [resetForm, setResetForm] = useState({ password: '', confirm_password: '' })
  const [form, setForm] = useState({})
  const [status, setStatus] = useState(null)

  useEffect(() => {
    loadPersonnel()
    loadHistory()
  }, [])

  const loadPersonnel = async () => {
    try {
      const data = await fetchPersonnel(token)
      setPersonnel(data)
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Could not load personnel records.' })
    }
  }

  const loadHistory = async () => {
    try {
      const data = await fetchLoginHistory(token)
      setHistory(data)
    } catch (error) {
      setStatus({ type: 'error', message: getErrorMessage(error, 'Could not load access log history.') })
    }
  }

  const handleSelect = user => {
    setSelected(user)
    setForm({
      rank: user.rank || '',
      rank_classification: user.rank_classification || '',
      first_name: user.first_name || '',
      middle_name: user.middle_name || '',
      last_name: user.last_name || '',
      qualifier: user.qualifier || '',
      birthdate: user.birthdate || '',
      unit: user.unit || '',
      unit_other: user.unit_other || '',
      sex: user.sex || '',
      weight_kg: user.weight_kg || '',
      height_cm: user.height_cm || '',
      waist_cm: user.waist_cm || '',
      hip_cm: user.hip_cm || '',
      wrist_cm: user.wrist_cm || '',
    })
  }

  const handleChange = e => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleResetChange = e => {
    const { name, value } = e.target
    setResetForm(prev => ({ ...prev, [name]: value }))
  }

  const handleUpdate = async event => {
    event.preventDefault()
    if (!selected) return
    try {
      await updatePersonnel(selected.id, form, token)
      setStatus({ type: 'success', message: 'Personnel updated successfully.' })
      setSelected(null)
      loadPersonnel()
      loadHistory()
    } catch (error) {
      setStatus({ type: 'error', message: getErrorMessage(error, 'Could not update personnel.') })
    }
  }

  const handleResetSelect = user => {
    setResetUser(user)
    setResetForm({ password: '', confirm_password: '' })
  }

  const handleResetPassword = async event => {
    event.preventDefault()
    if (!resetUser) return
    try {
      const response = await resetPersonnelPassword(resetUser.id, resetForm, token)
      setStatus({ type: 'success', message: response.message })
      setResetUser(null)
      setResetForm({ password: '', confirm_password: '' })
      loadHistory()
    } catch (error) {
      setStatus({ type: 'error', message: getErrorMessage(error, 'Could not reset personnel password.') })
    }
  }

  const handleDelete = async id => {
    if (!window.confirm('Delete this personnel record?')) return
    try {
      await deletePersonnel(id, token)
      setStatus({ type: 'success', message: 'Personnel record deleted.' })
      if (selected && selected.id === id) setSelected(null)
      if (resetUser && resetUser.id === id) setResetUser(null)
      loadPersonnel()
      loadHistory()
    } catch (error) {
      setStatus({ type: 'error', message: getErrorMessage(error, 'Could not delete personnel.') })
    }
  }

  const handleExport = async () => {
    try {
      const blob = await exportPersonnel(token)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'bmi_reports.xlsx'
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      setStatus({ type: 'error', message: 'Export failed.' })
    }
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>Admin Dashboard</h2>
            <p>Welcome, {admin.first_name || admin.username}</p>
          </div>
          <button onClick={onLogout}>Logout</button>
        </div>
        <div style={{ marginTop: 12 }}>
          <button className="primary" onClick={handleExport}>Export Full BMI Reports</button>
        </div>
      </div>

      {status && <div className={`notice ${status.type}`}>{status.message}</div>}

      <div className="table-wrapper card" style={{ marginBottom: 24 }}>
        <table className="report-table">
          <thead>
            <tr>
              {reportColumns.map(column => (
                <th key={column.label}>{column.label}</th>
              ))}
              <th>ACTION</th>
            </tr>
          </thead>
          <tbody>
            {personnel.map(user => (
              <tr key={user.id}>
                {reportColumns.map(column => (
                  <td key={column.label} className={column.className || ''}>
                    {displayValue(column.value(user))}
                  </td>
                ))}
                <td>
                  <button onClick={() => handleSelect(user)}>Edit</button>
                  <button onClick={() => handleResetSelect(user)} style={{ marginLeft: 8 }}>Reset Password</button>
                  <button onClick={() => handleDelete(user.id)} style={{ marginLeft: 8 }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {resetUser && (
        <div className="card" style={{ marginBottom: 24 }}>
          <h3>Reset Personnel Password</h3>
          <p>{resetUser.rank} {resetUser.first_name} {resetUser.last_name} ({resetUser.username})</p>
          <form onSubmit={handleResetPassword}>
            <div className="grid">
              <div>
                <label>New Password</label>
                <input type="password" name="password" value={resetForm.password} onChange={handleResetChange} />
              </div>
              <div>
                <label>Confirm New Password</label>
                <input type="password" name="confirm_password" value={resetForm.confirm_password} onChange={handleResetChange} />
              </div>
            </div>
            <small>Min 8 chars, alphanumeric, 1 uppercase, 2 lowercase, at least 1 digit.</small>
            <div style={{ marginTop: 16 }}>
              <button className="primary" type="submit">Reset Password</button>
              <button type="button" onClick={() => setResetUser(null)} style={{ marginLeft: 12 }}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {selected && (
        <div className="card" style={{ marginBottom: 24 }}>
          <h3>Edit Personnel</h3>
          <form onSubmit={handleUpdate}>
            <div className="grid">
              <div>
                <label>Rank</label>
                <input name="rank" value={form.rank} onChange={handleChange} />
              </div>
              <div>
                <label>Rank Classification</label>
                <input name="rank_classification" value={form.rank_classification} onChange={handleChange} />
              </div>
              <div>
                <label>Last Name</label>
                <input name="last_name" value={form.last_name} onChange={handleChange} />
              </div>
              <div>
                <label>First Name</label>
                <input name="first_name" value={form.first_name} onChange={handleChange} />
              </div>
              <div>
                <label>Middle Name</label>
                <input name="middle_name" value={form.middle_name} onChange={handleChange} />
              </div>
              <div>
                <label>Qualifier</label>
                <input name="qualifier" value={form.qualifier} onChange={handleChange} />
              </div>
            </div>

            <div className="grid">
              <div>
                <label>Birthdate</label>
                <input type="date" name="birthdate" value={form.birthdate} onChange={handleChange} />
              </div>
              <div>
                <label>Unit</label>
                <input name="unit" value={form.unit} onChange={handleChange} />
              </div>
              <div>
                <label>Unit Other</label>
                <input name="unit_other" value={form.unit_other} onChange={handleChange} />
              </div>
              <div>
                <label>Sex</label>
                <input name="sex" value={form.sex} onChange={handleChange} />
              </div>
            </div>

            <div className="grid">
              <div>
                <label>Weight (kg)</label>
                <input name="weight_kg" type="number" step="0.1" value={form.weight_kg} onChange={handleChange} />
              </div>
              <div>
                <label>Height (cm)</label>
                <input name="height_cm" type="number" step="0.1" value={form.height_cm} onChange={handleChange} />
              </div>
              <div>
                <label>Waist (cm)</label>
                <input name="waist_cm" type="number" step="0.1" value={form.waist_cm} onChange={handleChange} />
              </div>
              <div>
                <label>Hip (cm)</label>
                <input name="hip_cm" type="number" step="0.1" value={form.hip_cm} onChange={handleChange} />
              </div>
              <div>
                <label>Wrist (cm)</label>
                <input name="wrist_cm" type="number" step="0.1" value={form.wrist_cm} onChange={handleChange} />
              </div>
            </div>

            <button className="primary" type="submit">Save Changes</button>
            <button type="button" onClick={() => setSelected(null)} style={{ marginLeft: 12 }}>Cancel</button>
          </form>
        </div>
      )}

      <div className="table-wrapper card">
        <h3>Access Log History</h3>
        <table className="history-table">
          <thead>
            <tr>
              <th>DATE/TIME</th>
              <th>USERNAME</th>
              <th>ACTION</th>
              <th>STATUS</th>
            </tr>
          </thead>
          <tbody>
            {history.map(item => (
              <tr key={item.id}>
                <td>{formatTimestamp(item.timestamp)}</td>
                <td>{displayValue(item.username)}</td>
                <td>{displayValue(item.action)}</td>
                <td>{item.success ? 'SUCCESS' : 'FAILED'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

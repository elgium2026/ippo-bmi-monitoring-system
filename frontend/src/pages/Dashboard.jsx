import { useState } from 'react'
import { computeBMI } from '../api.js'

export default function Dashboard({ user, token, onLogout, onUpdate }) {
  const [form, setForm] = useState({
    sex: user.sex || 'Male',
    weight_kg: user.weight_kg || '',
    height_cm: user.height_cm || '',
    waist_cm: user.waist_cm || '',
    hip_cm: user.hip_cm || '',
    wrist_cm: user.wrist_cm || '',
  })
  const [status, setStatus] = useState(null)

  const handleChange = e => {
    const value = e.target.value
    setForm(prev => ({ ...prev, [e.target.name]: value }))
  }

  const handleSubmit = async event => {
    event.preventDefault()
    try {
      const data = {
        sex: form.sex,
        weight_kg: form.weight_kg ? parseFloat(form.weight_kg) : null,
        height_cm: form.height_cm ? parseFloat(form.height_cm) : null,
        waist_cm: form.waist_cm ? parseFloat(form.waist_cm) : null,
        hip_cm: form.hip_cm ? parseFloat(form.hip_cm) : null,
        wrist_cm: form.wrist_cm ? parseFloat(form.wrist_cm) : null,
      }
      const response = await computeBMI(data, token)
      onUpdate(response)
      setStatus({ type: 'success', message: 'BMI computed successfully.' })
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Could not compute BMI.' })
    }
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>BMI Monitoring Dashboard</h2>
        <button onClick={onLogout}>Logout</button>
      </div>
      <p>Age: <strong>{user.age ?? 'N/A'}</strong></p>
      {status && <div className={`notice ${status.type}`}>{status.message}</div>}
      <form onSubmit={handleSubmit}>
        <div className="grid">
          <div>
            <label>Sex</label>
            <select name="sex" value={form.sex} onChange={handleChange}>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
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
        <button className="primary" type="submit">Compute</button>
      </form>

      <div style={{ marginTop: 24 }}>
        <h3>BMI Results</h3>
        <div className="result-card">
          <div>
            <strong>BMI</strong>
            <p>{user.bmi ?? '-'}</p>
          </div>
          <div>
            <strong>PNP Classification</strong>
            <p>{user.pnp_bmi_classification ?? '-'}</p>
          </div>
          <div>
            <strong>WHO Classification</strong>
            <p>{user.who_bmi_classification ?? '-'}</p>
          </div>
          <div>
            <strong>Weight to Lose (kg)</strong>
            <p>{user.weight_to_lose ?? '-'}</p>
          </div>
          <div>
            <strong>Maximum Normal Weight (kg)</strong>
            <p>{user.max_normal_weight ?? '-'}</p>
          </div>
        </div>
        {user.remarks && <div className="notice success" style={{ marginTop: 16 }}>{user.remarks}</div>}
      </div>
    </div>
  )
}

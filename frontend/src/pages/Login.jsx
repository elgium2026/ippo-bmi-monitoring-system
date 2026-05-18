import { useState } from 'react'
import { personnelLogin } from '../api.js'

export default function Login({ onLogin, onShowSignup, onShowAdmin }) {
  const [form, setForm] = useState({ username: '', password: '' })
  const [status, setStatus] = useState(null)

  const handleChange = e => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleSubmit = async event => {
    event.preventDefault()
    try {
      const data = await personnelLogin(form)
      setStatus({ type: 'success', message: 'Login successful.' })
      onLogin(data)
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Invalid credentials.' })
    }
  }

  return (
    <div className="card">
      <h2>Personnel Login</h2>
      {status && <div className={`notice ${status.type}`}>{status.message}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input name="username" value={form.username} onChange={handleChange} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} />
        </div>
        <button className="primary" type="submit">Login</button>
      </form>
      <div style={{ marginTop: 16 }}>
        <button onClick={onShowSignup}>Go to Signup</button>
        <button onClick={onShowAdmin}>Admin Login</button>
      </div>
    </div>
  )
}

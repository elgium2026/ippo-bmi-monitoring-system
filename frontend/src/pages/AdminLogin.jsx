import { useState } from 'react'
import { adminLogin, adminForgotPassword, adminVerifyOtp, adminChangePassword } from '../api.js'

export default function AdminLogin({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ username: '', password: '', confirm_password: '', otp: '' })
  const [adminToken, setAdminToken] = useState('')
  const [qrCode, setQrCode] = useState('')
  const [status, setStatus] = useState(null)

  const handleChange = e => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleLogin = async event => {
    event.preventDefault()
    try {
      const response = await adminLogin({ username: form.username, password: form.password })
      if (response.must_change_password) {
        setAdminToken(response.tokens.access)
        setMode('change-password')
        setStatus({ type: 'warning', message: 'First login requires password change.' })
        return
      }
      setStatus({ type: 'success', message: 'Admin login successful.' })
      onLogin(response)
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Invalid admin credentials.' })
    }
  }

  const handleForgot = async event => {
    event.preventDefault()
    try {
      const response = await adminForgotPassword({ username: form.username })
      setQrCode(response.qr_code_base64)
      setMode('verify')
      setStatus({ type: 'success', message: response.message })
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Could not process forgot password.' })
    }
  }

  const handleVerify = async event => {
    event.preventDefault()
    try {
      await adminVerifyOtp({ username: form.username, otp: form.otp, password: form.password, confirm_password: form.confirm_password })
      setStatus({ type: 'success', message: 'Password reset successfully. Please login with your new password.' })
      setMode('login')
      setForm(prev => ({ ...prev, password: '', confirm_password: '', otp: '' }))
      setQrCode('')
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Verification failed.' })
    }
  }

  const handleChangePassword = async event => {
    event.preventDefault()
    try {
      await adminChangePassword({ password: form.password, confirm_password: form.confirm_password }, adminToken)
      setStatus({ type: 'success', message: 'Password changed. Please login again.' })
      setMode('login')
      setAdminToken('')
    } catch (error) {
      setStatus({ type: 'error', message: error.detail || 'Could not change password.' })
    }
  }

  return (
    <div className="card">
      <h2>Admin Login</h2>
      {status && <div className={`notice ${status.type}`}>{status.message}</div>}
      {mode === 'login' && (
        <form onSubmit={handleLogin}>
          <div>
            <label>Username</label>
            <input name="username" value={form.username} onChange={handleChange} />
          </div>
          <div>
            <label>Password</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} />
          </div>
          <button className="primary" type="submit">Login</button>
          <button type="button" onClick={() => setMode('forgot')} style={{ marginLeft: 12 }}>Forgot Password</button>
        </form>
      )}

      {mode === 'forgot' && (
        <form onSubmit={handleForgot}>
          <div>
            <label>Admin Username</label>
            <input name="username" value={form.username} onChange={handleChange} />
          </div>
          <button className="primary" type="submit">Request QR Code</button>
          <button type="button" onClick={() => setMode('login')} style={{ marginLeft: 12 }}>Back</button>
        </form>
      )}

      {mode === 'verify' && (
        <form onSubmit={handleVerify}>
          <div>
            <label>Scan this QR code in Google Authenticator</label>
            {qrCode && <img src={qrCode} alt="QR Code" style={{ maxWidth: '240px', display: 'block', marginTop: 12 }} />}
          </div>
          <div>
            <label>One-Time Password</label>
            <input name="otp" value={form.otp} onChange={handleChange} />
          </div>
          <div>
            <label>New Password</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} />
          </div>
          <div>
            <label>Confirm Password</label>
            <input type="password" name="confirm_password" value={form.confirm_password} onChange={handleChange} />
          </div>
          <button className="primary" type="submit">Verify and Reset</button>
        </form>
      )}

      {mode === 'change-password' && (
        <form onSubmit={handleChangePassword}>
          <div>
            <label>New Password</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} />
          </div>
          <div>
            <label>Confirm Password</label>
            <input type="password" name="confirm_password" value={form.confirm_password} onChange={handleChange} />
          </div>
          <button className="primary" type="submit">Change Password</button>
        </form>
      )}
    </div>
  )
}

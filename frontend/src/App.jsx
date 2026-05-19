import { useEffect, useState } from 'react'
import Signup from './pages/Signup'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'

function App() {
  const storedPersonnel = JSON.parse(window.localStorage.getItem('personnel') || 'null')
  const storedPersonnelToken = window.localStorage.getItem('personnelToken') || ''
  const storedAdmin = JSON.parse(window.localStorage.getItem('admin') || 'null')
  const storedAdminToken = window.localStorage.getItem('adminToken') || ''

  const parseHash = () => {
    const hash = window.location.hash.replace('#/', '').replace('#', '')
    if (['login', 'signup', 'admin-login'].includes(hash)) {
      return hash
    }
    return null
  }

  const [view, setView] = useState(() => {
    if (storedPersonnel) return 'dashboard'
    if (storedAdmin) return 'admin-dashboard'
    return parseHash() || 'login'
  })
  const [personnel, setPersonnel] = useState(storedPersonnel)
  const [personnelToken, setPersonnelToken] = useState(storedPersonnelToken)
  const [admin, setAdmin] = useState(storedAdmin)
  const [adminToken, setAdminToken] = useState(storedAdminToken)

  useEffect(() => {
    if (personnel) {
      setView('dashboard')
      return
    }
    if (admin) {
      setView('admin-dashboard')
      return
    }

    const hashView = parseHash()
    if (hashView) {
      setView(hashView)
      return
    }

    if (!window.location.hash) {
      window.location.hash = '#/login'
    }
  }, [personnel, admin])

  useEffect(() => {
    if (!personnel && !admin && ['login', 'signup', 'admin-login'].includes(view)) {
      window.location.hash = `#/${view}`
    }
  }, [view, personnel, admin])

  useEffect(() => {
    const handleHashChange = () => {
      if (personnel || admin) return
      const hashView = parseHash()
      if (hashView) {
        setView(hashView)
      }
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [personnel, admin])

  const loginPersonnel = data => {
    setPersonnel(data.user)
    setPersonnelToken(data.tokens.access)
    window.localStorage.setItem('personnel', JSON.stringify(data.user))
    window.localStorage.setItem('personnelToken', data.tokens.access)
    setView('dashboard')
  }

  const loginAdmin = data => {
    setAdmin(data.user)
    setAdminToken(data.tokens.access)
    window.localStorage.setItem('admin', JSON.stringify(data.user))
    window.localStorage.setItem('adminToken', data.tokens.access)
    setView('admin-dashboard')
  }

  const logoutPersonnel = () => {
    setPersonnel(null)
    setPersonnelToken('')
    window.localStorage.removeItem('personnel')
    window.localStorage.removeItem('personnelToken')
    setView('login')
  }

  const logoutAdmin = () => {
    setAdmin(null)
    setAdminToken('')
    window.localStorage.removeItem('admin')
    window.localStorage.removeItem('adminToken')
    setView('admin-login')
  }

  const updatePersonnel = updated => {
    setPersonnel(updated)
    window.localStorage.setItem('personnel', JSON.stringify(updated))
  }

  return (
    <div className="app-container">
      <header>
        <h1>Ifugao PPO BMI Monitoring</h1>
      </header>

      {!personnel && !admin && (
        <div className="form-switcher">
          <button className={view === 'login' ? 'active' : ''} onClick={() => setView('login')}>
            Personnel Login
          </button>
          <button className={view === 'signup' ? 'active' : ''} onClick={() => setView('signup')}>
            Signup
          </button>
          <button className={view === 'admin-login' ? 'active' : ''} onClick={() => setView('admin-login')}>
            Admin Login
          </button>
        </div>
      )}

      {personnel && view === 'dashboard' && (
        <Dashboard user={personnel} token={personnelToken} onLogout={logoutPersonnel} onUpdate={updatePersonnel} />
      )}

      {admin && view === 'admin-dashboard' && (
        <AdminDashboard admin={admin} token={adminToken} onLogout={logoutAdmin} />
      )}

      {!personnel && !admin && view === 'signup' && <Signup onSignup={() => setView('login')} />}
      {!personnel && !admin && view === 'login' && <Login onLogin={loginPersonnel} onShowSignup={() => setView('signup')} onShowAdmin={() => setView('admin-login')} />}
      {!personnel && !admin && view === 'admin-login' && <AdminLogin onLogin={loginAdmin} />}
    </div>
  )
}

export default App

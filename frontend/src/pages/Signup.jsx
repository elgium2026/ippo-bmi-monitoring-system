import { useState } from 'react'
import { signup } from '../api.js'

const ranks = [
  'PBGEN', 'PCOL', 'PLTCOL', 'PMAJ', 'PCPT', 'PLT', 'PEMS', 'PCMS',
  'PSMS', 'PMSg', 'PSSg', 'PCpl', 'Pat', 'NUP',
]
const rankClassifications = ['PCO', 'PNCO', 'NUP']
const units = [
  'PHQ', '1st IPMFC', '2nd IPMFC', 'Aguinaldo MPS', 'Alfonso Lista MPS', 'Asipulo MPS',
  'Banaue MPS', 'Hingyon MPS', 'Hungduan MPS', 'Kiangan MPS', 'Lagawe MPS',
  'Lamut MPS', 'Mayoyao MPS', 'Tinoc MPS', 'Other Units (Please Specify)',
]

function uppercaseIfPco(value, classification) {
  return classification === 'PCO' ? value.toUpperCase() : value
}

export default function Signup({ onSignup }) {
  const [form, setForm] = useState({
    username: '',
    password: '',
    confirm_password: '',
    rank: 'PBGEN',
    rank_classification: 'PCO',
    first_name: '',
    middle_name: '',
    last_name: '',
    qualifier: '',
    birthdate: '',
    unit: 'PHQ',
    unit_other: '',
  })
  const [status, setStatus] = useState(null)

  const handleChange = e => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async event => {
    event.preventDefault()
    try {
      const requestData = {
        ...form,
        first_name: uppercaseIfPco(form.first_name, form.rank_classification),
        middle_name: uppercaseIfPco(form.middle_name, form.rank_classification),
        last_name: uppercaseIfPco(form.last_name, form.rank_classification),
        qualifier: uppercaseIfPco(form.qualifier, form.rank_classification),
      }
      await signup(requestData)
      setStatus({ type: 'success', message: 'Signup successful. You can now login.' })
      if (onSignup) {
        setTimeout(onSignup, 800)
      }
    } catch (error) {
      const message = error?.message || 'Could not complete signup.'
      setStatus({ type: 'error', message })
    }
  }

  return (
    <div className="card">
      <h2>Personnel Signup</h2>
      {status && <div className={`notice ${status.type}`}>{status.message}</div>}
      <form onSubmit={handleSubmit}>
        <div className="grid">
          <div>
            <label>Rank</label>
            <select name="rank" value={form.rank} onChange={handleChange}>
              {ranks.map(rank => <option key={rank} value={rank}>{rank}</option>)}
            </select>
          </div>
          <div>
            <label>Rank Classification</label>
            <select name="rank_classification" value={form.rank_classification} onChange={handleChange}>
              {rankClassifications.map(item => <option key={item} value={item}>{item}</option>)}
            </select>
          </div>
        </div>

        <div className="grid">
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
            <label>Username</label>
            <input name="username" value={form.username} onChange={handleChange} />
          </div>
        </div>

        <div className="grid">
          <div>
            <label>Password</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} />
            <small>Min 8 chars, alphanumeric, 1 uppercase, 2 lowercase, at least 1 digit.</small>
          </div>
          <div>
            <label>Confirm Password</label>
            <input type="password" name="confirm_password" value={form.confirm_password} onChange={handleChange} />
          </div>
        </div>

        <div>
          <label>Unit</label>
          <select name="unit" value={form.unit} onChange={handleChange}>
            {units.map(unit => <option key={unit} value={unit}>{unit}</option>)}
          </select>
        </div>
        {form.unit === 'Other Units (Please Specify)' && (
          <div>
            <label>Specify Unit</label>
            <input name="unit_other" value={form.unit_other} onChange={handleChange} />
          </div>
        )}

        <button className="primary" type="submit">Signup</button>
      </form>
    </div>
  )
}


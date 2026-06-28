import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiPost } from '../api'

export default function PatientRegister() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    full_name: '', age: 65, gender: 'female', education_years: 12,
    medical_history: '', family_history: '', medications: '',
  })
  const [error, setError] = useState('')

  function update(k, v) { setForm({ ...form, [k]: v }) }

  async function submit(e) {
    e.preventDefault()
    setError('')
    try {
      const p = await apiPost('/api/patients', {
        ...form,
        age: Number(form.age),
        education_years: Number(form.education_years),
      })
      navigate(`/patients/${p.id}/assess`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container">
      <h1>Patient Registration</h1>
      <div className="card">
        <form onSubmit={submit}>
          <label>Full name</label>
          <input value={form.full_name} onChange={(e) => update('full_name', e.target.value)} required />
          <div className="grid2">
            <div>
              <label>Age</label>
              <input type="number" value={form.age} onChange={(e) => update('age', e.target.value)} />
            </div>
            <div>
              <label>Gender</label>
              <select value={form.gender} onChange={(e) => update('gender', e.target.value)}>
                <option value="female">Female</option>
                <option value="male">Male</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
          <label>Education (years)</label>
          <input type="number" value={form.education_years} onChange={(e) => update('education_years', e.target.value)} />
          <label>Medical history</label>
          <textarea value={form.medical_history} onChange={(e) => update('medical_history', e.target.value)} />
          <label>Family history</label>
          <textarea value={form.family_history} onChange={(e) => update('family_history', e.target.value)} />
          <label>Medications</label>
          <textarea value={form.medications} onChange={(e) => update('medications', e.target.value)} />
          {error && <p className="error">{error}</p>}
          <button className="btn" type="submit">Save & Assess</button>
        </form>
      </div>
    </div>
  )
}

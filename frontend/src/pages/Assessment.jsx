import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { apiPost } from '../api'

const FIELDS = [
  ['mmse_score', 'MMSE (0-30)', 24],
  ['moca_score', 'MoCA (0-30)', 22],
  ['adl_score', 'ADL/IADL impairment (0-100)', 20],
  ['behaviour_score', 'Behaviour (0-100)', 20],
  ['language_score', 'Language (0-100)', 20],
  ['attention_score', 'Attention (0-100)', 20],
  ['executive_score', 'Executive function (0-100)', 20],
  ['mri_atrophy', 'MRI atrophy (0-1)', 0.2],
  ['voice_biomarker', 'Voice biomarker (0-1)', 0.2],
]

export default function Assessment() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState(
    Object.fromEntries(FIELDS.map(([k, , d]) => [k, d]))
  )
  const [error, setError] = useState('')

  function update(k, v) { setForm({ ...form, [k]: v }) }

  async function submit(e) {
    e.preventDefault()
    setError('')
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, Number(v)])
      )
      const a = await apiPost(`/api/patients/${id}/assessments`, payload)
      navigate(`/assessments/${a.id}`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container">
      <h1>Assessment Module</h1>
      <div className="card">
        <form onSubmit={submit}>
          <div className="grid2">
            {FIELDS.map(([k, label]) => (
              <div key={k}>
                <label>{label}</label>
                <input type="number" step="any" value={form[k]}
                  onChange={(e) => update(k, e.target.value)} />
              </div>
            ))}
          </div>
          {error && <p className="error">{error}</p>}
          <button className="btn" type="submit">Run Prediction</button>
        </form>
      </div>
    </div>
  )
}

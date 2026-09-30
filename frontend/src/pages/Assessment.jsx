import { useState, useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { apiPost, fetchPatientMRIs } from '../api'

const FIELDS = [
  ['mmse_score', 'MMSE Score (0-30)', 24],
  ['moca_score', 'MoCA Score (0-30)', 22],
  ['adl_score', 'ADL/IADL Impairment (0-100)', 20],
  ['behaviour_score', 'Behavioural Symptoms (0-100)', 20],
  ['language_score', 'Language Impairment (0-100)', 20],
  ['attention_score', 'Attention Deficit (0-100)', 20],
  ['executive_score', 'Executive Dysfunction (0-100)', 20],
  ['mri_atrophy', 'MRI Atrophy Ratio (0-1)', 0.25],
  ['voice_biomarker', 'Voice Biomarker (0-1)', 0.20],
]

export default function Assessment() {
  const { id } = useParams()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const queryMriId = searchParams.get('mri_id')

  const [form, setForm] = useState(
    Object.fromEntries(FIELDS.map(([k, , d]) => [k, d]))
  )
  const [mriScans, setMriScans] = useState([])
  const [selectedMriId, setSelectedMriId] = useState(queryMriId || '')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchPatientMRIs(id)
      .then(scans => {
        setMriScans(scans)
        if (queryMriId) {
          setSelectedMriId(queryMriId)
        } else if (scans.length > 0) {
          setSelectedMriId(scans[0].id)
        }
      })
      .catch(() => {})
  }, [id, queryMriId])

  function update(k, v) { setForm({ ...form, [k]: v }) }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, Number(v)])
      )
      if (selectedMriId) {
        payload.mri_scan_id = Number(selectedMriId)
      }
      const a = await apiPost(`/api/patients/${id}/assessments`, payload)
      navigate(`/assessments/${a.id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="container">
      <h1>Clinical Assessment & Multimodal Fusion</h1>
      <p className="subtitle">Integrate clinical cognitive scores with PyTorch Brain MRI Deep Learning Staging</p>
      
      <div className="card shadow-glow">
        <form onSubmit={submit}>
          <div className="form-group" style={{ marginBottom: 24 }}>
            <label>Link MRI Brain Scan (Optional - Fuses PyTorch Deep Learning Staging):</label>
            <select 
              value={selectedMriId} 
              onChange={(e) => setSelectedMriId(e.target.value)}
              className="input-select"
            >
              <option value="">-- No Attached MRI Scan --</option>
              {mriScans.map(scan => (
                <option key={scan.id} value={scan.id}>
                  Scan #{scan.id}: {scan.filename} ({scan.predicted_stage} - {scan.confidence_score}% Confidence)
                </option>
              ))}
            </select>
          </div>

          <div className="grid2">
            {FIELDS.map(([k, label]) => (
              <div key={k} className="form-group">
                <label>{label}</label>
                <input 
                  type="number" 
                  step="any" 
                  value={form[k]}
                  onChange={(e) => update(k, e.target.value)} 
                  className="input-field"
                />
              </div>
            ))}
          </div>

          {error && <div className="error-alert">{error}</div>}
          <button className="btn btn-primary btn-lg" type="submit" disabled={submitting}>
            {submitting ? 'Running Multimodal Prediction...' : '⚡ Run Integrated Prediction & SHAP Analysis'}
          </button>
        </form>
      </div>
    </div>
  )
}

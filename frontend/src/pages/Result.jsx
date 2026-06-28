import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { apiGet, reportUrl } from '../api'

export default function Result() {
  const { id } = useParams()
  const [a, setA] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGet(`/api/assessments/${id}`).then(setA).catch((e) => setError(e.message))
  }, [id])

  if (error) return <div className="container"><p className="error">{error}</p></div>
  if (!a) return <div className="container">Loading...</div>

  const probData = Object.entries(a.stage_probabilities || {})
    .map(([stage, p]) => ({ stage, prob: Math.round(p * 1000) / 10 }))
  const impData = Object.entries(a.feature_importance || {})
    .slice(0, 8)
    .map(([feature, v]) => ({ feature, value: Math.round(v * 1000) / 10 }))

  return (
    <div className="container">
      <h1>Prediction Result</h1>
      <div className="card">
        <p>Predicted stage: <span className={`stage-badge stage-${a.predicted_stage}`}>{a.predicted_stage}</span></p>
        <a className="btn" href={reportUrl(a.id)} target="_blank" rel="noreferrer">Download PDF Report</a>
      </div>

      <div className="card">
        <h3>Stage probabilities (%)</h3>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={probData}>
            <XAxis dataKey="stage" /><YAxis /><Tooltip />
            <Bar dataKey="prob" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3>Explainable AI - top feature importance (%)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={impData} layout="vertical">
            <XAxis type="number" /><YAxis type="category" dataKey="feature" width="120" /><Tooltip />
            <Bar dataKey="value" fill="#16a34a" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3>Recommendations</h3>
        <ul>
          {(a.recommendations || []).map((r, i) => <li key={i}>{r}</li>)}
        </ul>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { apiGet, reportUrl, BASE } from '../api'

const STAGE_COLORS = {
  'Non Demented': '#10b981',
  'Very Mild Demented': '#3b82f6',
  'Mild Demented': '#f59e0b',
  'Moderate Demented': '#ef4444'
}

export default function Result() {
  const { id } = useParams()
  const [a, setA] = useState(null)
  const [error, setError] = useState('')
  const [opacity, setOpacity] = useState(0.85)

  useEffect(() => {
    apiGet(`/api/assessments/${id}`).then(setA).catch((e) => setError(e.message))
  }, [id])

  if (error) return <div className="container"><div className="error-alert">{error}</div></div>
  if (!a) return <div className="container"><div className="card">Loading diagnosis result...</div></div>

  const probData = Object.entries(a.stage_probabilities || {})
    .map(([stage, p]) => ({ stage, prob: Math.round(p * 1000) / 10 }))

  const impData = Object.entries(a.feature_importance || {})
    .slice(0, 8)
    .map(([feature, v]) => ({ feature: feature.replace(/_/g, ' '), value: Math.round(v * 1000) / 10 }))

  return (
    <div className="container">
      <div className="header-flex">
        <div>
          <h1>Diagnostic Result & Clinical Decision Report</h1>
          <p className="subtitle">Assessment #{a.id} • Evaluated by {a.created_by || 'Doctor'}</p>
        </div>
        <a className="btn btn-primary btn-lg" href={reportUrl(a.id)} target="_blank" rel="noreferrer">
          📄 Download Full Clinical PDF Report
        </a>
      </div>

      <div className="card shadow-glow">
        <div className="result-banner">
          <div>
            <h3>Integrated Multimodal Alzheimer Stage Prediction</h3>
            <p>Combines Clinical Cognitive Scores (MMSE/ADL) + PyTorch Deep Learning Brain MRI Analysis</p>
          </div>
          <div className="stage-tag">
            <span className={`badge stage-${a.predicted_stage.replace(/\s+/g, '-').toLowerCase()}`}>
              {a.predicted_stage}
            </span>
          </div>
        </div>
      </div>

      {/* Embedded Brain MRI & SHAP Heatmap Viewer if available */}
      {a.mri_heatmap_url && (
        <div className="card shadow-glow">
          <h3>🧠 Explainable AI: SHAP / Grad-CAM Brain MRI Heatmap</h3>
          <p className="subtitle">Visual overlay highlighting brain tissue atrophy regions driving stage prediction</p>
          
          <div className="mri-visualizer-container" style={{ marginTop: 16 }}>
            <div className="visualizer-card">
              <h4>SHAP Visual Atrophy Heatmap Overlay</h4>
              <div className="img-wrapper relative" style={{ maxWidth: 360, margin: '0 auto' }}>
                <img 
                  src={`${BASE}${a.mri_heatmap_url}`} 
                  alt="SHAP Brain Heatmap" 
                  style={{ width: '100%', borderRadius: 12 }} 
                />
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid2">
        <div className="card shadow-glow">
          <h3>Stage Probabilities (%)</h3>
          <p className="subtitle">Deep Learning & Statistical Ensemble Distribution</p>
          <div style={{ width: '100%', height: 260, marginTop: 12 }}>
            <ResponsiveContainer>
              <BarChart data={probData}>
                <XAxis dataKey="stage" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
                <Bar dataKey="prob" radius={[6, 6, 0, 0]}>
                  {probData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={STAGE_COLORS[entry.stage] || '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card shadow-glow">
          <h3>Explainable AI - Feature Importance (%)</h3>
          <p className="subtitle">Top Clinical & MRI Features Contributing to Diagnosis</p>
          <div style={{ width: '100%', height: 260, marginTop: 12 }}>
            <ResponsiveContainer>
              <BarChart data={impData} layout="vertical">
                <XAxis type="number" stroke="#94a3b8" />
                <YAxis type="category" dataKey="feature" width={140} stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
                <Bar dataKey="value" fill="#10b981" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card shadow-glow" style={{ marginTop: 24 }}>
        <h3>Clinical Recommendations & Next Steps</h3>
        <ul className="recommendations-list">
          {(a.recommendations || []).map((r, i) => (
            <li key={i} className="rec-item">
              <span className="rec-bullet">✓</span>
              <span>{r}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { apiGet } from '../api'

export default function Records() {
  const { id } = useParams()
  const [items, setItems] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    apiGet(`/api/patients/${id}/assessments`).then(setItems).catch((e) => setError(e.message))
  }, [id])

  const progress = items.map((a, i) => ({
    n: i + 1,
    MMSE: a.mmse_score,
    MoCA: a.moca_score,
    ADL: a.adl_score,
  }))

  return (
    <div className="container">
      <h1>Previous Records</h1>
      {error && <p className="error">{error}</p>}

      <div className="card">
        <h3>Progress graph</h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={progress}>
            <XAxis dataKey="n" /><YAxis /><Tooltip /><Legend />
            <Line dataKey="MMSE" stroke="#2563eb" />
            <Line dataKey="MoCA" stroke="#16a34a" />
            <Line dataKey="ADL" stroke="#dc2626" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3>History</h3>
        <table>
          <thead><tr><th>#</th><th>MMSE</th><th>MoCA</th><th>Stage</th><th></th></tr></thead>
          <tbody>
            {items.map((a, i) => (
              <tr key={a.id}>
                <td>{i + 1}</td>
                <td>{a.mmse_score}</td>
                <td>{a.moca_score}</td>
                <td><span className={`stage-badge stage-${a.predicted_stage}`}>{a.predicted_stage}</span></td>
                <td><Link to={`/assessments/${a.id}`}>View</Link></td>
              </tr>
            ))}
            {items.length === 0 && <tr><td colSpan="5">No records yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

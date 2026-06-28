import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGet } from '../api'

export default function Patients() {
  const [patients, setPatients] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    apiGet('/api/patients').then(setPatients).catch((e) => setError(e.message))
  }, [])

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Patients</h1>
        <Link className="btn" to="/patients/new">+ Register Patient</Link>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="card">
        <table>
          <thead>
            <tr><th>Name</th><th>Age</th><th>Gender</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id}>
                <td>{p.full_name}</td>
                <td>{p.age}</td>
                <td>{p.gender}</td>
                <td>
                  <Link to={`/patients/${p.id}/assess`}>Assess</Link>{' | '}
                  <Link to={`/patients/${p.id}/records`}>Records</Link>
                </td>
              </tr>
            ))}
            {patients.length === 0 && (
              <tr><td colSpan="4">No patients yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

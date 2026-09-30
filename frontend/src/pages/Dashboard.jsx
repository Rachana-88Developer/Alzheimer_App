import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth.jsx'
import { fetchPatients } from '../api.js'

export default function Dashboard() {
  const { user } = useAuth()
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchPatients()
        setPatients(data || [])
      } catch (err) {
        console.error('Failed to load dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const totalPatients = patients.length
  const highRiskCount = patients.filter(p => p.stage === 'Mild Demented' || p.stage === 'Moderate Demented').length
  const mciCount = patients.filter(p => p.stage === 'Very Mild Demented').length

  return (
    <div className="container">
      {/* Doctor Welcome Header */}
      <div className="doctor-header">
        <div className="doctor-welcome">
          <h1>Welcome, Dr. {user?.username ? user.username.toUpperCase() : 'Doctor'} 👋</h1>
          <p>Alzheimer's Clinical Decision Support Dashboard | Active Clinical Session</p>
        </div>
        <div>
          <Link to="/patients" className="btn">+ Add New Patient</Link>
        </div>
      </div>

      {/* Stats Metric Cards */}
      <div className="stats-row">
        <div className="stat-card">
          <span className="stat-label">Total Registered Patients</span>
          <span className="stat-value">{loading ? '...' : totalPatients}</span>
          <span className="stat-desc">Active in database</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">High Risk Cases</span>
          <span className="stat-value" style={{ color: '#dc2626' }}>{loading ? '...' : highRiskCount}</span>
          <span className="stat-desc" style={{ color: '#dc2626' }}>Mild / Moderate Staging</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">MCI Patients</span>
          <span className="stat-value" style={{ color: '#ca8a04' }}>{loading ? '...' : mciCount}</span>
          <span className="stat-desc" style={{ color: '#ca8a04' }}>Very Mild Demented</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">System AI Status</span>
          <span className="stat-value" style={{ color: '#16a34a', fontSize: '20px', marginTop: '12px' }}>● Ready</span>
          <span className="stat-desc">PyTorch / SHAP Enabled</span>
        </div>
      </div>

      {/* Quick Action Navigation Tiles */}
      <div className="dashboard-actions">
        <Link to="/patients" className="action-tile">
          <div className="action-icon">👥</div>
          <div className="action-info">
            <h4>Patient Directory</h4>
            <p>View, manage, and register new patients</p>
          </div>
        </Link>
        <Link to="/mri" className="action-tile">
          <div className="action-icon">🧠</div>
          <div className="action-info">
            <h4>MRI Brain Scan Staging</h4>
            <p>Upload scans & run PyTorch Deep Learning Staging</p>
          </div>
        </Link>
        <Link to="/records" className="action-tile">
          <div className="action-icon">📄</div>
          <div className="action-info">
            <h4>Clinical PDF Reports</h4>
            <p>View past reports & longitudinal history</p>
          </div>
        </Link>
      </div>

      {/* Recent Patients Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ margin: 0, color: '#0f172a' }}>Recent Patient Activity</h3>
          <Link to="/patients" style={{ fontSize: 13, fontWeight: 600 }}>View All Patients →</Link>
        </div>

        {loading ? (
          <p style={{ color: '#64748b' }}>Loading recent patient records...</p>
        ) : patients.length === 0 ? (
          <p style={{ color: '#64748b' }}>No patients registered yet. Click "+ Add New Patient" above to get started.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>MMSE Score</th>
                <th>Current Staging</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {patients.slice(0, 5).map((p) => (
                <tr key={p.id}>
                  <td><strong>#{p.id}</strong></td>
                  <td>{p.first_name} {p.last_name}</td>
                  <td>{p.age || '68'}</td>
                  <td>{p.mmse_score ? `${p.mmse_score}/30` : 'Pending'}</td>
                  <td>
                    <span className={`stage-badge stage-${(p.stage || 'normal').toLowerCase().includes('very mild') ? 'mci' : (p.stage || 'normal').toLowerCase().includes('mild') ? 'mild' : (p.stage || 'normal').toLowerCase().includes('moderate') ? 'moderate' : 'normal'}`}>
                      {p.stage || 'Non-Demented'}
                    </span>
                  </td>
                  <td>
                    <Link to="/patients" className="btn btn-secondary" style={{ padding: '4px 10px', fontSize: 12 }}>View Record</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

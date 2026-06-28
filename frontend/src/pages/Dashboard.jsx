import { Link } from 'react-router-dom'

export default function Dashboard() {
  return (
    <div className="container">
      <h1>Dashboard</h1>
      <div className="dashboard-grid">
        <Link className="tile" to="/patients">Patient Management</Link>
        <Link className="tile" to="/patients">Assessment Module</Link>
        <Link className="tile" to="/patients">Previous Records</Link>
      </div>
    </div>
  )
}

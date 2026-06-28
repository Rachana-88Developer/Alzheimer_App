import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { useAuth } from './auth.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Patients from './pages/Patients.jsx'
import PatientRegister from './pages/PatientRegister.jsx'
import Assessment from './pages/Assessment.jsx'
import Result from './pages/Result.jsx'
import Records from './pages/Records.jsx'

function Protected({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}

function Navbar() {
  const { user, signOut } = useAuth()
  if (!user) return null
  return (
    <div className="navbar">
      <div>
        <Link to="/">Dashboard</Link>
        <Link to="/patients">Patients</Link>
      </div>
      <div>
        <span style={{ marginRight: 16 }}>{user.username} ({user.role})</span>
        <button className="btn btn-secondary" onClick={signOut}>Logout</button>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Protected><Dashboard /></Protected>} />
        <Route path="/patients" element={<Protected><Patients /></Protected>} />
        <Route path="/patients/new" element={<Protected><PatientRegister /></Protected>} />
        <Route path="/patients/:id/assess" element={<Protected><Assessment /></Protected>} />
        <Route path="/patients/:id/records" element={<Protected><Records /></Protected>} />
        <Route path="/assessments/:id" element={<Protected><Result /></Protected>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}

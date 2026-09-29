import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth.jsx'

export default function Login() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('doctor')
  const [password, setPassword] = useState('doctor123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await signIn(username, password)
      navigate('/')
    } catch (err) {
      setError(err.message || 'Authentication failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-header">
          <h2>🧠 Alzheimer's CDSS</h2>
          <p>Clinical Decision Support Portal</p>
        </div>
        <form onSubmit={submit}>
          <label>Username / Doctor ID</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            required
          />
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            required
          />
          {error && <div className="error">{error}</div>}
          <button className="btn" type="submit" disabled={loading} style={{ width: '100%', marginTop: 8 }}>
            {loading ? 'Authenticating...' : 'Sign In to Portal'}
          </button>
        </form>

        <div style={{ marginTop: 24, padding: '12px 14px', background: '#f8fafc', borderRadius: 8, border: '1px solid #e2e8f0', fontSize: 13 }}>
          <strong style={{ display: 'block', color: '#0f172a', marginBottom: 4 }}>Demo Credentials:</strong>
          <div style={{ color: '#64748b' }}>👨‍⚕️ Doctor: <code>doctor</code> / <code>doctor123</code></div>
          <div style={{ color: '#64748b' }}>🔑 Admin: <code>admin</code> / <code>admin123</code></div>
        </div>
      </div>
    </div>
  )
}

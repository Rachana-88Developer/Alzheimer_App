import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth.jsx'

export default function Login() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('doctor')
  const [password, setPassword] = useState('doctor123')
  const [error, setError] = useState('')

  async function submit(e) {
    e.preventDefault()
    setError('')
    try {
      await signIn(username, password)
      navigate('/')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="login-wrap">
      <div className="card">
        <h2>Alzheimer's CDSS Login</h2>
        <form onSubmit={submit}>
          <label>Username</label>
          <input value={username} onChange={(e) => setUsername(e.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {error && <p className="error">{error}</p>}
          <button className="btn" type="submit">Sign in</button>
        </form>
        <p style={{ fontSize: 12, color: '#6b7280', marginTop: 16 }}>
          Demo: admin/admin123, doctor/doctor123, staff/staff123
        </p>
      </div>
    </div>
  )
}

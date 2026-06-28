import { createContext, useContext, useState } from 'react'
import { login as apiLogin } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  })

  async function signIn(username, password) {
    const data = await apiLogin(username, password)
    localStorage.setItem('token', data.access_token)
    const u = { username: data.username, role: data.role }
    localStorage.setItem('user', JSON.stringify(u))
    setUser(u)
    return u
  }

  function signOut() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

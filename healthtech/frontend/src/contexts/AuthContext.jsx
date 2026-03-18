import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api/axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchProfile = useCallback(async () => {
    try {
      const { data } = await api.get('/auth/profile/')
      setUser(data)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) fetchProfile()
    else setLoading(false)
  }, [fetchProfile])

  const login = async (email, password) => {
    const { data } = await api.post('/auth/login/', { email, password })
    localStorage.setItem('access_token', data.tokens.access)
    localStorage.setItem('refresh_token', data.tokens.refresh)
    setUser(data.user)
    return data.user
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout/', { refresh: localStorage.getItem('refresh_token') })
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, fetchProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)

import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import PatientDashboard from './pages/PatientDashboard'
import DoctorDashboard from './pages/DoctorDashboard'
import AppointmentBooking from './pages/AppointmentBooking'
import AppointmentList from './pages/AppointmentList'
import MedicalRecords from './pages/MedicalRecords'
import SymptomChecker from './pages/SymptomChecker'
import TelemedicineRoom from './pages/TelemedicineRoom'
import AdminDashboard from './pages/AdminDashboard'

function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="flex items-center justify-center h-screen"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to="/dashboard" replace />
  return children
}

function DashboardRedirect() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (user.role === 'doctor' || user.role === 'nurse') return <Navigate to="/doctor-dashboard" replace />
  if (user.role === 'admin') return <Navigate to="/admin-dashboard" replace />
  return <Navigate to="/patient-dashboard" replace />
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardRedirect /></ProtectedRoute>} />
          <Route path="/patient-dashboard" element={<ProtectedRoute roles={['patient']}><PatientDashboard /></ProtectedRoute>} />
          <Route path="/doctor-dashboard" element={<ProtectedRoute roles={['doctor', 'nurse']}><DoctorDashboard /></ProtectedRoute>} />
          <Route path="/admin-dashboard" element={<ProtectedRoute roles={['admin']}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/appointments" element={<ProtectedRoute><AppointmentList /></ProtectedRoute>} />
          <Route path="/appointments/book" element={<ProtectedRoute roles={['patient']}><AppointmentBooking /></ProtectedRoute>} />
          <Route path="/medical-records" element={<ProtectedRoute><MedicalRecords /></ProtectedRoute>} />
          <Route path="/symptom-checker" element={<ProtectedRoute roles={['patient']}><SymptomChecker /></ProtectedRoute>} />
          <Route path="/telemedicine/:sessionId" element={<ProtectedRoute><TelemedicineRoom /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

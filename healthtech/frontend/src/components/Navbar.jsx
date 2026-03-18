import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import NotificationBell from './NotificationBell'
import { Bars3Icon, XMarkIcon, UserCircleIcon } from '@heroicons/react/24/outline'

const NAV_LINKS = {
  patient: [
    { label: 'Dashboard', to: '/patient-dashboard' },
    { label: 'Book Appointment', to: '/appointments/book' },
    { label: 'My Appointments', to: '/appointments' },
    { label: 'Medical Records', to: '/medical-records' },
    { label: 'Symptom Checker', to: '/symptom-checker' },
  ],
  doctor: [
    { label: 'Dashboard', to: '/doctor-dashboard' },
    { label: 'Appointments', to: '/appointments' },
    { label: 'Medical Records', to: '/medical-records' },
  ],
  nurse: [
    { label: 'Dashboard', to: '/doctor-dashboard' },
    { label: 'Appointments', to: '/appointments' },
  ],
  admin: [
    { label: 'Dashboard', to: '/admin-dashboard' },
    { label: 'Appointments', to: '/appointments' },
    { label: 'Medical Records', to: '/medical-records' },
  ],
}

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)

  const links = user ? (NAV_LINKS[user.role] || []) : []

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-8">
            <Link to="/dashboard" className="text-xl font-bold text-primary-600">
              🏥 HealthTech
            </Link>
            <div className="hidden md:flex gap-4">
              {links.map((l) => (
                <Link key={l.to} to={l.to} className="text-gray-600 hover:text-primary-600 text-sm font-medium transition-colors">
                  {l.label}
                </Link>
              ))}
            </div>
          </div>
          {user && (
            <div className="flex items-center gap-3">
              <NotificationBell />
              <div className="flex items-center gap-2 text-sm text-gray-700">
                <UserCircleIcon className="h-6 w-6 text-gray-400" />
                <span className="hidden md:block">{user.first_name} {user.last_name}</span>
                <span className="hidden md:block px-2 py-0.5 bg-primary-50 text-primary-700 rounded-full text-xs capitalize">{user.role}</span>
              </div>
              <button onClick={handleLogout} className="text-sm text-red-600 hover:text-red-800 font-medium">
                Logout
              </button>
              <button className="md:hidden" onClick={() => setMobileOpen(!mobileOpen)}>
                {mobileOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
              </button>
            </div>
          )}
        </div>
      </div>
      {mobileOpen && (
        <div className="md:hidden px-4 pb-4 flex flex-col gap-2">
          {links.map((l) => (
            <Link key={l.to} to={l.to} onClick={() => setMobileOpen(false)} className="text-gray-700 py-2 border-b border-gray-100 text-sm">
              {l.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}

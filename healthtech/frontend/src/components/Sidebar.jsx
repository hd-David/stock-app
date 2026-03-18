import React from 'react'
import { NavLink } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import {
  HomeIcon, CalendarIcon, DocumentTextIcon,
  HeartIcon, VideoCameraIcon, ChartBarIcon,
} from '@heroicons/react/24/outline'

const MENUS = {
  patient: [
    { label: 'Dashboard', to: '/patient-dashboard', icon: HomeIcon },
    { label: 'Book Appointment', to: '/appointments/book', icon: CalendarIcon },
    { label: 'My Appointments', to: '/appointments', icon: CalendarIcon },
    { label: 'Medical Records', to: '/medical-records', icon: DocumentTextIcon },
    { label: 'Symptom Checker', to: '/symptom-checker', icon: HeartIcon },
  ],
  doctor: [
    { label: 'Dashboard', to: '/doctor-dashboard', icon: HomeIcon },
    { label: 'Appointments', to: '/appointments', icon: CalendarIcon },
    { label: 'Medical Records', to: '/medical-records', icon: DocumentTextIcon },
    { label: 'Telemedicine', to: '/telemedicine', icon: VideoCameraIcon },
  ],
  admin: [
    { label: 'Dashboard', to: '/admin-dashboard', icon: ChartBarIcon },
    { label: 'Appointments', to: '/appointments', icon: CalendarIcon },
    { label: 'Records', to: '/medical-records', icon: DocumentTextIcon },
  ],
}

export default function Sidebar() {
  const { user } = useAuth()
  const items = user ? (MENUS[user.role] || MENUS.patient) : []

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen p-4">
      <nav className="flex flex-col gap-1">
        {items.map(({ label, to, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <Icon className="h-5 w-5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

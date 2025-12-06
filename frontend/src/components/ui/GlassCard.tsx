import React from 'react'

interface GlassCardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
}

export const GlassCard: React.FC<GlassCardProps> = ({ children, className = '', onClick }) => {
  return (
    <div
      className={`glass rounded-lg p-6 hover-glow transition-all duration-300 ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  )
}


import React from 'react'

interface NeonInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

export const NeonInput: React.FC<NeonInputProps> = ({ label, className = '', ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-neon-blue mb-2">
          {label}
        </label>
      )}
      <input
        className={`
          w-full px-4 py-2 bg-dark-bg-secondary/50 border border-neon-blue/30
          rounded-lg text-white placeholder-gray-500
          focus:outline-none focus:border-neon-blue focus:shadow-neon-sm
          transition-all duration-300
          ${className}
        `}
        {...props}
      />
    </div>
  )
}


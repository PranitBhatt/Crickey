import React from 'react'

interface NeonButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  children: React.ReactNode
}

export const NeonButton: React.FC<NeonButtonProps> = ({
  variant = 'primary',
  children,
  className = '',
  ...props
}) => {
  const variantClasses = {
    primary: 'bg-neon-blue/20 border-neon-blue text-neon-blue hover:bg-neon-blue/30',
    secondary: 'bg-dark-bg-tertiary border-neon-blue/50 text-neon-blue hover:border-neon-blue',
    danger: 'bg-red-500/20 border-red-500 text-red-400 hover:bg-red-500/30',
  }

  return (
    <button
      className={`
        ${variantClasses[variant]}
        px-6 py-2 rounded-lg border-2 font-semibold
        transition-all duration-300 hover-glow
        disabled:opacity-50 disabled:cursor-not-allowed
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  )
}


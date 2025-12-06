/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          blue: '#00b7ff',
          'blue-light': '#3ae7ff',
          'blue-dark': '#0099cc',
        },
        dark: {
          bg: '#000000',
          'bg-secondary': '#0a0a0a',
          'bg-tertiary': '#1a1a1a',
        }
      },
      boxShadow: {
        'neon': '0 0 10px #00b7ff, 0 0 20px #00b7ff, 0 0 30px #00b7ff',
        'neon-sm': '0 0 5px #00b7ff, 0 0 10px #00b7ff',
        'neon-lg': '0 0 20px #00b7ff, 0 0 40px #00b7ff, 0 0 60px #00b7ff',
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
        'pulse-neon': 'pulse-neon 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00b7ff, 0 0 10px #00b7ff' },
          '100%': { boxShadow: '0 0 20px #00b7ff, 0 0 40px #00b7ff, 0 0 60px #00b7ff' },
        },
        'pulse-neon': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        },
      },
    },
  },
  plugins: [],
}


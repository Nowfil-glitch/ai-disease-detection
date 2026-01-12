import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        // Echo Labs color palette - Deep Blue to Cyan gradient theme
        echo: {
          // Primary gradient colors
          'navy': '#020344',
          'navy-light': '#0a0d5c',
          'cyan': '#28B8D5',
          'cyan-light': '#5fd4eb',
          'cyan-pale': '#a0e8f5',
          // Supporting colors
          'blue-mid': '#1a5a8a',
          'blue-accent': '#1e90c8',
          // Legacy colors (keeping for compatibility)
          crimson: '#c4343c',
          pink: '#e10878',
          // Neutrals
          white: '#ffffff',
          'gray-light': '#f2f2f2',
          'gray-mid': '#8a9bae',
          'gray-dark': '#4a5568',
          'gray-darker': '#2d3748',
          charcoal: '#1a202c',
          black: '#020344',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient-shift': 'gradient-shift 8s ease infinite',
        'slide-up': 'slide-up 0.5s ease-out',
        'slide-down': 'slide-down 0.5s ease-out',
        'fade-in': 'fade-in 0.6s ease-out',
        'scale-in': 'scale-in 0.4s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'gradient-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'slide-up': {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-down': {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'scale-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(196, 52, 60, 0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(196, 52, 60, 0.6)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      backgroundImage: {
        'echo-gradient': 'linear-gradient(90deg, #020344 0%, #28B8D5 100%)',
        'echo-gradient-135': 'linear-gradient(135deg, #020344 0%, #28B8D5 100%)',
        'echo-gradient-soft': 'linear-gradient(90deg, #0a0d5c 0%, #5fd4eb 100%)',
        'echo-radial': 'radial-gradient(circle at center, #28B8D5 0%, #020344 70%)',
        'echo-gradient-vertical': 'linear-gradient(180deg, #020344 0%, #28B8D5 100%)',
      },
    },
  },
  plugins: [],
}
export default config

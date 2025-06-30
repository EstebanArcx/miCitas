/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/templates/**/*.html", "./src/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        primary: '#18b2a1',
        'primary-hover': '#0fa192',
        accent: '#b2e5df',
        'accent-bg': '#65cbc0',
        'accent-hover': '#4dbcb0',
        'accent-form': '#95e9e09a',
      },
      animation: {
        'breathing-lg': 'breathing-lg 10s ease-in-out infinite',
        'breathing-md': 'breathing-md 8s ease-in-out infinite',
        'breathing-sm': 'breathing-sm 6s ease-in-out infinite',
        'slide-mensajes': 'slide-mensajes 10s ease-in-out infinite',
      },
      keyframes: {
        'breathing-lg': {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.1' },
          '50%': { transform: 'scale(1.4)', opacity: '0.3' },
        },
        'breathing-md': {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.1' },
          '50%': { transform: 'scale(1.25)', opacity: '0.25' },
        },
        'breathing-sm': {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.1' },
          '50%': { transform: 'scale(1.15)', opacity: '0.2' },
        },
        'slide-mensajes': {
        '0%, 25%': { transform: 'translateY(0)' },
        '50%, 75%': { transform: 'translateY(-10rem)' },
        '100%': { transform: 'translateY(0)' },
      },

        },
    },
  },
  plugins: [],
}



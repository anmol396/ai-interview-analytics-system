/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        panel: '#1e293b',
        borderDark: '#334155',
        accent: {
          500: '#8b5cf6', 
          600: '#7c3aed',
        }
      }
    },
  },
  plugins: [],
}

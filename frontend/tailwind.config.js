/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',    
        panel: '#1e293b',   
        primary: '#38bdf8', 
        danger: '#ef4444',  
        warning: '#f59e0b', 
      }
    },
  },
  plugins: [],
}
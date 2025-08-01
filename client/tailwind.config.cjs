/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#816a71',
          muted: '#f6eef1'
        },
        neutral: '#191516'
      }
    },
  },
  plugins: [],
};
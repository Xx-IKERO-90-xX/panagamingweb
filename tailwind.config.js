/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./static/estilo/**/*.{css}", 
    "./templates/**/*.{jinja}", 
    "/static/scripts/**/*.{js}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}


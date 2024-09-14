/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/estilo/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}


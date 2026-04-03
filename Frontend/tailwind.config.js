/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#af101a',
        secondary: '#4c56af',
        tertiary: '#2153ad',
        surface: '#f8f9fa',
        'on-surface': '#191c1d',
        'on-surface-variant': '#5b403d',
        'surface-container-low': '#f3f4f5',
        'surface-container-high': '#e7e8e9',
        'surface-container-highest': '#e1e3e4',
        'surface-container-lowest': '#ffffff',
        'on-primary': '#ffffff',
        'secondary-container': '#959efd',
        'on-secondary-container': '#27308a',
        'outline-variant': '#e4beba',
        // Agrega aquí cualquier otro color del JSON que necesites
      },
      fontFamily: {
        headline: ['Manrope', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        xl: '0.5rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
        full: '9999px',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};

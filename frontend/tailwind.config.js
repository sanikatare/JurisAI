/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        juris: {
          dark: '#000000',
          card: '#0A0A0A',
          surface: '#111111',
          surfaceLight: '#171717',
          surfaceBorder: '#1F1F1F',
          
          bg: '#FFFFFF',
          bgSecondary: '#FAFAF9',
          bgMuted: '#F7F7F5',
          
          border: '#E7E7E5',
          borderDark: '#DADAD7',
          
          textPrimary: '#111111',
          textBody: '#333333',
          textMuted: '#666666',
          textSubtle: '#8A8A8A',
          
          riskLow: '#15803D',
          riskLowBg: '#F0FDF4',
          riskLowBorder: '#BBF7D0',
          
          riskMod: '#B45309',
          riskModBg: '#FFFBEB',
          riskModBorder: '#FDE68A',
          
          riskHigh: '#B91C1C',
          riskHighBg: '#FEF2F2',
          riskHighBorder: '#FECACA',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'Cambria', 'Times New Roman', 'Times', 'serif'],
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px 0 rgba(0, 0, 0, 0.02)',
        'elevated': '0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02)',
        'dropdown': '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
      }
    },
  },
  plugins: [],
}

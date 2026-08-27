
module.exports = {
  content: ["./index.html"],
  safelist: [
    'bg-blue-600', 'hover:bg-blue-700', 'bg-green-600', 'hover:bg-green-700',
    'bg-blue-500', 'hover:bg-blue-500', 'text-blue-400', 'text-blue-300',
    'text-gray-400', 'text-white', 'tag', 'interactive-card', 'glass-effect',
    'reveal-element', 'visible'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#3b82f6'
        }
      }
    },
  },
  plugins: [],
}

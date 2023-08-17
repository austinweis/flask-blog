/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./awblog/templates/*.html"],
  theme: {
    extend : {
      fontFamily: {
        primary: "Pixel",
      },
      fontSize: {
        none: ['0px', '0px'],
      },
      transitionTimingFunction: {
        'in-expo': 'cubic-bezier(0.95, 0.05, 0.795, 0.035)',
        'out-expo': 'cubic-bezier(0.19, 1, 0.22, 1)',
      },
    },
    screens: {
      sm: '640px',
      // => @media (min-width: 640px) { ... }
  
      md: '768px',
      // => @media (min-width: 768px) { ... }
  
      lg: '1024px',
      // => @media (min-width: 1024px) { ... }
  
      xl: '1280px',
      // => @media (min-width: 1280px) { ... }
  
      '2xl': '1536px',
      // => @media (min-width: 1536px) { ... }
    },
  },
  plugins: [],
}


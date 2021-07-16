module.exports = {
  purge: {
    // enabled: process.env.debug === 'false', // TODO Uncomment this line
    enabled: true, // TODO Comment This line
    preserveHtmlElements: false,
    content: [
      "../homepage/templates/**/*.html",
      "../userprofiles/templates/**/*.html",
      "../products/templates/**/*.html",
      "../templates/base.html",
      "../static/script.js",
    ],

    options: {
      keyframes: true,
    },
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        brand: ['"Nunito Sans"', "sans-serif"],
      },
    },
  },
  variants: {
    extend: {
      borderWidth: ["hover"],
    },
  },
  plugins: [],
};

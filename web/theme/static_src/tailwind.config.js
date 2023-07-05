/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: [
    "../../templates/**/*.html",
    "../../templates/**/**/*.html",
    "../../static/js/*.js",
  ],

  theme: {
    extend: {
      backgroundColor: {
        primary: "#025464",
        secondary: "#F8F1F1",
        third: "#454545",
        forth: "#026443",
        headline: "#232323",
        paragraph: "#222525",
        dark: "#232323",
        light: "#fffffe",
      },
      colors: {
        primary: "#025464",
        secondary: "#F8F1F1",
        third: "#454545",
        forth: "#026443",
        headline: "#232323",
        paragraph: "#222525",
        dark: "#232323",
        light: "#fffffe",
      },
      borderColor: {
        primary: "#025464",
        secondary: "#F8F1F1",
        third: "#454545",
        forth: "#026443",
        headline: "#232323",
        paragraph: "#222525",
        dark: "#232323",
        light: "#fffffe",
      },
      width: {
        content: "fit-content",
        xs: "450px",
        s: "550px",
        sm: "600px",
        md: "700px",
        lg: "800px",
      },
      height: {
        content: "fit-content",
        120: "450px",
        screen: "calc(100vh - 82px)",
        "screen-admin": "calc(100vh - 106px)",
      },
      minHeight: {
        body: "calc(100vh - 48px)",
        600: "600px",
        screen: "calc(100vh - 82px)",
        "screen-admin": "calc(100vh - 106px)",
      },
      maxWidth: {
        100: "100%",
        800: "800px",
        900: "900px",
        1000: "1000px",
        1920: "1920px",
        1300: "1300px",
        1400: "1400px",
        1440: "1440px",
        1600: "1600px",
        1800: "1700px",
        "1/2": "50%",
      },
      maxHeight: {
        100: "100%",
        600: "600px",
      },
      fontFamily: {
        work: ["Work Sans", "sans", "arial"],
        poppins: ["Poppins", "sans"],
      },
      screens: {
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1536px",
        "3xl": "1950px",
      },
      lineHeight: {
        90: "90px",
      },
      fontSize: {
        ss: ["8px", "12px"],
      },
      gridTemplateColumns: {
        alerts: "15% 15% 15% 15% 12% 11% 11% 6%",
        alerts_mobile: "200px 200px 200px 200px 200px 200px 200px 80px",

        ads: "30% 20% 20% 20% 10%",
        ads_mobile: "200px 200px 200px 200px 150px",
      },
      boxShadow: {
        card: "rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;",
        cardHover: "rgba(0, 0, 0, 0.35) 0px 5px 15px;",
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};

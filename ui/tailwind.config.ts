import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Identité France Air
        marine: "#2f4a6f",
        rouge: "#d62828",
        electrique: "#00a8e8",
        teal: "#00b4a0",
        encre: "#0a0e1a",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      keyframes: {
        float: {
          "0%,100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-22px)" },
        },
        fadein: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        float: "float 9s ease-in-out infinite",
        fadein: "fadein .5s ease-out both",
      },
    },
  },
  plugins: [],
} satisfies Config;

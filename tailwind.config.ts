import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        cyber: {
          dark: {
            DEFAULT: "var(--cyber-dark-500)",
            50: "var(--cyber-dark-50)",
            100: "var(--cyber-dark-100)",
            200: "var(--cyber-dark-200)",
            300: "var(--cyber-dark-300)",
            400: "var(--cyber-dark-400)",
            500: "var(--cyber-dark-500)",
            600: "var(--cyber-dark-600)",
            700: "var(--cyber-dark-700)",
            800: "var(--cyber-dark-800)",
            900: "var(--cyber-dark-900)",
            950: "var(--cyber-dark-950)",
          },
          purple: {
            DEFAULT: "var(--cyber-purple-500)",
            50: "var(--cyber-purple-50)",
            100: "var(--cyber-purple-100)",
            200: "var(--cyber-purple-200)",
            300: "var(--cyber-purple-300)",
            400: "var(--cyber-purple-400)",
            500: "var(--cyber-purple-500)",
            600: "var(--cyber-purple-600)",
            700: "var(--cyber-purple-700)",
            800: "var(--cyber-purple-800)",
            900: "var(--cyber-purple-900)",
            950: "var(--cyber-purple-950)",
          },
          pink: {
            DEFAULT: "var(--cyber-pink-500)",
            50: "var(--cyber-pink-50)",
            100: "var(--cyber-pink-100)",
            200: "var(--cyber-pink-200)",
            300: "var(--cyber-pink-300)",
            400: "var(--cyber-pink-400)",
            500: "var(--cyber-pink-500)",
            600: "var(--cyber-pink-600)",
            700: "var(--cyber-pink-700)",
            800: "var(--cyber-pink-800)",
            900: "var(--cyber-pink-900)",
            950: "var(--cyber-pink-950)",
          },
          cyan: {
            DEFAULT: "var(--cyber-cyan-500)",
            50: "var(--cyber-cyan-50)",
            100: "var(--cyber-cyan-100)",
            200: "var(--cyber-cyan-200)",
            300: "var(--cyber-cyan-300)",
            400: "var(--cyber-cyan-400)",
            500: "var(--cyber-cyan-500)",
            600: "var(--cyber-cyan-600)",
            700: "var(--cyber-cyan-700)",
            800: "var(--cyber-cyan-800)",
            900: "var(--cyber-cyan-900)",
            950: "var(--cyber-cyan-950)",
          },
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        "neon-flicker": {
          "0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100%": { opacity: "1" },
          "20%, 21.999%, 63%, 63.999%, 65%, 69.999%": { opacity: "0.4" },
        },
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "glow-pulse": "glow-pulse 2s infinite ease-in-out",
        "neon-flicker": "neon-flicker 2s infinite linear",
      },
      boxShadow: {
        "neon-purple": "0 0 5px theme('colors.cyber.purple.500'), 0 0 20px theme('colors.cyber.purple.500')",
        "neon-pink": "0 0 5px theme('colors.cyber.pink.500'), 0 0 20px theme('colors.cyber.pink.500')",
        "neon-cyan": "0 0 5px theme('colors.cyber.cyan.500'), 0 0 20px theme('colors.cyber.cyan.500')",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;

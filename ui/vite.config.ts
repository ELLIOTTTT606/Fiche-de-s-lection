import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En dev, l'API tourne sur :8000 ; on proxifie /api vers le backend.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
  build: {
    outDir: "dist",
  },
});

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  if (mode === "widget") {
    // Build configuration for embeddable widget
    return {
      plugins: [react()],
      build: {
        lib: {
          entry: "src/widget.jsx",
          name: "MongoDBChatWidget",
          fileName: "mongodb-chat-widget",
          formats: ["umd"],
        },
        rollupOptions: {
          external: [],
          output: {
            globals: {},
          },
        },
      },
      define: {
        "process.env.NODE_ENV": '"production"',
      },
    };
  }

  // Development configuration
  return {
    plugins: [react()],
    server: {
      port: 3000,
      cors: true,
    },
  };
});

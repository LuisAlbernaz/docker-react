import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { nodePolyfills } from 'vite-plugin-node-polyfills';

export default defineConfig({
  plugins: [
    vue(),
    nodePolyfills({
      // Especifica os polyfills necessários
      globals: {
        crypto: true,
      },
    }),
  ],
  server: {
    host: '0.0.0.0',
    port: 8080,
    allowedHosts: [
      'frontend',      // Permite o host "frontend"
      'localhost',     // Permite o host "localhost"
    ],
  },
  resolve: {
    alias: {
      crypto: 'crypto-browserify',
      stream: 'stream-browserify',
    },
  },
});
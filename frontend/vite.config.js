import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// 替换为你的WSL IP地址
const WSL_IP = '172.29.223.73'  // 使用实际的IP地址

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: `http://${WSL_IP}:8000`,
        changeOrigin: true
      }
    }
  }
}) 
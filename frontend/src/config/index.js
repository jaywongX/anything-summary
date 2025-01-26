export const config = {
  // 是否使用模拟服务
  useMockService: import.meta.env.VITE_USE_MOCK === 'true',
  // API基础URL
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api'
}; 
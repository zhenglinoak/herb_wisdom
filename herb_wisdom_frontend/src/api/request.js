import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const service = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
})

service.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response) => {
    const data = response.data
    if (data.code === 200) {
      if (data.data?.token) {
        sessionStorage.setItem('token', data.data.token)
      }
      return data
    } else {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
  },
  (error) => {
    if (error.response?.status === 401) {
      sessionStorage.clear()
      ElMessage.error('登录过期，请重新登录')
      router.replace('/login')
    } else if (error.message === 'Network Error') {
      ElMessage.error('网络错误，请检查网络连接')
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请稍后重试')
    } else {
      ElMessage.error(error.response?.data?.msg || '请求失败，请稍后重试')
    }
    return Promise.reject(error)
  }
)

export default service
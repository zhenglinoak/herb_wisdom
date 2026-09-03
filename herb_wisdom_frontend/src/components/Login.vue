<template>
  <div class="login-page">
    <div class="bg-decoration">
      <div class="bg-leaf bg-leaf-1">
        <svg viewBox="0 0 200 200" width="200" height="200" fill="none" stroke="currentColor" stroke-width="1"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M100 20 C 50 50, 40 100, 100 180 C 160 100, 150 50, 100 20 Z" fill="rgba(74,124,89,0.04)" />
          <line x1="100" y1="40" x2="100" y2="180" stroke-width="0.8" />
          <path d="M100 70 Q 70 80, 55 100" stroke-width="0.8" />
          <path d="M100 70 Q 130 80, 145 100" stroke-width="0.8" />
          <path d="M100 100 Q 75 105, 62 120" stroke-width="0.8" />
          <path d="M100 100 Q 125 105, 138 120" stroke-width="0.8" />
        </svg>
      </div>
      <div class="bg-leaf bg-leaf-2">
        <svg viewBox="0 0 200 200" width="160" height="160" fill="none" stroke="currentColor" stroke-width="1"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M100 20 C 50 50, 40 100, 100 180 C 160 100, 150 50, 100 20 Z" fill="rgba(139,111,71,0.03)" />
          <line x1="100" y1="40" x2="100" y2="180" stroke-width="0.8" />
        </svg>
      </div>
    </div>

    <div class="auth-card" style="width: 400px;">
      <div class="brand-header">
        <div class="brand-logo">
          <svg viewBox="0 0 32 32" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 4 C 10 8, 8 14, 16 28 C 24 14, 22 8, 16 4 Z" fill="rgba(74,124,89,0.1)" />
            <line x1="16" y1="8" x2="16" y2="28" stroke-width="1" />
            <path d="M16 14 Q 12 16, 10 20" stroke-width="1" />
            <path d="M16 14 Q 20 16, 22 20" stroke-width="1" />
          </svg>
        </div>
        <h1>本草智典</h1>
        <p class="brand-tagline">HERBAL WISDOM</p>
      </div>

      <div class="tabs">
        <div class="tab-item" :class="{ active: loginType === 'password' }" @click="loginType = 'password'">
          账号密码登录
        </div>
        <div class="tab-item" :class="{ active: loginType === 'email' }" @click="loginType = 'email'">
          邮箱登录
        </div>
      </div>

      <div v-if="loginType === 'email'" class="form-container">
        <div class="form-item">
          <label>邮箱</label>
          <input type="text" v-model="email" :disabled="isSent" placeholder="请输入邮箱">
        </div>

        <div class="form-item">
          <label>验证码</label>
          <input type="text" v-model="code" :disabled="!isSent" placeholder="请输入验证码">
        </div>

        <button v-if="!isVerifying" class="btn-primary" type="button" @click="sendCode" :disabled="!email">
          发送验证码
        </button>

        <button v-else class="btn-primary" type="button" @click="verifyCode" :disabled="!code">
          验证登录
        </button>
      </div>

      <div v-else class="form-container">
        <div class="form-item">
          <label>账号</label>
          <input type="text" v-model="userName" placeholder="请输入账号或邮箱">
        </div>

        <div class="form-item">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请输入密码">
        </div>

        <button class="btn-primary" type="button" @click="passwordLogin" :disabled="!userName || !password">
          登录
        </button>
      </div>

      <div class="footer-link">
        还没有账号？<span @click="goToRegister">立即注册</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const router = useRouter()
const loginType = ref('password')
const email = ref('')
const code = ref('')
const userName = ref('zz')
const password = ref('123')
const isSent = ref(false)
const isVerifying = ref(false)

async function sendCode() {
  if (!email.value) {
    ElMessage.error('邮箱不能为空')
    return
  }

  try {
    const res = await request({
      url: '/user/sendEmailCode',
      method: 'get',
      params: { email: email.value }
    })
    ElMessage.success(res.msg)
    isSent.value = true
    isVerifying.value = true
  } catch (e) {
    console.error(e)
  }
}

async function verifyCode() {
  if (!code.value) {
    ElMessage.error('验证码不能为空')
    return
  }

  try {
    const res = await request({
      url: '/user/verifyCode',
      method: 'get',
      params: { email: email.value, code: code.value }
    })
    ElMessage.success(res.msg)
    sessionStorage.setItem('userName', res.data.user_name)
    setTimeout(() => {
      router.push('/chat')
    }, 1500)
  } catch (e) {
    console.error(e)
  }
}

async function passwordLogin() {
  if (!userName.value) {
    ElMessage.error('账号不能为空')
    return
  }
  if (!password.value) {
    ElMessage.error('密码不能为空')
    return
  }

  try {
    const res = await request({
      url: '/user/login',
      method: 'post',
      data: {
        s: userName.value,
        password: password.value
      }
    })
    ElMessage.success('登录成功')
    sessionStorage.setItem('userName', res.data.user_name)
    setTimeout(() => {
      router.push('/chat')
    }, 1500)
  } catch (e) {
    console.error(e)
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-card {
  width: 400px;
}
</style>
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

    <div class="auth-card" style="width: 460px;">
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

      <el-form ref="registerFormRef" :model="registerForm" :rules="rules" class="form-container" @submit.prevent>
        <el-form-item prop="userName">
          <label>用户名</label>
          <el-input v-model="registerForm.userName" placeholder="请输入用户名" :prefix-icon="User" />
        </el-form-item>

        <el-form-item prop="email">
          <label>邮箱</label>
          <el-input v-model="registerForm.email" placeholder="请输入邮箱" :prefix-icon="Message" />
        </el-form-item>

        <el-form-item prop="password">
          <label>密码</label>
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" show-password
            :prefix-icon="Lock" />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <label>确认密码</label>
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password
            :prefix-icon="Lock" />
        </el-form-item>

        <el-form-item>
          <button class="btn-primary" type="button" @click="handleRegister">
            注册
          </button>
        </el-form-item>
      </el-form>

      <div class="footer-link">
        已有账号？<span @click="goToLogin">去登录</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Message, Lock } from '@element-plus/icons-vue'
import request from '@/api/request'

const router = useRouter()
const registerFormRef = ref()

const registerForm = reactive({
  userName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  userName: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const goToLogin = () => {
  router.push('/login')
}

const handleRegister = () => {
  registerFormRef.value.validate(async (valid) => {
    if (!valid) {
      return false
    }

    try {
      await request({
        url: '/user/register',
        method: 'post',
        data: {
          user_name: registerForm.userName,
          email: registerForm.email,
          password: registerForm.password
        }
      })
      ElMessage.success('注册成功，请登录')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } catch (e) {
      console.error(e)
    }
  })
}
</script>

<style scoped>
.form-container :deep(.el-form-item) {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
}

.form-container :deep(.el-form-item__error) {
  padding-top: 2px;
  font-size: 12px;
}

.form-container :deep(.el-form-item__content) {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  line-height: normal;
  flex-wrap: wrap;
}

.form-container label {
  display: inline-block;
  width: 80px;
  flex-shrink: 0;
  margin-bottom: 0;
  color: var(--ink-black);
  font-size: 14px;
  font-weight: 500;
  line-height: 42px;
}

.form-container :deep(.el-input) {
  flex: 1;
}

.form-container :deep(.el-input__wrapper) {
  width: 100%;
  height: 42px;
  padding: 0 14px;
  box-sizing: border-box;
  border: 1px solid var(--border-warm);
  border-radius: 8px;
  outline: none;
  font-size: 14px;
  transition: all 0.3s;
  background: var(--rice-paper-light);
  color: var(--ink-black);
  font-family: inherit;
  box-shadow: none;
}

.form-container :deep(.el-input__wrapper.is-focus) {
  border-color: var(--herbal-green);
  box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.1);
  background: #fff;
}

.form-container :deep(.el-input__inner) {
  color: var(--ink-black);
}

.form-container :deep(.el-input__inner::placeholder) {
  color: var(--ink-muted);
}

.form-container :deep(.el-form-item:last-of-type .el-form-item__content) {
  display: block;
}

.btn-primary {
  margin-top: 6px;
}
</style>
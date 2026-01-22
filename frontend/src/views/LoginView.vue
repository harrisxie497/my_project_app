<template>
  <div class="login-wrap">
    <div class="login-card">
      <div class="login-left">
        <div class="brand">
          <div class="brand-badge"></div>
          <div>
            <div class="brand-title">日本清关/派送 Excel 自动处理系统</div>
            <div class="muted" style="color: rgba(255,255,255,.85); font-size: 12px;">Vue3 + Element Plus</div>
          </div>
        </div>
        <div style="margin-top: 18px;">
          <h1>一站式上传 → 修复/补齐 → 下载</h1>
          <p>支持清关文件 / 派送文件 · 规则驱动 · AI 字段补齐 · 输出对比与统计</p>
        </div>
      </div>
      <div class="login-right">
        <div class="section-title">登录</div>
        <el-form label-position="top">
          <el-form-item label="账号">
            <el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="loginForm.password" placeholder="请输入密码" show-password></el-input>
          </el-form-item>
          <el-button type="primary" style="width: 100%;" @click="doLogin" :loading="loading">登录</el-button>
          <div class="footer-note">登录后可访问任务中心；管理员可进入配置中心。</div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import authService from '../services/authService'

const router = useRouter()
const loading = ref(false)

const loginForm = reactive({ username: "admin", password: "admin123" })

const doLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.error("请输入账号密码")
    return
  }
  
  loading.value = true
  
  try {
    // 调用真实登录API
    console.log("开始登录，账号:", loginForm.username)
    const response = await authService.login(loginForm.username, loginForm.password)
    console.log("登录响应:", response)
    
    if (response && response.data) {
      // 保存认证信息到本地存储
      authService.saveAuth({
        loggedIn: true,
        token: response.data.access_token,
        user: response.data.user
      })
      
      ElMessage.success("登录成功")
      router.push('/tasks')
    } else {
      console.error("登录响应数据格式错误:", response)
      ElMessage.error("登录失败，响应格式错误")
    }
  } catch (error) {
    console.error("登录错误:", error)
    let errorMessage = "登录失败，请稍后重试"
    
    // 解析错误响应，获取详细错误信息
    if (error.response) {
      console.error("错误详情:", error.response)
      if (error.response.data && error.response.data.detail) {
        // 根据后端返回的错误信息显示不同的提示
        const detail = error.response.data.detail
        if (detail === "User does not exist") {
          errorMessage = "用户不存在"
        } else if (detail === "User account is disabled") {
          errorMessage = "用户账号已被禁用"
        } else if (detail === "Incorrect password") {
          errorMessage = "密码错误"
        } else {
          errorMessage = detail
        }
      } else if (error.response.status === 401) {
        errorMessage = "用户名或密码错误"
      }
    } else if (error.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap { height: 100vh; display:flex; align-items:center; justify-content:center; padding: 16px; }
.login-card { width: 980px; max-width: 100%; display:grid; grid-template-columns: 1.2fr 0.8fr; overflow:hidden; border-radius: 18px; border: 1px solid #eaecef; background:#fff; }
.login-left { padding: 28px; background: linear-gradient(135deg, #2f54eb 0%, #1f1f1f 120%); color: #fff; }
.login-left h1 { margin: 0 0 6px; font-size: 22px; }
.login-left p { margin: 0; opacity: .9; }
.login-right { padding: 28px; }
.brand { display:flex; align-items:center; gap:10px; }
.brand-badge { width: 28px; height: 28px; border-radius: 10px; background: #2f54eb; }
.brand-title { font-weight: 700; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.muted { color:#6b7280; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
.danger-box { border: 1px dashed #f56c6c; padding: 10px; border-radius: 12px; background: #fff5f5; color: #b42318; }
@media (max-width: 980px) {
  .login-card { grid-template-columns: 1fr; }
}
</style>
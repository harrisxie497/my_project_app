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
        <div style="margin-top: 18px;" class="danger-box">
          提示：该页面无真实后端，仅用于确认页面结构与交互流程。
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
          <el-button type="primary" style="width: 100%;" @click="doLogin">登录</el-button>
          <div class="footer-note">登录后可访问任务中心；管理员可进入配置中心。</div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const loginForm = reactive({ username: "admin", password: "123456" })

const doLogin = () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.error("请输入账号密码")
    return
  }
  
  // 模拟登录成功，存储用户信息到本地存储
  const user = {
    id: "u_123",
    username: loginForm.username,
    display_name: loginForm.username === "admin" ? "Admin" : "Operator",
    role: loginForm.username === "admin" ? "admin" : "operator"
  }
  
  localStorage.setItem('auth', JSON.stringify({
    loggedIn: true,
    token: "mock-jwt",
    user
  }))
  
  ElMessage.success("登录成功")
  router.push('/tasks')
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
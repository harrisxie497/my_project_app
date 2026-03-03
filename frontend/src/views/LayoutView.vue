<template>
  <div class="app-shell">
    <div class="topbar">
      <div class="brand">
        <div class="brand-badge"></div>
        <div>
          <div class="brand-title">日本清关/派送 Excel 自动处理系统</div>
          <div class="muted" style="font-size: 12px;">
            当前用户：<span class="mono">{{ getUsername() }}</span> · 角色：<span class="mono">{{ getRole() }}</span>
          </div>
        </div>
      </div>
      <div style="display:flex; gap: 8px; align-items:center;">
        <el-button @click="$router.push('/tasks')">任务中心</el-button>
        <el-button type="danger" plain @click="doLogout">退出</el-button>
      </div>
    </div>

    <div class="content">
      <div class="sidebar" :class="{ 'collapsed': sidebarCollapsed }">
        <div class="sidebar-header">
          <el-button 
            type="text" 
            @click="toggleSidebar" 
            style="padding: 8px; font-size: 16px; color: #6b7280;">
            {{ sidebarCollapsed ? '>>' : '<<' }}
          </el-button>
        </div>
        <el-menu 
          :default-active="activeRoute" 
          @select="handleMenuSelect" 
          style="border-right: none;"
          :collapse="sidebarCollapsed"
        >
          <el-menu-item v-for="m in menuItems" :key="m.key" :index="m.key">
            <template #icon>
              <span>{{ m.icon }}</span>
            </template>
            <template #title>
              <span>{{ m.label }}</span>
            </template>
          </el-menu-item>
        </el-menu>
        <div class="footer-note" v-if="!sidebarCollapsed">
          侧边栏随角色变化。下载不做额外鉴权（仅登录）。
        </div>
      </div>

      <div class="main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

// 侧边栏折叠状态
const sidebarCollapsed = ref(false)

// 切换侧边栏折叠状态
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const auth = ref({
  loggedIn: false,
  token: "",
  user: { id: "", username: "", display_name: "", role: "operator" }
})

// 安全地获取用户名
const getUsername = () => {
  try {
    return auth.value?.user?.username || "未知用户"
  } catch (e) {
    return "未知用户"
  }
}

// 安全地获取角色
const getRole = () => {
  try {
    return auth.value?.user?.role || "operator"
  } catch (e) {
    return "operator"
  }
}

const activeRoute = computed(() => {
  const path = route.path
  if (path === '/tasks') return 'tasks'
  if (path === '/task-detail/:id') return 'task_detail'
  if (path === '/admin/users') return 'admin_users'
  if (path === '/admin/logs') return 'admin_logs'
  if (path === '/admin/file-definitions') return 'admin_file_definitions'
  if (path === '/admin/field-pipelines') return 'admin_field_pipelines'
  if (path === '/admin/rule-definitions') return 'admin_rule_definitions'
  return 'tasks'
})

const menuItems = computed(() => {
  const base = [
    { key: 'tasks', label: '任务中心', icon: '📄', path: '/tasks' }
  ]
  if (auth.value.user.role === "admin") {
    base.push(
      { key: 'admin_file_definitions', label: '文件定义配置', icon: '📋', path: '/admin/file-definitions' },
      { key: 'admin_field_pipelines', label: '字段映射配置', icon: '🔄', path: '/admin/field-pipelines' },
      { key: 'admin_rule_definitions', label: '字段规则配置', icon: '📏', path: '/admin/rule-definitions' },
      { key: 'admin_users', label: '用户管理', icon: '👤', path: '/admin/users' },
      { key: 'admin_logs', label: '操作日志', icon: '🧾', path: '/admin/logs' }
    )
  }
  return base
})

const handleMenuSelect = (key) => {
  const menuItem = menuItems.value.find(item => item.key === key)
  if (menuItem) {
    router.push(menuItem.path)
  }
}

const doLogout = () => {
  localStorage.removeItem('auth')
  auth.value.loggedIn = false
  ElMessage.success("退出成功")
  router.push('/login')
}

const checkAuth = () => {
  const authStr = localStorage.getItem('auth')
  if (authStr) {
    try {
      const authData = JSON.parse(authStr)
      // 确保 authData 有 user 字段
      if (authData && authData.user) {
        auth.value = authData
        return true
      } else {
        // 数据格式不正确，清除并返回 false
        localStorage.removeItem('auth')
        return false
      }
    } catch (e) {
      localStorage.removeItem('auth')
      return false
    }
  }
  return false
}

onMounted(() => {
  if (!checkAuth()) {
    router.push('/login')
  }
})
</script>

<style scoped>
.app-shell { height: 100vh; display: flex; flex-direction: column; }
.topbar { display:flex; align-items:center; justify-content:space-between; padding: 12px 16px; background:#ffffff; border-bottom: 1px solid #eaecef; }
.brand { display:flex; align-items:center; gap:10px; }
.brand-badge { width: 28px; height: 28px; border-radius: 10px; background: #2f54eb; }
.brand-title { font-weight: 700; }
.content { flex: 1; display:flex; min-height: 0; }
.sidebar { width: 240px; background:#fff; border-right:1px solid #eaecef; padding: 10px; transition: width 0.3s ease; }
.sidebar.collapsed { width: 80px; }
.sidebar-header { display: flex; justify-content: flex-end; margin-bottom: 10px; }
.main { flex: 1; padding: 16px; overflow:auto; background: #f6f7fb; }
.muted { color:#6b7280; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
@media (max-width: 980px) {
  .sidebar { display:none; }
}
</style>
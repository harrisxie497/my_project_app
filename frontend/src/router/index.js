import { createRouter, createWebHistory } from 'vue-router'

// 导入页面组件
import LoginView from '../views/LoginView.vue'
import LayoutView from '../views/LayoutView.vue'
import TaskListView from '../views/TaskListView.vue'
import TaskDetailView from '../views/TaskDetailView.vue'
import UserManagementView from '../views/admin/UserManagementView.vue'
import OperationLogView from '../views/admin/OperationLogView.vue'
import FileDefinitionsView from '../views/admin/FileDefinitionsView.vue'
import FieldPipelinesView from '../views/admin/FieldPipelinesView.vue'
import RuleDefinitionsView from '../views/admin/RuleDefinitionsView.vue'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/tasks'
  },
  {
    path: '/tasks',
    component: LayoutView,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'tasks',
        component: TaskListView
      },
      {
        path: '/task-detail/:id',
        name: 'task-detail',
        component: TaskDetailView
      }
    ]
  },
  {
    path: '/admin',
    component: LayoutView,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'users',
        name: 'admin-users',
        component: UserManagementView
      },
      {
        path: 'logs',
        name: 'admin-logs',
        component: OperationLogView
      },
      {
        path: 'file-definitions',
        name: 'admin-file-definitions',
        component: FileDefinitionsView
      },
      {
        path: 'field-pipelines',
        name: 'admin-field-pipelines',
        component: FieldPipelinesView
      },
      {
        path: 'rule-definitions',
        name: 'admin-rule-definitions',
        component: RuleDefinitionsView
      }
    ]
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStr = localStorage.getItem('auth')
  let auth = {
    loggedIn: false,
    token: '',
    user: { role: 'operator' }
  }
  
  if (authStr) {
    try {
      auth = JSON.parse(authStr)
    } catch (e) {
      localStorage.removeItem('auth')
    }
  }
  
  // 不需要认证的页面
  if (!to.meta.requiresAuth) {
    next()
    return
  }
  
  // 需要认证的页面
  if (!auth.loggedIn) {
    next('/login')
    return
  }
  
  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && auth.user.role !== 'admin') {
    next('/tasks')
    return
  }
  
  next()
})

export default router
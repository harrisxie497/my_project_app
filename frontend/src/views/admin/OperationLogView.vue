<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">操作日志</div>
        <div class="muted">登录 / 创建任务 / 成功失败 / 配置变更</div>
      </div>
    </div>
    <div class="card-bd">
      <el-table :data="logs" style="width:100%;" :loading="loading">
        <el-table-column prop="created_at" label="time" width="200">
          <template #default="{row}">
            <span>{{ formatDateTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="user_id" label="user" width="120"></el-table-column>
        <el-table-column prop="action" label="action" width="180"></el-table-column>
        <el-table-column prop="entity_type" label="entity type" width="120"></el-table-column>
        <el-table-column prop="entity_id" label="entity id" width="160"></el-table-column>
        <el-table-column prop="success" label="success" width="120">
          <template #default="{row}">
            <el-tag v-if="row.success" type="success">true</el-tag>
            <el-tag v-else type="danger">false</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="message"></el-table-column>
      </el-table>
      <div class="footer-note">
        一期建议：日志只读；二期可增加筛选与导出。
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import operationLogService from '../../services/operationLogService'

const logs = ref([])
const loading = ref(false)

// 格式化日期时间
const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 加载操作日志
const loadLogs = async () => {
  loading.value = true
  try {
    // 调用API获取操作日志
    const response = await operationLogService.adminGetOperationLogs()
    logs.value = response.data.items
  } catch (error) {
    console.error('获取操作日志失败:', error)
    ElMessage.error('获取操作日志失败')
    logs.value = []
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载日志
onMounted(() => {
  loadLogs()
})
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
</style>
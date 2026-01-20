<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">操作日志</div>
        <div class="muted">登录 / 创建任务 / 成功失败 / 配置变更</div>
      </div>
    </div>
    <div class="card-bd">
      <el-table :data="logs" style="width:100%;">
        <el-table-column prop="created_at" label="time" width="200"></el-table-column>
        <el-table-column prop="user" label="user" width="120"></el-table-column>
        <el-table-column prop="action" label="action" width="180"></el-table-column>
        <el-table-column prop="entity" label="entity" width="160"></el-table-column>
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
import { ref } from 'vue'

const logs = ref([
  { id: "log_1", created_at: "2026-01-20T01:02:03Z", user: "admin", action: "TASK_CREATED", entity: "task:t_001", success: true, message: "created" },
  { id: "log_2", created_at: "2026-01-20T01:02:20Z", user: "admin", action: "TASK_SUCCEEDED", entity: "task:t_001", success: true, message: "success" },
  { id: "log_3", created_at: "2026-01-20T02:10:11Z", user: "op1", action: "TASK_FAILED", entity: "task:t_002", success: false, message: "RULE_VALIDATION_FAILED" },
]);
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
</style>
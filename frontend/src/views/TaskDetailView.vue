<template>
  <div class="split">
    <div class="card">
      <div class="card-hd">
        <div>
          <div class="section-title">任务详情</div>
          <div class="muted">任务ID：<span class="mono">{{taskDetail.id}}</span></div>
        </div>
        <div style="display:flex; gap:8px;">
          <el-button @click="$router.push('/tasks')">返回列表</el-button>
          <el-button type="primary" :disabled="taskDetail.status==='processing'" @click="runTask">运行任务</el-button>
        </div>
      </div>

      <div class="card-bd">
        <div style="display:flex; gap:10px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="tag-pill">类型：{{taskDetail.file_type==='customs'?'清关':'派送'}}</span>
          <span class="tag-pill">唯一编码：<span class="mono">{{taskDetail.unique_code}}</span></span>
          <span v-if="taskDetail.file_type==='customs'" class="tag-pill">航空号：<span class="mono">{{taskDetail.flight_no}}</span></span>
          <span v-if="taskDetail.file_type==='customs'" class="tag-pill">报关日期：<span class="mono">{{taskDetail.declare_date}}</span></span>
          <span class="tag-pill">状态：
            <el-tag v-if="taskDetail.status==='success'" type="success">success</el-tag>
            <el-tag v-else-if="taskDetail.status==='failed'" type="danger">failed</el-tag>
            <el-tag v-else-if="taskDetail.status==='processing'" type="warning">processing</el-tag>
            <el-tag v-else>queued</el-tag>
          </span>
        </div>

        <el-divider />

        <div style="display:flex; gap:8px; flex-wrap: wrap;">
          <el-button @click="downloadFile('original')">下载原始文件</el-button>
          <el-button type="primary" @click="downloadFile('result')" :disabled="taskDetail.status!=='success'">下载结果文件</el-button>
          <el-button @click="downloadFile('diff')" :disabled="taskDetail.status!=='success'">下载对比文件</el-button>
        </div>
        <div class="footer-note">
          一期：下载不做额外鉴权（仅登录即可）。处理失败时不提供结果/对比。
        </div>

        <el-divider />

        <div v-if="taskDetail.status==='success'">
          <div class="section-title" style="margin-bottom: 8px;">变化统计</div>
          <div class="kpi">
            <div class="box"><div class="label">总行数</div><div class="value">{{taskDetail.stats.total_rows}}</div></div>
            <div class="box"><div class="label">修复字段数</div><div class="value">{{taskDetail.stats.fixed_count}}</div></div>
            <div class="box"><div class="label">补齐字段数</div><div class="value">{{taskDetail.stats.filled_count}}</div></div>
            <div class="box"><div class="label">汇率变更行数</div><div class="value">{{taskDetail.stats.fx_changed_rows}}</div></div>
            <div class="box"><div class="label">LLM补齐字段数</div><div class="value">{{taskDetail.stats.llm_filled_count}}</div></div>
          </div>
        </div>

        <div v-else-if="taskDetail.status==='failed'">
          <div class="section-title" style="margin-bottom: 8px;">失败原因</div>
          <el-alert type="error" :closable="false"
            :title="taskDetail.error.message"
            :description="'错误码：'+taskDetail.error.code+'；位置：'+taskDetail.error.detail.sheet+' R'+taskDetail.error.detail.row+' C'+taskDetail.error.detail.col">
          </el-alert>
        </div>

        <div v-else>
          <el-alert type="info" :closable="false" title="等待处理或处理中" description="processing 阶段可展示进度与日志（一期可简化）。"></el-alert>
        </div>
      </div>
    </div>

    <!-- RIGHT: Config snapshot -->
    <div class="card">
      <div class="card-hd">
        <div>
          <div class="section-title">处理配置快照（展示）</div>
          <div class="muted">模板映射 + MAP + PROCESS + AI 能力</div>
        </div>
      </div>
      <div class="card-bd">
        <el-collapse accordion>
          <el-collapse-item title="模板映射（template_mappings）" name="1">
            <div class="muted">用于识别 Sheet、绑定原始列到 source_key</div>
            <div style="margin-top:8px;">
              <el-tag>sheet_match: Sheet1</el-tag>
              <div class="footer-note">仅展示，不做编辑。</div>
            </div>
          </el-collapse-item>

          <el-collapse-item title="字段映射（MAP）" name="2">
            <div class="muted">定义最终列值从哪里来：COPY/DROP/DERIVE</div>
            <div class="footer-note">DERIVE 可能走 AI 或计算；COPY 取原始列；DROP 不输出。</div>
          </el-collapse-item>

          <el-collapse-item title="字段处理（PROCESS）" name="3">
            <div class="muted">RULE_FIX / CALC / AI，且依赖关系不同</div>
            <div class="footer-note">RULE_FIX 仅依赖自身；CALC/AI 可依赖其他列。</div>
          </el-collapse-item>

          <el-collapse-item title="AI 能力（ai_field_capabilities）" name="4">
            <div class="muted">列级 prompt / 约束 / 失败策略</div>
            <div class="footer-note">用于 PROCESS 阶段 field_type=AI 的执行。</div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import taskService from '../services/taskService'

const route = useRoute()
const taskId = route.params.id

// 任务详情数据
const taskDetail = ref({
  id: '',
  file_type: 'customs',
  unique_code: '',
  flight_no: '',
  declare_date: '',
  status: 'queued',
  created_at: '',
  progress_stage: 'done',
  stats: null,
  error: null
});

// 加载任务详情
const loadTaskDetail = async () => {
  try {
    // 获取任务详情，axios拦截器已经处理了response.data
    const response = await taskService.getTaskDetail(taskId);
    const data = response.data;
    taskDetail.value = data;
    // 添加计算字段
    taskDetail.value.progress_stage = data.status === "processing" ? "fill" : (data.status === "success" ? "done" : "failed");
  } catch (error) {
    console.error('获取任务详情错误:', error);
    ElMessage.error('获取任务详情失败');
  }
};

// 运行任务
const runTask = async () => {
  try {
    // 运行任务，axios拦截器已经处理了response.data
    await taskService.runTask(taskId);
    ElMessage.info("开始处理");
    // 重新加载任务详情
    await loadTaskDetail();
    // 定期轮询任务状态
    const pollInterval = setInterval(async () => {
      await loadTaskDetail();
      if (taskDetail.value.status !== 'processing') {
        clearInterval(pollInterval);
        if (taskDetail.value.status === 'success') {
          ElMessage.success("处理完成");
        } else if (taskDetail.value.status === 'failed') {
          ElMessage.error("处理失败");
        }
      }
    }, 1000);
  } catch (error) {
    console.error('运行任务错误:', error);
    ElMessage.error('运行任务失败');
  }
};

// 下载任务文件
const downloadFile = async (kind) => {
  try {
    const response = await taskService.downloadTaskFile(taskId, kind);
    // 创建下载链接，blob数据在response.data中
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${taskId}_${kind}.xlsx`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    ElMessage.success(`下载 ${kind} 文件成功`);
  } catch (error) {
    console.error('下载文件错误:', error);
    ElMessage.error(`下载 ${kind} 文件失败`);
  }
};

// 组件挂载时加载任务详情
onMounted(async () => {
  await loadTaskDetail();
});
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.tag-pill { display:inline-flex; align-items:center; gap:6px; padding: 2px 10px; border-radius: 999px; border:1px solid #eaecef; background:#fff; font-size: 12px; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
.split { display:grid; grid-template-columns: 1.25fr 0.75fr; gap: 12px; }
.kpi { display:grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
.kpi .box { padding: 12px; border-radius: 12px; border: 1px solid #eaecef; background: #fff; }
.kpi .label { font-size: 12px; color:#6b7280; }
.kpi .value { font-weight: 800; font-size: 18px; margin-top: 4px; }
@media (max-width: 980px) {
  .split { grid-template-columns: 1fr; }
  .kpi { grid-template-columns: 1fr 1fr; }
}
</style>
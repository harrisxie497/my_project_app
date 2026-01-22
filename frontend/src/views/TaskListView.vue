<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">任务中心</div>
        <div class="muted">上传 1 个 Excel → 生成结果 Excel、对比文件、变化统计</div>
      </div>
      <div style="display:flex; gap:8px;">
        <el-button type="primary" @click="createDialog=true">新建任务</el-button>
      </div>
    </div>

    <div class="card-bd">
      <div class="grid-2" style="margin-bottom: 10px;">
        <el-select v-model="filters.file_type" placeholder="文件类型（全部）" clearable>
          <el-option label="清关文件" value="customs"></el-option>
          <el-option label="派送文件" value="delivery"></el-option>
        </el-select>

        <el-select v-model="filters.status" placeholder="状态（全部）" clearable>
          <el-option label="queued" value="queued"></el-option>
          <el-option label="processing" value="processing"></el-option>
          <el-option label="success" value="success"></el-option>
          <el-option label="failed" value="failed"></el-option>
        </el-select>

        <el-input v-model="filters.unique_code" placeholder="唯一编码（模糊匹配）"></el-input>
        <div></div>
      </div>

      <el-table :data="filteredTasks" style="width:100%;" @row-click="goTaskDetail">
        <el-table-column prop="id" label="任务ID" width="120"></el-table-column>
        <el-table-column prop="file_type" label="类型" width="120">
          <template #default="{row}">
            <span class="tag-pill">{{ row.file_type==='customs' ? '清关' : '派送' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="unique_code" label="唯一编码" width="140"></el-table-column>
        <el-table-column prop="flight_no" label="航空号" width="120"></el-table-column>
        <el-table-column prop="declare_date" label="报关日期" width="120"></el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{row}">
            <el-tag v-if="row.status==='success'" type="success">success</el-tag>
            <el-tag v-else-if="row.status==='failed'" type="danger">failed</el-tag>
            <el-tag v-else-if="row.status==='processing'" type="warning">processing</el-tag>
            <el-tag v-else>queued</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间"></el-table-column>
      </el-table>

      <div class="footer-note">
        点击任意行进入任务详情。
      </div>
    </div>

    <!-- Create Task Dialog -->
    <el-dialog v-model="createDialog" title="新建任务（上传 Excel）" width="720px">
      <el-form label-position="top">
        <div class="grid-2">
          <el-form-item label="文件类型">
            <el-select v-model="createForm.file_type" style="width:100%;">
              <el-option label="清关文件" value="customs"></el-option>
              <el-option label="派送文件" value="delivery"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="唯一编码（必填）">
            <el-input v-model="createForm.unique_code" placeholder="例如 UC001"></el-input>
          </el-form-item>
        </div>

        <div v-if="createForm.file_type==='customs'" class="grid-2">
          <el-form-item label="航空号（必填）">
            <el-input v-model="createForm.flight_no" placeholder="例如 NH123"></el-input>
          </el-form-item>
          <el-form-item label="报关日期（必填）">
            <el-date-picker v-model="createForm.declare_date" type="date" value-format="YYYY-MM-DD" style="width:100%;"></el-date-picker>
          </el-form-item>
        </div>

        <el-form-item label="上传文件（仅支持 .xlsx，且一次仅 1 个文件）">
          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".xlsx"
            :on-change="handleFileChange"
            :on-remove="handleRemove"
            :file-list="fileList"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">拖拽文件到此处，或 <em>点击选择</em></div>
          </el-upload>
        </el-form-item>

        <el-alert type="info" :closable="false"
          title="处理逻辑提示"
          description="系统将按：模板映射(template_mappings) → 字段映射(MAP) → 字段处理(PROCESS：RULE_FIX/CALC/AI) → 样式(ExcelConfig) 生成最终文件。">
        </el-alert>
      </el-form>

      <template #footer>
        <el-button @click="createDialog=false">取消</el-button>
        <el-button type="primary" @click="submitCreate">创建任务</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import taskService from '../services/taskService'

const router = useRouter()

// 任务列表
const tasks = ref([]);
const loading = ref(false);

// Filters
const filters = reactive({
  file_type: "",
  status: "",
  unique_code: ""
});

// 获取任务列表
const fetchTasks = async () => {
  loading.value = true;
  try {
    // 获取任务列表，axios拦截器已经处理了response.data
    const response = await taskService.getTasks(filters);
    tasks.value = response.data?.items || [];
  } catch (error) {
    ElMessage.error('获取任务列表失败');
    console.error('获取任务列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 监听过滤条件变化
const filteredTasks = computed(() => {
  return tasks.value.filter(t => {
    if (filters.file_type && t.file_type !== filters.file_type) return false;
    if (filters.status && t.status !== filters.status) return false;
    if (filters.unique_code && !String(t.unique_code).includes(filters.unique_code)) return false;
    return true;
  });
});

// 创建任务对话框
const createDialog = ref(false);
const createForm = reactive({
  file_type: "customs",
  unique_code: "",
  flight_no: "",
  declare_date: ""
});

// 文件列表，用于Upload组件
const fileList = ref([]);

// 处理文件选择变化
const handleFileChange = (file, files) => {
  // 更新文件列表
  fileList.value = files;
};

// 移除文件
const handleRemove = (file, files) => {
  fileList.value = files;
};

// 创建任务
const submitCreate = async () => {
  try {
    // 检查是否选择了文件
    if (!fileList.value || fileList.value.length === 0) {
      ElMessage.error('请选择要上传的文件');
      return;
    }
    
    // 构造FormData对象，用于multipart/form-data格式的请求
    const formData = new FormData();
    
    // 添加表单字段
    formData.append('file_type', createForm.file_type);
    formData.append('unique_code', createForm.unique_code);
    
    // 仅当字段有值时才添加
    if (createForm.flight_no) {
      formData.append('flight_no', createForm.flight_no);
    }
    if (createForm.declare_date) {
      formData.append('declare_date', createForm.declare_date);
    }
    
    // 从fileList中获取文件，Element Plus的Upload组件中，文件对象存储在raw属性中
    const file = fileList.value[0].raw;
    if (file) {
      formData.append('file', file);
    } else {
      ElMessage.error('文件格式错误，请重新选择');
      return;
    }
    
    // 发送请求
    const response = await taskService.createTask(formData);
    const newTask = response.data;
    
    // 刷新任务列表
    await fetchTasks();
    
    // 关闭对话框
    createDialog.value = false;
    
    // 跳转到任务详情页
    router.push(`/task-detail/${newTask.task_id}`);
    
    // 显示成功消息
    ElMessage.success('任务创建成功');
    
    // 清空文件列表
    fileList.value = [];
  } catch (error) {
    ElMessage.error('任务创建失败');
    console.error('任务创建失败:', error);
  }
};

const goTaskDetail = (row) => {
  router.push(`/task-detail/${row.id}`);
};

// 初始化加载数据
onMounted(() => {
  fetchTasks();
});
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.grid-2 { display:grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.tag-pill { display:inline-flex; align-items:center; gap:6px; padding: 2px 10px; border-radius: 999px; border:1px solid #eaecef; background:#fff; font-size: 12px; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
@media (max-width: 980px) {
  .grid-2 { grid-template-columns: 1fr; }
}
</style>
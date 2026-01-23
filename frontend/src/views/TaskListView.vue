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
            <el-option label="待处理" value="queued"></el-option>
            <el-option label="处理中" value="processing"></el-option>
            <el-option label="成功" value="success"></el-option>
            <el-option label="失败" value="failed"></el-option>
          </el-select>

          <el-date-picker 
            v-model="filters.arrival_date_range" 
            type="daterange" 
            range-separator="至" 
            start-placeholder="到达日期开始" 
            end-placeholder="到达日期结束" 
            value-format="YYYY-MM-DD" 
            style="width: 100%;"
          ></el-date-picker>

          <el-input v-model="filters.flight_no" placeholder="FLIGHT NO"></el-input>
        </div>
        <div class="grid-2" style="margin-bottom: 10px;">
          <el-input v-model="filters.created_by" placeholder="负责人（创建人）"></el-input>
        </div>

        <el-table :data="filteredTasks" style="width:100%;" stripe>
          <el-table-column prop="file_type" label="文件类型" width="100">
            <template #default="{row}">
              <span class="tag-pill">{{ row.file_type==='customs' ? '清关' : '派送' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="flight_no" label="FLIGHT NO" width="100"></el-table-column>
          <el-table-column prop="declare_date" label="ARRIVAL DATE" width="120"></el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{row}">
              <el-tag v-if="row.status==='success'" type="success">成功</el-tag>
              <el-tag v-else-if="row.status==='failed'" type="danger">失败</el-tag>
              <el-tag v-else-if="row.status==='processing'" type="warning">处理中</el-tag>
              <el-tag v-else>待处理</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_by_user_name" label="创建人" width="120"></el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{row}">
              <el-button 
                type="primary" 
                size="small" 
                @click="goTaskDetail(row)" 
                :icon="View"
                style="margin-right: 8px;">
                详情
              </el-button>
              <el-button 
                type="primary" 
                size="small" 
                @click.stop="downloadResult(row.id)" 
                :disabled="row.status !== 'success'"
                :icon="Download"
              >
                下载结果
              </el-button>
            </template>
          </el-table-column>
        </el-table>

      <div class="footer-note">
        点击详情按钮进入任务详情页。
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
        </div>

        <!-- 清关文件字段 -->
        <div v-if="createForm.file_type==='customs'" class="grid-2">
          <el-form-item label="MAWB NO" required>
            <el-input v-model="createForm.mawb_no" placeholder="例如 16003270890"></el-input>
          </el-form-item>
          <el-form-item label="FLIGHT NO" required>
            <el-input v-model="createForm.flight_no" placeholder="例如 CX596"></el-input>
          </el-form-item>
          <el-form-item label="ARRIVAL DATE" required>
            <el-date-picker v-model="createForm.arrival_date" type="date" value-format="YYYYMMDD" style="width:100%;"></el-date-picker>
          </el-form-item>
        </div>

        <!-- 派送文件字段 -->
        <div v-if="createForm.file_type==='delivery'" class="grid-2">
          <el-form-item label="記事欄2" required>
            <el-input v-model="createForm.note_field2" placeholder="例如 160-03270890"></el-input>
          </el-form-item>
        </div>

        <el-form-item label="上传文件（仅支持 .xlsx，且一次仅 1 个文件）" required>
          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".xlsx"
            :on-change="handleFileChange"
            :on-remove="handleRemove"
            :file-list="fileList"
            :disabled="false"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">拖拽文件到此处，或 <em>点击选择</em></div>
            <template #tip>
              <div class="el-upload__tip">
                仅支持 .xlsx 文件，最大支持 10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-alert type="info" :closable="false"
          title="处理逻辑提示"
          description="系统将按：模板映射(template_mappings) → 字段映射(MAP) → 字段处理(PROCESS：RULE_FIX/CALC/AI) → 样式(ExcelConfig) 生成最终文件。">
        </el-alert>
      </el-form>

      <template #footer>
        <el-button @click="createDialog=false">取消</el-button>
        <el-button type="primary" @click="submitCreate" :disabled="fileList.length === 0">创建任务</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Download, View } from '@element-plus/icons-vue'
import taskService from '../services/taskService'

const router = useRouter()

// 任务列表
const tasks = ref([]);
const loading = ref(false);

// Filters
const filters = reactive({
  file_type: "",
  status: "",
  arrival_date_range: null,
  flight_no: "",
  created_by: ""
});

// 获取任务列表
const fetchTasks = async () => {
  loading.value = true;
  try {
    // 构造查询参数
    const queryParams = {
      file_type: filters.file_type,
      status: filters.status,
      flight_no: filters.flight_no,
      created_by: filters.created_by
    };
    
    // 添加到达日期范围查询参数
    if (filters.arrival_date_range && filters.arrival_date_range.length === 2) {
      queryParams.declare_date_from = filters.arrival_date_range[0];
      queryParams.declare_date_to = filters.arrival_date_range[1];
    }
    
    // 获取任务列表，axios拦截器已经处理了response.data
    const response = await taskService.getTasks(queryParams);
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
    if (filters.flight_no && !String(t.flight_no || '').includes(filters.flight_no)) return false;
    if (filters.created_by && !String(t.created_by_user_name || '').includes(filters.created_by)) return false;
    // 处理到达日期范围过滤
    if (filters.arrival_date_range && filters.arrival_date_range.length === 2) {
      const fromDate = new Date(filters.arrival_date_range[0]);
      const toDate = new Date(filters.arrival_date_range[1]);
      const taskDate = new Date(t.declare_date);
      if (taskDate < fromDate || taskDate > toDate) return false;
    }
    return true;
  });
});

// 创建任务对话框
const createDialog = ref(false);

// 获取今天的日期，格式化为YYYYMMDD
const today = new Date();
const todayFormatted = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`;

const createForm = reactive({
  file_type: "customs",
  // 清关文件字段
  mawb_no: "16003270890",
  flight_no: "CX596",
  arrival_date: todayFormatted,
  // 派送文件字段
  note_field2: "160-03270890"
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
    
    if (createForm.file_type === 'customs') {
      // 清关文件：MAWB NO 作为唯一编码
      formData.append('unique_code', createForm.mawb_no);
      formData.append('flight_no', createForm.flight_no);
      
      // 转换 arrival_date 格式从 YYYYMMDD 到 YYYY-MM-DD
      const arrivalDate = createForm.arrival_date;
      if (arrivalDate) {
        const formattedDate = `${arrivalDate.substring(0, 4)}-${arrivalDate.substring(4, 6)}-${arrivalDate.substring(6, 8)}`;
        formData.append('declare_date', formattedDate);
      }
    } else if (createForm.file_type === 'delivery') {
      // 派送文件：記事欄2 作为唯一编码
      formData.append('unique_code', createForm.note_field2);
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

// 下载结果文件
const downloadResult = async (taskId) => {
  try {
    await taskService.downloadTaskFile(taskId, 'result');
    ElMessage.success('下载结果文件成功');
  } catch (error) {
    console.error('下载结果文件失败:', error);
    ElMessage.error('下载结果文件失败');
  }
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
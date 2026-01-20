<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">AI 能力配置（ai_field_capabilities）</div>
        <div class="muted">按列配置 capability / depends_on / prompt / 输出约束</div>
      </div>
      <div style="display:flex; gap:8px;">
        <el-button type="primary" @click="openAddDialog">新增 AI 配置</el-button>
      </div>
    </div>
    <div class="card-bd">
      <el-table :data="aiCaps" style="width:100%;">
        <el-table-column prop="file_type" label="file_type" width="120"></el-table-column>
        <el-table-column prop="target_column" label="target_column" width="140"></el-table-column>
        <el-table-column prop="capability_code" label="capability_code" width="220"></el-table-column>
        <el-table-column prop="depends_on" label="depends_on" width="200"></el-table-column>
        <el-table-column prop="on_fail" label="on_fail" width="120"></el-table-column>
        <el-table-column prop="enabled" label="enabled" width="120">
          <template #default="{row}"><el-switch v-model="row.enabled"></el-switch></template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default>
            <el-button size="small">编辑</el-button>
            <el-button size="small" type="danger" plain>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="footer-note">
        编辑页应包含：prompt_template、多语言、output_constraints_json（max_length/charset/not_empty）。
      </div>
    </div>

    <!-- 新增AI配置弹窗 -->
    <el-dialog
      v-model="addDialogVisible"
      title="新增AI配置"
      width="720px"
      :close-on-click-modal="false"
    >
      <el-form ref="addFormRef" :model="addForm" label-position="top" :rules="addFormRules">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="file_type" prop="file_type">
              <el-input v-model="addForm.file_type" placeholder="请输入file_type" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="target_column" prop="target_column">
              <el-input v-model="addForm.target_column" placeholder="请输入目标列（如：B）" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="capability_code" prop="capability_code">
              <el-input v-model="addForm.capability_code" placeholder="请输入能力代码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="depends_on" prop="depends_on">
              <el-input v-model="addForm.depends_on" placeholder="依赖列（如：B,C,D,E）" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="on_fail" prop="on_fail">
              <el-select v-model="addForm.on_fail" placeholder="选择失败处理方式">
                <el-option label="阻塞" value="block" />
                <el-option label="跳过" value="skip" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="enabled" prop="enabled">
              <el-switch v-model="addForm.enabled" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="prompt_template" prop="prompt_template">
          <el-input
            v-model="addForm.prompt_template"
            type="textarea"
            :rows="4"
            placeholder="请输入AI提示模板"
          />
        </el-form-item>
        <el-form-item label="output_constraints_json" prop="output_constraints_json">
          <el-input
            v-model="addForm.output_constraints_json"
            type="textarea"
            :rows="3"
            placeholder='JSON格式：{"max_length":100,"charset":"utf-8","not_empty":true}'
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import aiCapabilityService from '../../services/aiCapabilityService'

const aiCaps = ref([]);
const loading = ref(false);

// 获取AI能力配置列表
const fetchAICapabilities = async () => {
  loading.value = true;
  try {
    const response = await aiCapabilityService.getAICapabilities();
    aiCaps.value = response.data.list || [];
  } catch (error) {
    ElMessage.error('获取AI能力配置失败');
    console.error('获取AI能力配置失败:', error);
  } finally {
    loading.value = false;
  }
};

// 新增AI配置弹窗相关
const addDialogVisible = ref(false);
const addFormRef = ref(null);
const addForm = ref({
  file_type: '',
  target_column: '',
  capability_code: '',
  depends_on: '',
  on_fail: 'block',
  enabled: true,
  prompt_template: '',
  output_constraints_json: ''
});

const addFormRules = ref({
  file_type: [{ required: true, message: '请输入file_type', trigger: 'blur' }],
  target_column: [{ required: true, message: '请输入目标列', trigger: 'blur' }],
  capability_code: [{ required: true, message: '请输入能力代码', trigger: 'blur' }],
  prompt_template: [{ required: true, message: '请输入AI提示模板', trigger: 'blur' }]
});

const openAddDialog = () => {
  addDialogVisible.value = true;
};

const handleAddSubmit = async () => {
  addFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await aiCapabilityService.addAICapability(addForm.value);
        const newItem = response.data;
        aiCaps.value.push(newItem);
        addDialogVisible.value = false;
        // 重置表单
        addFormRef.value.resetFields();
        ElMessage.success('新增AI配置成功');
      } catch (error) {
        ElMessage.error('新增AI配置失败');
        console.error('新增AI配置失败:', error);
      }
    }
  });
};

// 初始化加载数据
onMounted(() => {
  fetchAICapabilities();
});
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
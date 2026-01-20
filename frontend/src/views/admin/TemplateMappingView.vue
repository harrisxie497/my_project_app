<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">模板映射（template_mappings）</div>
        <div class="muted">解决原始 Excel 模板差异：Sheet 识别 + 列绑定</div>
      </div>
      <div style="display:flex; gap:8px;">
        <el-button type="primary" @click="addDialogVisible = true">新增映射</el-button>
      </div>
    </div>
    <div class="card-bd">
      <el-table :data="templateMappings" style="width:100%;">
        <el-table-column prop="mapping_code" label="mapping_code" width="200"></el-table-column>
        <el-table-column prop="file_type" label="file_type" width="120"></el-table-column>
        <el-table-column prop="sheet_match_mode" label="sheet_match_mode" width="150"></el-table-column>
        <el-table-column prop="sheet_match_value" label="sheet_match_value" width="160"></el-table-column>
        <el-table-column prop="enabled" label="enabled" width="120">
          <template #default="{row}"><el-switch v-model="row.enabled"></el-switch></template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default>
            <el-button size="small">编辑</el-button>
            <el-button size="small" type="primary" plain>校验</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="footer-note">
        建议编辑页：支持 JSON 编辑器（column_bindings_json）、一键校验 required source_key 是否能解析。
      </div>
    </div>

    <!-- 新增映射弹窗 -->
    <el-dialog
      v-model="addDialogVisible"
      title="新增模板映射"
      width="720px"
      :close-on-click-modal="false"
    >
      <el-form ref="addFormRef" :model="addForm" label-position="top" :rules="addFormRules">
        <div class="grid-2">
          <el-form-item label="映射编码" prop="mapping_code">
            <el-input v-model="addForm.mapping_code" placeholder="例如：TM_CUSTOMS_V1"></el-input>
          </el-form-item>
          <el-form-item label="文件类型" prop="file_type">
            <el-select v-model="addForm.file_type" style="width:100%;">
              <el-option label="清关文件" value="customs"></el-option>
              <el-option label="派送文件" value="delivery"></el-option>
            </el-select>
          </el-form-item>
        </div>

        <div class="grid-2">
          <el-form-item label="Sheet 匹配模式" prop="sheet_match_mode">
            <el-select v-model="addForm.sheet_match_mode" style="width:100%;">
              <el-option label="按名称匹配" value="name"></el-option>
              <el-option label="按索引匹配" value="index"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="匹配值" prop="sheet_match_value">
            <el-input v-model="addForm.sheet_match_value" placeholder="例如：Sheet1 或 0"></el-input>
          </el-form-item>
        </div>

        <el-form-item label="列绑定 JSON" prop="column_bindings_json">
          <el-input
            v-model="addForm.column_bindings_json"
            type="textarea"
            :rows="6"
            placeholder='例如：{"bindings":[{"source_key":"order_no","match":{"by":"header","candidates":["お客様管理番号","订单号"]},"fallback":{"by":"col","value":"A"},"required":true}]}'
          ></el-input>
        </el-form-item>

        <el-form-item label="启用状态">
          <el-switch v-model="addForm.enabled"></el-switch>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import templateMappingService from '../../services/templateMappingService'

const templateMappings = ref([]);
const loading = ref(false);

// 获取模板映射列表
const fetchTemplateMappings = async () => {
  loading.value = true;
  try {
    const response = await templateMappingService.getTemplateMappings();
    templateMappings.value = response.data.list || [];
  } catch (error) {
    ElMessage.error('获取模板映射列表失败');
    console.error('获取模板映射列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 新增映射弹窗相关
const addDialogVisible = ref(false)
const addFormRef = ref(null)
const addForm = reactive({
  mapping_code: '',
  file_type: 'customs',
  sheet_match_mode: 'name',
  sheet_match_value: '',
  column_bindings_json: '',
  enabled: true
})

const addFormRules = reactive({
  mapping_code: [
    { required: true, message: '请输入映射编码', trigger: 'blur' }
  ],
  file_type: [
    { required: true, message: '请选择文件类型', trigger: 'change' }
  ],
  sheet_match_mode: [
    { required: true, message: '请选择Sheet匹配模式', trigger: 'change' }
  ],
  sheet_match_value: [
    { required: true, message: '请输入匹配值', trigger: 'blur' }
  ]
})

const handleAdd = async () => {
  try {
    await addFormRef.value.validate()
    const response = await templateMappingService.addTemplateMapping(addForm);
    const newMapping = response.data;
    templateMappings.value.push(newMapping);
    addDialogVisible.value = false
    ElMessage.success('新增映射成功')
    // 重置表单
    Object.assign(addForm, {
      mapping_code: '',
      file_type: 'customs',
      sheet_match_mode: 'name',
      sheet_match_value: '',
      column_bindings_json: '',
      enabled: true
    })
  } catch (error) {
    ElMessage.error('新增映射失败');
    console.error('新增映射失败:', error);
  }
}

// 初始化加载数据
onMounted(() => {
  fetchTemplateMappings();
});
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.footer-note { font-size: 12px; color:#6b7280; margin-top: 10px; }
</style>
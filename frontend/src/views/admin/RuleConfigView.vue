<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">规则配置</div>
        <div class="muted">rule_tables / rule_items · 支持导入模板</div>
      </div>
      <div style="display:flex; gap:8px;">
        <el-button type="primary" @click="importDialog=true">导入规则模板</el-button>
      </div>
    </div>

    <div class="card-bd">
      <el-table :data="ruleTables" style="width:100%;">
        <el-table-column prop="code" label="code" width="170"></el-table-column>
        <el-table-column prop="file_type" label="file_type" width="120"></el-table-column>
        <el-table-column prop="rule_stage" label="stage" width="120"></el-table-column>
        <el-table-column prop="enabled" label="enabled" width="120">
          <template #default="{row}">
            <el-switch v-model="row.enabled"></el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="description"></el-table-column>
      </el-table>

      <div class="footer-note">
        rule_items 的增删改查可在二级页面完成。
      </div>
    </div>

    <!-- Import Dialog -->
    <el-dialog v-model="importDialog" title="导入规则配置（Excel 模板）" width="720px">
      <el-upload
        drag
        :auto-upload="false"
        :limit="1"
        accept=".xlsx"
        :on-change="onImportChange"
      >
        <div class="el-upload__text">拖拽导入模板到此处，或 <em>点击选择</em></div>
      </el-upload>

      <div class="footer-note">
        导入将写入 rule_tables / rule_items / template_mappings / ai_field_capabilities。
      </div>

      <template #footer>
        <el-button @click="importDialog=false">取消</el-button>
        <el-button type="primary" @click="doImport">开始导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ruleService from '../../services/ruleService'

const ruleTables = ref([]);
const loading = ref(false);

// 获取规则表列表
const fetchRuleTables = async () => {
  loading.value = true;
  try {
    const response = await ruleService.getRuleTables();
    ruleTables.value = response.data.list || [];
  } catch (error) {
    ElMessage.error('获取规则表失败');
    console.error('获取规则表失败:', error);
  } finally {
    loading.value = false;
  }
};

const importDialog = ref(false);
const importFile = ref(null);

const onImportChange = (file) => { importFile.value = file; };

const doImport = async () => {
  try {
    // 模拟导入操作
    const formData = new FormData();
    if (importFile.value) {
      formData.append('file', importFile.value.raw);
    }
    // 使用mock API
    const response = await ruleService.importRuleTemplate(formData);
    ElMessage.success('规则模板导入成功');
    fetchRuleTables(); // 重新加载规则表
    importDialog.value = false;
  } catch (error) {
    ElMessage.error('导入失败');
    console.error('导入失败:', error);
  }
};

// 初始化加载数据
onMounted(() => {
  fetchRuleTables();
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
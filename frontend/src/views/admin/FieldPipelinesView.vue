<template>
  <div class="admin-container">
    <div class="header-actions">
      <h2>字段映射管理</h2>
      <el-button type="primary" @click="handleAdd">新增配置</el-button>
    </div>
    <div class="table-container">
      <el-table :data="fieldPipelines" stripe style="width: 100%">
        <el-table-column prop="file_type" label="文件类型" width="100"></el-table-column>
        <el-table-column prop="target_col" label="目标列" width="80"></el-table-column>
        <el-table-column prop="target_header" label="目标表头" width="150"></el-table-column>
        <el-table-column prop="field_type" label="字段类型" width="120"></el-table-column>
        <el-table-column prop="order" label="顺序" width="80"></el-table-column>
        <el-table-column prop="enabled" label="状态" width="80">
          <template #default="scope">
            <el-switch v-model="scope.row.enabled" @change="handleStatusChange(scope.row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      ></el-pagination>
    </div>
    
    <!-- 新增配置对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新增字段映射"
      width="500px"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="120px"
      >
        <el-form-item label="文件类型" prop="file_type">
          <el-select v-model="form.file_type" placeholder="请选择文件类型">
            <el-option label="清关文件" value="customs"></el-option>
            <el-option label="派送文件" value="delivery"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="目标列" prop="target_col">
          <el-input v-model="form.target_col" placeholder="请输入目标列，例如：A"></el-input>
        </el-form-item>
        <el-form-item label="目标表头" prop="target_header">
          <el-input v-model="form.target_header" placeholder="请输入目标表头"></el-input>
        </el-form-item>
        <el-form-item label="映射操作" prop="map_op">
          <el-select v-model="form.map_op" placeholder="请选择映射操作">
            <el-option label="复制" value="COPY"></el-option>
            <el-option label="常量" value="CONST"></el-option>
            <el-option label="输入" value="INPUT"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="源列" prop="source_cols">
          <el-input
            v-model="form.source_cols"
            type="textarea"
            placeholder='请输入源列，例如：["A", "B"]'
            rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="字段类型" prop="field_type">
          <el-select v-model="form.field_type" placeholder="请选择字段类型">
            <el-option label="复制" value="COPY"></el-option>
            <el-option label="格式化" value="FORMAT"></el-option>
            <el-option label="默认值" value="DEFAULT"></el-option>
            <el-option label="计算" value="CALC"></el-option>
            <el-option label="规则修复" value="RULE_FIX"></el-option>
            <el-option label="常量" value="CONST"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="规则引用" prop="rule_ref">
          <el-input
            v-model="form.rule_ref"
            type="textarea"
            placeholder='请输入规则引用，例如：["rule1", "rule2"]'
            rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="依赖列" prop="depends_on">
          <el-input
            v-model="form.depends_on"
            type="textarea"
            placeholder='请输入依赖列，例如：["A", "B"]'
            rows="2"
          ></el-input>
        </el-form-item>
        <el-form-item label="顺序" prop="order">
          <el-input-number v-model="form.order" :min="1" :max="100" placeholder="请输入顺序"></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import fieldPipelinesService from '../../services/fieldPipelinesService';

export default {
  name: 'FieldPipelinesView',
  data() {
    return {
      fieldPipelines: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
      dialogVisible: false,
      formRef: null,
      form: {
        file_type: '',
        target_col: '',
        target_header: '',
        map_op: '',
        source_cols: '[]',
        field_type: '',
        rule_ref: '[]',
        depends_on: '[]',
        order: 10,
        enabled: true
      },
      rules: {
        file_type: [
          { required: true, message: '请选择文件类型', trigger: 'change' }
        ],
        target_col: [
          { required: true, message: '请输入目标列', trigger: 'blur' }
        ],
        target_header: [
          { required: true, message: '请输入目标表头', trigger: 'blur' }
        ],
        map_op: [
          { required: true, message: '请选择映射操作', trigger: 'change' }
        ],
        field_type: [
          { required: true, message: '请选择字段类型', trigger: 'change' }
        ]
      }
    };
  },
  mounted() {
    this.fetchFieldPipelines();
  },
  methods: {
    /**
     * 获取字段映射列表
     */
    async fetchFieldPipelines() {
      try {
        const response = await fieldPipelinesService.getFieldPipelines({
          page: this.currentPage,
          page_size: this.pageSize
        });
        this.fieldPipelines = response.data.items;
        this.total = response.data.total;
      } catch (error) {
        this.$message.error('获取字段映射列表失败');
        console.error('Failed to fetch field pipelines:', error);
      }
    },
    
    /**
     * 处理页面大小变化
     * @param {number} val - 新的页面大小
     */
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.fetchFieldPipelines();
    },
    
    /**
     * 处理当前页码变化
     * @param {number} val - 新的页码
     */
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchFieldPipelines();
    },
    
    /**
     * 处理状态变化
     * @param {Object} row - 字段映射行数据
     */
    async handleStatusChange(row) {
      try {
        await fieldPipelinesService.updateFieldPipelineStatus(row.id, row.enabled);
        this.$message.success('状态更新成功');
      } catch (error) {
        row.enabled = !row.enabled; // 恢复原状态
        this.$message.error('状态更新失败');
        console.error('Failed to update status:', error);
      }
    },
    
    /**
     * 处理编辑操作
     * @param {Object} row - 字段映射行数据
     */
    handleEdit(row) {
      // 设置表单数据
      this.form = {
        file_type: row.file_type,
        target_col: row.target_col,
        target_header: row.target_header,
        map_op: row.map_op,
        source_cols: JSON.stringify(row.source_cols),
        field_type: row.field_type,
        rule_ref: JSON.stringify(row.rule_ref),
        depends_on: JSON.stringify(row.depends_on),
        order: row.order,
        enabled: row.enabled
      };
      // 打开对话框
      this.dialogVisible = true;
    },
    
    /**
     * 处理删除操作
     * @param {Object} row - 字段映射行数据
     */
    async handleDelete(row) {
      try {
        await this.$confirm('确定要删除这条字段映射吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await fieldPipelinesService.deleteFieldPipeline(row.id);
        this.$message.success('删除成功');
        this.fetchFieldPipelines();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('删除失败');
        console.error('Failed to delete field pipeline:', error);
      }
    },
    
    /**
     * 处理新增配置
     */
    handleAdd() {
      // 重置表单
      this.form = {
        file_type: '',
        target_col: '',
        target_header: '',
        map_op: '',
        source_cols: '[]',
        field_type: '',
        rule_ref: '[]',
        depends_on: '[]',
        order: 10,
        enabled: true
      };
      if (this.formRef) {
        this.formRef.resetFields();
      }
      // 打开对话框
      this.dialogVisible = true;
    },
    
    /**
     * 处理表单提交
     */
    async handleSubmit() {
      try {
        // 表单验证
        await this.$refs.formRef.validate();
        
        // 准备提交数据
        const submitData = {
          ...this.form,
          source_cols: JSON.parse(this.form.source_cols),
          rule_ref: JSON.parse(this.form.rule_ref),
          depends_on: JSON.parse(this.form.depends_on)
        };
        
        // 调用API创建字段映射
        await fieldPipelinesService.createFieldPipeline(submitData);
        
        // 关闭对话框
        this.dialogVisible = false;
        
        // 显示成功消息
        this.$message.success('字段映射创建成功');
        
        // 重新获取列表
        this.fetchFieldPipelines();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('字段映射创建失败');
        console.error('Failed to create field pipeline:', error);
      }
    }
  }
};
</script>

<style scoped>
.admin-container {
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-container {
  margin: 20px 0;
}

.pagination-container {
  text-align: right;
  margin-top: 20px;
}
</style>
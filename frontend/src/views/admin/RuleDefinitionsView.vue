<template>
  <div class="admin-container">
    <div class="header-actions">
      <h2>规则定义管理</h2>
      <el-button type="primary" @click="handleAdd">新增配置</el-button>
    </div>
    <div class="table-container">
      <el-table :data="ruleDefinitions" stripe style="width: 100%">
        <el-table-column prop="rule_ref" label="规则标识" width="200"></el-table-column>
        <el-table-column prop="rule_type" label="规则类型" width="150"></el-table-column>
        <el-table-column prop="executor_type" label="执行器类型" width="150"></el-table-column>
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
      title="新增规则定义"
      width="600px"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="120px"
      >
        <el-form-item label="规则标识" prop="rule_ref">
          <el-input v-model="form.rule_ref" placeholder="请输入规则标识"></el-input>
        </el-form-item>
        <el-form-item label="规则类型" prop="rule_type">
          <el-select v-model="form.rule_type" placeholder="请选择规则类型">
            <el-option label="格式化" value="FORMAT"></el-option>
            <el-option label="计算" value="CALC"></el-option>
            <el-option label="规则修复" value="RULE_FIX"></el-option>
            <el-option label="常量" value="CONST"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="执行器类型" prop="executor_type">
          <el-select v-model="form.executor_type" placeholder="请选择执行器类型">
            <el-option label="程序" value="program"></el-option>
            <el-option label="AI" value="ai"></el-option>
            <el-option label="Web" value="web"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="规则配置" prop="schema_json">
          <el-input
            v-model="form.schema_json"
            type="textarea"
            placeholder="请输入规则配置JSON"
            rows="4"
          ></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.enabled"></el-switch>
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
import ruleDefinitionsService from '../../services/ruleDefinitionsService';

export default {
  name: 'RuleDefinitionsView',
  data() {
    return {
      ruleDefinitions: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
      dialogVisible: false,
      formRef: null,
      form: {
        rule_ref: '',
        rule_type: '',
        executor_type: '',
        schema_json: '{}',
        enabled: true
      },
      rules: {
        rule_ref: [
          { required: true, message: '请输入规则标识', trigger: 'blur' }
        ],
        rule_type: [
          { required: true, message: '请选择规则类型', trigger: 'change' }
        ],
        executor_type: [
          { required: true, message: '请选择执行器类型', trigger: 'change' }
        ],
        schema_json: [
          { required: true, message: '请输入规则配置', trigger: 'blur' }
        ]
      }
    };
  },
  mounted() {
    this.fetchRuleDefinitions();
  },
  methods: {
    /**
     * 获取规则定义列表
     */
    async fetchRuleDefinitions() {
      try {
        const response = await ruleDefinitionsService.getRuleDefinitions({
          page: this.currentPage,
          page_size: this.pageSize
        });
        this.ruleDefinitions = response.data.items;
        this.total = response.data.total;
      } catch (error) {
        this.$message.error('获取规则定义列表失败');
        console.error('Failed to fetch rule definitions:', error);
      }
    },
    
    /**
     * 处理页面大小变化
     * @param {number} val - 新的页面大小
     */
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.fetchRuleDefinitions();
    },
    
    /**
     * 处理当前页码变化
     * @param {number} val - 新的页码
     */
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchRuleDefinitions();
    },
    
    /**
     * 处理状态变化
     * @param {Object} row - 规则定义行数据
     */
    async handleStatusChange(row) {
      try {
        await ruleDefinitionsService.updateRuleDefinitionStatus(row.rule_ref, row.enabled);
        this.$message.success('状态更新成功');
      } catch (error) {
        row.enabled = !row.enabled; // 恢复原状态
        this.$message.error('状态更新失败');
        console.error('Failed to update status:', error);
      }
    },
    
    /**
     * 处理编辑操作
     * @param {Object} row - 规则定义行数据
     */
    handleEdit(row) {
      // 设置表单数据
      this.form = {
        rule_ref: row.rule_ref,
        rule_type: row.rule_type,
        executor_type: row.executor_type,
        schema_json: JSON.stringify(row.schema_json),
        enabled: row.enabled
      };
      // 打开对话框
      this.dialogVisible = true;
    },
    
    /**
     * 处理删除操作
     * @param {Object} row - 规则定义行数据
     */
    async handleDelete(row) {
      try {
        await this.$confirm('确定要删除这条规则定义吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await ruleDefinitionsService.deleteRuleDefinition(row.rule_ref);
        this.$message.success('删除成功');
        this.fetchRuleDefinitions();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('删除失败');
        console.error('Failed to delete rule definition:', error);
      }
    },
    
    /**
     * 处理新增配置
     */
    handleAdd() {
      // 重置表单
      this.form = {
        rule_ref: '',
        rule_type: '',
        executor_type: '',
        schema_json: '{}',
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
          schema_json: JSON.parse(this.form.schema_json)
        };
        
        // 调用API创建规则定义
        await ruleDefinitionsService.createRuleDefinition(submitData);
        
        // 关闭对话框
        this.dialogVisible = false;
        
        // 显示成功消息
        this.$message.success('规则定义创建成功');
        
        // 重新获取列表
        this.fetchRuleDefinitions();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('规则定义创建失败');
        console.error('Failed to create rule definition:', error);
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
<template>
  <div class="admin-container">
    <div class="header-actions">
      <h2>文件定义管理</h2>
      <el-button type="primary" @click="handleAdd">新增配置</el-button>
    </div>
    <div class="table-container">
      <el-table :data="fileDefinitions" stripe style="width: 100%">
        <el-table-column prop="file_type" label="文件类型" width="100"></el-table-column>
        <el-table-column prop="file_role" label="文件角色" width="100"></el-table-column>
        <el-table-column prop="sheet_name" label="工作表名" width="150"></el-table-column>
        <el-table-column prop="header_row" label="表头行" width="80"></el-table-column>
        <el-table-column prop="data_start_row" label="数据起始行" width="100"></el-table-column>
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
      title="新增文件定义"
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
        <el-form-item label="文件角色" prop="file_role">
          <el-select v-model="form.file_role" placeholder="请选择文件角色">
            <el-option label="源文件" value="source"></el-option>
            <el-option label="输出文件" value="output"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="工作表名" prop="sheet_name">
          <el-input v-model="form.sheet_name" placeholder="请输入工作表名"></el-input>
        </el-form-item>
        <el-form-item label="表头行" prop="header_row">
          <el-input-number v-model="form.header_row" :min="1" :max="100" placeholder="请输入表头行"></el-input-number>
        </el-form-item>
        <el-form-item label="数据起始行" prop="data_start_row">
          <el-input-number v-model="form.data_start_row" :min="1" :max="100" placeholder="请输入数据起始行"></el-input-number>
        </el-form-item>
        <el-form-item label="列配置" prop="columns_json">
          <el-input
            v-model="form.columns_json"
            type="textarea"
            placeholder='请输入列配置JSON格式，例如：[{"col": "A", "header": "列A"}]'
            rows="3"
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
import fileDefinitionsService from '../../services/fileDefinitionsService';

export default {
  name: 'FileDefinitionsView',
  data() {
    return {
      fileDefinitions: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
      dialogVisible: false,
      formRef: null,
      form: {
        file_type: '',
        file_role: '',
        sheet_name: '',
        header_row: 1,
        data_start_row: 2,
        columns_json: '[]',
        enabled: true
      },
      rules: {
        file_type: [
          { required: true, message: '请选择文件类型', trigger: 'change' }
        ],
        file_role: [
          { required: true, message: '请选择文件角色', trigger: 'change' }
        ],
        sheet_name: [
          { required: true, message: '请输入工作表名', trigger: 'blur' }
        ],
        header_row: [
          { required: true, message: '请输入表头行', trigger: 'blur' }
        ],
        data_start_row: [
          { required: true, message: '请输入数据起始行', trigger: 'blur' }
        ],
        columns_json: [
          { required: true, message: '请输入列配置', trigger: 'blur' }
        ]
      }
    };
  },
  mounted() {
    this.fetchFileDefinitions();
  },
  methods: {
    /**
     * 获取文件定义列表
     */
    async fetchFileDefinitions() {
      try {
        const response = await fileDefinitionsService.getFileDefinitions({
          page: this.currentPage,
          page_size: this.pageSize
        });
        this.fileDefinitions = response.data.items;
        this.total = response.data.total;
      } catch (error) {
        this.$message.error('获取文件定义列表失败');
        console.error('Failed to fetch file definitions:', error);
      }
    },
    
    /**
     * 处理页面大小变化
     * @param {number} val - 新的页面大小
     */
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.fetchFileDefinitions();
    },
    
    /**
     * 处理当前页码变化
     * @param {number} val - 新的页码
     */
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchFileDefinitions();
    },
    
    /**
     * 处理状态变化
     * @param {Object} row - 文件定义行数据
     */
    async handleStatusChange(row) {
      try {
        await fileDefinitionsService.updateFileDefinitionStatus(row.id, row.enabled);
        this.$message.success('状态更新成功');
      } catch (error) {
        row.enabled = !row.enabled; // 恢复原状态
        this.$message.error('状态更新失败');
        console.error('Failed to update status:', error);
      }
    },
    
    /**
     * 处理编辑操作
     * @param {Object} row - 文件定义行数据
     */
    handleEdit(row) {
      // 设置表单数据
      this.form = {
        file_type: row.file_type,
        file_role: row.file_role,
        sheet_name: row.sheet_name,
        header_row: row.header_row,
        data_start_row: row.data_start_row,
        columns_json: JSON.stringify(row.columns_json),
        enabled: row.enabled
      };
      // 打开对话框
      this.dialogVisible = true;
    },
    
    /**
     * 处理删除操作
     * @param {Object} row - 文件定义行数据
     */
    async handleDelete(row) {
      try {
        await this.$confirm('确定要删除这条文件定义吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await fileDefinitionsService.deleteFileDefinition(row.id);
        this.$message.success('删除成功');
        this.fetchFileDefinitions();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('删除失败');
        console.error('Failed to delete file definition:', error);
      }
    },
    
    /**
     * 处理新增配置
     */
    handleAdd() {
      // 重置表单
      this.form = {
        file_ref: '',
        file_name: '',
        file_type: '',
        description: '',
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
          columns_json: JSON.parse(this.form.columns_json)
        };
        
        // 调用API创建文件定义
        await fileDefinitionsService.createFileDefinition(submitData);
        
        // 关闭对话框
        this.dialogVisible = false;
        
        // 显示成功消息
        this.$message.success('文件定义创建成功');
        
        // 重新获取列表
        this.fetchFileDefinitions();
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        this.$message.error('文件定义创建失败');
        console.error('Failed to create file definition:', error);
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
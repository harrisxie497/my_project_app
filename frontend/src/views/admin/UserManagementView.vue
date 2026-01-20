<template>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="section-title">用户管理</div>
        <div class="muted">创建用户、启用/禁用、重置密码</div>
      </div>
      <div style="display:flex; gap:8px;">
        <el-button type="primary" @click="openAddUserDialog">新增用户</el-button>
      </div>
    </div>
    <div class="card-bd">
      <el-table :data="users" style="width:100%;">
        <el-table-column prop="username" label="username" width="180"></el-table-column>
        <el-table-column prop="display_name" label="display_name" width="180"></el-table-column>
        <el-table-column prop="role" label="role" width="140">
          <template #default="{row}">
            <el-tag v-if="row.role==='admin'" type="warning">admin</el-tag>
            <el-tag v-else>operator</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="enabled" label="enabled" width="140">
          <template #default="{row}"><el-switch v-model="row.enabled"></el-switch></template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="{row}">
            <el-button size="small" @click="openResetPasswordDialog(row)">重置密码</el-button>
            <el-button size="small" type="danger" plain @click="deleteUser(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增用户弹窗 -->
    <el-dialog
      v-model="addDialogVisible"
      title="新增用户"
      width="640px"
      :close-on-click-modal="false"
    >
      <el-form ref="addFormRef" :model="addForm" label-position="top" :rules="addFormRules">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="addForm.username" placeholder="请输入用户名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="显示名称" prop="display_name">
              <el-input v-model="addForm.display_name" placeholder="请输入显示名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="addForm.role" placeholder="请选择角色" style="width:100%;">
                <el-option label="管理员" value="admin" />
                <el-option label="操作员" value="operator" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="初始密码" prop="password">
              <el-input v-model="addForm.password" type="password" placeholder="请输入初始密码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="启用状态">
          <el-switch v-model="addForm.enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddUser">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 重置密码弹窗 -->
    <el-dialog
      v-model="resetDialogVisible"
      title="重置密码"
      width="540px"
      :close-on-click-modal="false"
    >
      <el-form ref="resetFormRef" :model="resetForm" label-position="top" :rules="resetFormRules">
        <el-form-item label="用户名" disabled>
          <el-input v-model="resetForm.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item label="新密码" prop="password">
          <el-input v-model="resetForm.password" type="password" placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="resetForm.confirmPassword" type="password" placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="resetDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleResetPassword">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const users = ref([
  { id: "u_123", username: "admin", display_name: "Admin", role: "admin", enabled: true },
  { id: "u_200", username: "op1", display_name: "操作员1", role: "operator", enabled: true },
]);

// 新增用户弹窗相关
const addDialogVisible = ref(false);
const addFormRef = ref(null);
const addForm = reactive({
  username: '',
  display_name: '',
  role: 'operator',
  password: '',
  enabled: true
});

const addFormRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  display_name: [
    { required: true, message: '请输入显示名称', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入初始密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
});

const openAddUserDialog = () => {
  addDialogVisible.value = true;
};

const handleAddUser = () => {
  addFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟提交
      const newUser = {
        id: `u_${Date.now()}`,
        ...addForm
      };
      users.value.push(newUser);
      addDialogVisible.value = false;
      // 重置表单
      addFormRef.value.resetFields();
      ElMessage.success('用户创建成功');
    }
  });
};

// 重置密码弹窗相关
const resetDialogVisible = ref(false);
const resetFormRef = ref(null);
const resetForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

const resetFormRules = reactive({
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== resetForm.password) {
          callback(new Error('两次输入的密码不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
});

const openResetPasswordDialog = (row) => {
  resetForm.username = row.username;
  resetForm.password = '';
  resetForm.confirmPassword = '';
  resetDialogVisible.value = true;
};

const handleResetPassword = () => {
  resetFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟重置密码
      resetDialogVisible.value = false;
      ElMessage.success('密码重置成功');
    }
  });
};

// 删除用户
const deleteUser = (row) => {
  // 模拟删除
  users.value = users.value.filter(user => user.id !== row.id);
  ElMessage.success('用户删除成功');
};
</script>

<style scoped>
.card { background:#fff; border:1px solid #eaecef; border-radius: 14px; }
.card-hd { padding: 14px 14px 0 14px; display:flex; align-items:center; justify-content:space-between; gap: 12px; }
.card-bd { padding: 14px; }
.muted { color:#6b7280; }
.section-title { font-weight: 800; margin: 0 0 10px; }
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
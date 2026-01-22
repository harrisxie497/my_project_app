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
          <template #default="{row}"><el-switch :model-value="row.enabled" @change="toggleUserEnabled(row, $event)"></el-switch></template>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import userService from '../../services/userService'

const users = ref([]);

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

// 重置密码弹窗相关
const resetDialogVisible = ref(false);
const resetFormRef = ref(null);
const resetForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  userId: ''
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

// 加载用户列表
const loadUsers = async () => {
  try {
    const response = await userService.getUsers();
    users.value = response.data.items;
  } catch (error) {
    console.error('获取用户列表错误:', error);
    ElMessage.error('获取用户列表失败');
  }
};

// 打开新增用户弹窗
const openAddUserDialog = () => {
  addDialogVisible.value = true;
};

// 新增用户
const handleAddUser = async () => {
  addFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await userService.createUser(addForm);
        addDialogVisible.value = false;
        // 重置表单
        addFormRef.value.resetFields();
        ElMessage.success('用户创建成功');
        // 重新加载用户列表
        await loadUsers();
      } catch (error) {
        console.error('创建用户错误:', error);
        ElMessage.error('用户创建失败');
      }
    }
  });
};

// 打开重置密码弹窗
const openResetPasswordDialog = (row) => {
  resetForm.username = row.username;
  resetForm.userId = row.id;
  resetForm.password = '';
  resetForm.confirmPassword = '';
  resetDialogVisible.value = true;
};

// 重置密码
const handleResetPassword = async () => {
  resetFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await userService.adminResetPassword(resetForm.userId, resetForm.password);
        resetDialogVisible.value = false;
        ElMessage.success('密码重置成功');
      } catch (error) {
        console.error('重置密码错误:', error);
        ElMessage.error('密码重置失败');
      }
    }
  });
};

// 删除用户
const deleteUser = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    const response = await userService.deleteUser(row.id);
    ElMessage.success('用户删除成功');
    // 重新加载用户列表
    await loadUsers();
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消删除
      return;
    }
    console.error('删除用户错误:', error);
    ElMessage.error('用户删除失败');
  }
};

// 切换用户启用状态
const toggleUserEnabled = async (row, newEnabled) => {
  try {
    // 使用$event参数获取新的状态，而不是依赖row.enabled
    const response = await (newEnabled ? userService.enableUser(row.id) : userService.disableUser(row.id));
    
    // 直接使用response数据，因为axios拦截器已经处理了response.data
    ElMessage.success(newEnabled ? '用户启用成功' : '用户禁用成功');
    // 重新加载用户列表
    await loadUsers();
  } catch (error) {
    console.error('切换用户状态错误:', error);
    // 恢复原状态，因为我们使用了:model-value而不是v-model
    // 所以需要手动更新UI
    await loadUsers();
    ElMessage.error(newEnabled ? '用户启用失败' : '用户禁用失败');
  }
};

// 组件挂载时加载用户列表
onMounted(async () => {
  await loadUsers();
});
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
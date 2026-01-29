import axios from '../utils/axios';

// 用户管理相关API
const userService = {
  // 获取用户列表
  getUsers(params = {}) {
    return axios.get('/users/', { params });
  },

  // 创建用户
  createUser(data) {
    return axios.post('/users/', data);
  },

  // 获取用户详情
  getUserDetail(id) {
    return axios.get(`/users/${id}`);
  },

  // 更新用户信息
  updateUser(id, data) {
    return axios.put(`/users/${id}`, data);
  },

  // 删除用户
  deleteUser(id) {
    return axios.delete(`/users/${id}`);
  },

  // 启用用户
  enableUser(id) {
    return axios.put(`/users/${id}/enable`);
  },

  // 禁用用户
  disableUser(id) {
    return axios.put(`/users/${id}/disable`);
  },

  // 管理员获取用户列表
  adminGetUsers() {
    return axios.get('/admin/users/');
  },

  // 管理员创建用户
  adminCreateUser(data) {
    return axios.post('/admin/users/', data);
  },

  // 管理员启用/禁用用户
  adminEnableDisableUser(id, enabled) {
    return axios.put(`/admin/users/${id}`, { enabled });
  },

  // 管理员重置用户密码
  adminResetPassword(id, newPassword) {
    return axios.post(`/admin/users/${id}/reset-password`, { new_password: newPassword });
  }
};

export default userService;
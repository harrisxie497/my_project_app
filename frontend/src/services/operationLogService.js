import axios from '../utils/axios';

// 操作日志相关API
const operationLogService = {
  // 获取操作日志列表
  getOperationLogs(params = {}) {
    return axios.get('/api/v1/operation-logs', { params });
  },

  // 获取指定用户的操作日志
  getOperationLogsByUser(userId, params = {}) {
    return axios.get(`/api/v1/operation-logs/user/${userId}`, { params });
  },

  // 获取指定操作类型的操作日志
  getOperationLogsByAction(action, params = {}) {
    return axios.get(`/api/v1/operation-logs/action/${action}`, { params });
  },

  // 管理员获取操作日志列表
  adminGetOperationLogs(params = {}) {
    return axios.get('/api/v1/admin/operation-logs', { params });
  }
};

export default operationLogService;

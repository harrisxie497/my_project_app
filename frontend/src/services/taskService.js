import axios from '../utils/axios';

// 任务相关API
const taskService = {
  // 获取任务列表
  getTasks(params) {
    return axios.get('/tasks', { params });
  },

  // 获取任务详情
  getTaskDetail(taskId) {
    return axios.get(`/tasks/${taskId}`);
  },

  // 创建任务
  createTask(data) {
    return axios.post('/tasks', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 运行任务
  runTask(taskId) {
    return axios.post(`/tasks/${taskId}/run`);
  },

  // 获取任务对比统计
  getTaskStats(taskId) {
    return axios.get(`/tasks/${taskId}/stats`);
  },

  // 下载任务文件
  downloadTaskFile(taskId, fileType) {
    return axios.get(`/tasks/${taskId}/files/${fileType}`, { responseType: 'blob' });
  },

  // 删除任务
  deleteTask(taskId) {
    return axios.delete(`/tasks/${taskId}`);
  }
};

export default taskService;

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
    return axios.post('/tasks', data);
  },

  // 下载任务文件
  downloadTaskFile(taskId, fileType) {
    return axios.get(`/tasks/${taskId}/download/${fileType}`, { responseType: 'blob' });
  },

  // 删除任务
  deleteTask(taskId) {
    return axios.delete(`/tasks/${taskId}`);
  }
};

export default taskService;

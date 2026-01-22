import axios from '../utils/axios';

// AI能力配置相关API
const aiCapabilityService = {
  // 获取AI能力配置列表
  getAICapabilities() {
    return axios.get('/api/v1/ai-capabilities/');
  },

  // 获取AI能力配置详情
  getAICapabilityDetail(id) {
    return axios.get(`/api/v1/ai-capabilities/${id}`);
  },

  // 新增AI能力配置
  addAICapability(data) {
    return axios.post('/api/v1/ai-capabilities/', data);
  },

  // 更新AI能力配置
  updateAICapability(id, data) {
    return axios.put(`/api/v1/ai-capabilities/${id}`, data);
  },

  // 删除AI能力配置
  deleteAICapability(id) {
    return axios.delete(`/api/v1/ai-capabilities/${id}`);
  },

  // 启用AI能力配置
  enableAICapability(id) {
    return axios.put(`/api/v1/ai-capabilities/${id}/enable`);
  },

  // 禁用AI能力配置
  disableAICapability(id) {
    return axios.put(`/api/v1/ai-capabilities/${id}/disable`);
  }
};

export default aiCapabilityService;

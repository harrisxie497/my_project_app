import axios from '../utils/axios';

// AI能力配置相关API
const aiCapabilityService = {
  // 获取AI能力配置列表
  getAICapabilities() {
    return axios.get('/ai-capabilities');
  },

  // 获取AI能力配置详情
  getAICapabilityDetail(id) {
    return axios.get(`/ai-capabilities/${id}`);
  },

  // 新增AI能力配置
  addAICapability(data) {
    return axios.post('/ai-capabilities', data);
  },

  // 更新AI能力配置
  updateAICapability(id, data) {
    return axios.put(`/ai-capabilities/${id}`, data);
  },

  // 删除AI能力配置
  deleteAICapability(id) {
    return axios.delete(`/ai-capabilities/${id}`);
  },

  // 更新AI能力配置状态
  updateCapabilityStatus(id, enabled) {
    return axios.patch(`/ai-capabilities/${id}/status`, { enabled });
  }
};

export default aiCapabilityService;

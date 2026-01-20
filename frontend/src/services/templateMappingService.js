import axios from '../utils/axios';

// 模板映射相关API
const templateMappingService = {
  // 获取模板映射列表
  getTemplateMappings() {
    return axios.get('/template-mappings');
  },

  // 获取模板映射详情
  getTemplateMappingDetail(id) {
    return axios.get(`/template-mappings/${id}`);
  },

  // 新增模板映射
  addTemplateMapping(data) {
    return axios.post('/template-mappings', data);
  },

  // 更新模板映射
  updateTemplateMapping(id, data) {
    return axios.put(`/template-mappings/${id}`, data);
  },

  // 删除模板映射
  deleteTemplateMapping(id) {
    return axios.delete(`/template-mappings/${id}`);
  },

  // 更新模板映射状态
  updateMappingStatus(id, enabled) {
    return axios.patch(`/template-mappings/${id}/status`, { enabled });
  }
};

export default templateMappingService;

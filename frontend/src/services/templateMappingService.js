import axios from '../utils/axios';

// 模板映射相关API
const templateMappingService = {
  // 获取模板映射列表
  getTemplateMappings() {
    return axios.get('/api/v1/template-mappings/');
  },

  // 获取模板映射详情
  getTemplateMappingDetail(id) {
    return axios.get(`/api/v1/template-mappings/${id}`);
  },

  // 新增模板映射
  addTemplateMapping(data) {
    return axios.post('/api/v1/template-mappings/', data);
  },

  // 更新模板映射
  updateTemplateMapping(id, data) {
    return axios.put(`/api/v1/template-mappings/${id}`, data);
  },

  // 删除模板映射
  deleteTemplateMapping(id) {
    return axios.delete(`/api/v1/template-mappings/${id}`);
  },

  // 启用模板映射
  enableTemplateMapping(id) {
    return axios.put(`/api/v1/template-mappings/${id}/enable`);
  },

  // 禁用模板映射
  disableTemplateMapping(id) {
    return axios.put(`/api/v1/template-mappings/${id}/disable`);
  },

  // 模板映射自检
  validateTemplateMapping(id) {
    return axios.post(`/api/v1/admin/template-mappings/${id}/validate`);
  }
};

export default templateMappingService;

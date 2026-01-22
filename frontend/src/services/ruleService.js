import axios from '../utils/axios';

// 规则配置相关API
const ruleService = {
  // 获取规则表列表
  getRuleTables() {
    return axios.get('/api/v1/rule-tables/');
  },

  // 获取规则表详情
  getRuleTableDetail(tableId) {
    return axios.get(`/api/v1/rule-tables/${tableId}`);
  },

  // 获取规则项列表
  getRuleItems(ruleTableId) {
    return axios.get(`/api/v1/rule-tables/${ruleTableId}/rule-items/`);
  },

  // 导入规则模板
  importRuleTemplate(formData) {
    return axios.post('/api/v1/admin/rules/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 新增规则项
  addRuleItem(data) {
    return axios.post('/api/v1/rule-items/', data);
  },

  // 更新规则项
  updateRuleItem(id, data) {
    return axios.put(`/api/v1/rule-items/${id}`, data);
  },

  // 删除规则项
  deleteRuleItem(id) {
    return axios.delete(`/api/v1/rule-items/${id}`);
  },

  // 启用规则项
  enableRuleItem(id) {
    return axios.put(`/api/v1/rule-items/${id}/enable`);
  },

  // 禁用规则项
  disableRuleItem(id) {
    return axios.put(`/api/v1/rule-items/${id}/disable`);
  }
};

export default ruleService;

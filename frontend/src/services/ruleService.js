import axios from '../utils/axios';

// 规则配置相关API
const ruleService = {
  // 获取规则表列表
  getRuleTables() {
    return axios.get('/rules/tables');
  },

  // 获取规则表详情
  getRuleTableDetail(tableCode) {
    return axios.get(`/rules/tables/${tableCode}`);
  },

  // 获取规则项列表
  getRuleItems(tableCode) {
    return axios.get(`/rules/items`, { params: { table_code: tableCode } });
  },

  // 导入规则模板
  importRuleTemplate(formData) {
    return axios.post('/rules/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 新增规则项
  addRuleItem(data) {
    return axios.post('/rules/items', data);
  },

  // 更新规则项
  updateRuleItem(id, data) {
    return axios.put(`/rules/items/${id}`, data);
  },

  // 删除规则项
  deleteRuleItem(id) {
    return axios.delete(`/rules/items/${id}`);
  }
};

export default ruleService;

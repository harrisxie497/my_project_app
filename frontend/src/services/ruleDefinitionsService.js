import axios from '../utils/axios';

// 规则定义相关API
const ruleDefinitionsService = {
  /**
   * 获取规则定义列表
   * @param {Object} params - 查询参数
   * @param {string} params.rule_type - 规则类型过滤
   * @param {string} params.executor_type - 执行器类型过滤
   * @param {boolean} params.enabled - 启用状态过滤
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页条数
   * @returns {Promise} - 返回规则定义列表
   */
  getRuleDefinitions(params = {}) {
    return axios.get('/rule-definitions', { params });
  },

  /**
   * 创建规则定义
   * @param {Object} data - 规则定义数据
   * @returns {Promise} - 返回创建的规则定义
   */
  createRuleDefinition(data) {
    return axios.post('/rule-definitions', data);
  },

  /**
   * 获取单个规则定义
   * @param {string} id - 规则定义ID
   * @returns {Promise} - 返回规则定义详情
   */
  getRuleDefinitionDetail(id) {
    return axios.get(`/rule-definitions/${id}`);
  },

  /**
   * 更新规则定义
   * @param {string} id - 规则定义ID
   * @param {Object} data - 更新的数据
   * @returns {Promise} - 返回更新后的规则定义
   */
  updateRuleDefinition(id, data) {
    return axios.put(`/rule-definitions/${id}`, data);
  },

  /**
   * 删除规则定义
   * @param {string} id - 规则定义ID
   * @returns {Promise} - 返回删除结果
   */
  deleteRuleDefinition(id) {
    return axios.delete(`/rule-definitions/${id}`);
  },

  /**
   * 启用/禁用规则定义
   * @param {string} id - 规则定义ID
   * @param {boolean} enabled - 启用状态
   * @returns {Promise} - 返回更新后的规则定义
   */
  updateRuleDefinitionStatus(id, enabled) {
    return axios.patch(`/rule-definitions/${id}/status`, null, {
      params: { enabled }
    });
  }
};

export default ruleDefinitionsService;
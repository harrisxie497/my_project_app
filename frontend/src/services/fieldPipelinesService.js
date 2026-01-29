import axios from '../utils/axios';

// 字段映射相关API
const fieldPipelinesService = {
  /**
   * 获取字段映射列表
   * @param {Object} params - 查询参数
   * @param {string} params.file_ref - 文件引用标识过滤
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页条数
   * @returns {Promise} - 返回字段映射列表
   */
  getFieldPipelines(params = {}) {
    return axios.get('/field-pipelines', { params });
  },

  /**
   * 创建字段映射
   * @param {Object} data - 字段映射数据
   * @returns {Promise} - 返回创建的字段映射
   */
  createFieldPipeline(data) {
    return axios.post('/field-pipelines', data);
  },

  /**
   * 获取单个字段映射
   * @param {string} id - 字段映射ID
   * @returns {Promise} - 返回字段映射详情
   */
  getFieldPipelineDetail(id) {
    return axios.get(`/field-pipelines/${id}`);
  },

  /**
   * 更新字段映射
   * @param {string} id - 字段映射ID
   * @param {Object} data - 更新的数据
   * @returns {Promise} - 返回更新后的字段映射
   */
  updateFieldPipeline(id, data) {
    return axios.put(`/field-pipelines/${id}`, data);
  },

  /**
   * 删除字段映射
   * @param {string} id - 字段映射ID
   * @returns {Promise} - 返回删除结果
   */
  deleteFieldPipeline(id) {
    return axios.delete(`/field-pipelines/${id}`);
  },

  /**
   * 更新字段映射的规则顺序
   * @param {string} id - 字段映射ID
   * @param {Array} rules_order - 规则顺序列表
   * @returns {Promise} - 返回更新后的字段映射
   */
  updateFieldPipelineRulesOrder(id, rules_order) {
    return axios.put(`/field-pipelines/${id}/rules-order`, { rules_order });
  },

  /**
   * 启用/禁用字段映射
   * @param {string} id - 字段映射ID
   * @param {boolean} enabled - 启用状态
   * @returns {Promise} - 返回更新后的字段映射
   */
  updateFieldPipelineStatus(id, enabled) {
    return axios.patch(`/field-pipelines/${id}/status`, null, {
      params: { enabled }
    });
  }
};

export default fieldPipelinesService;
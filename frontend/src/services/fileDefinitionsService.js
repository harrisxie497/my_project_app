import axios from '../utils/axios';

// 文件定义相关API
const fileDefinitionsService = {
  /**
   * 获取文件定义列表
   * @param {Object} params - 查询参数
   * @param {string} params.file_type - 文件类型过滤
   * @param {number} params.page - 页码
   * @param {number} params.page_size - 每页条数
   * @returns {Promise} - 返回文件定义列表
   */
  getFileDefinitions(params = {}) {
    return axios.get('/file-definitions', { params });
  },

  /**
   * 创建文件定义
   * @param {Object} data - 文件定义数据
   * @returns {Promise} - 返回创建的文件定义
   */
  createFileDefinition(data) {
    return axios.post('/file-definitions', data);
  },

  /**
   * 获取单个文件定义
   * @param {string} id - 文件定义ID
   * @returns {Promise} - 返回文件定义详情
   */
  getFileDefinitionDetail(id) {
    return axios.get(`/file-definitions/${id}`);
  },

  /**
   * 更新文件定义
   * @param {string} id - 文件定义ID
   * @param {Object} data - 更新的数据
   * @returns {Promise} - 返回更新后的文件定义
   */
  updateFileDefinition(id, data) {
    return axios.put(`/file-definitions/${id}`, data);
  },

  /**
   * 删除文件定义
   * @param {string} id - 文件定义ID
   * @returns {Promise} - 返回删除结果
   */
  deleteFileDefinition(id) {
    return axios.delete(`/file-definitions/${id}`);
  },

  /**
   * 启用/禁用文件定义
   * @param {string} id - 文件定义ID
   * @param {boolean} enabled - 启用状态
   * @returns {Promise} - 返回更新后的文件定义
   */
  updateFileDefinitionStatus(id, enabled) {
    return axios.patch(`/file-definitions/${id}/status`, null, {
      params: { enabled }
    });
  }
};

export default fileDefinitionsService;
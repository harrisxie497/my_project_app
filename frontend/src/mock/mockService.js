import axios from '../utils/axios';
import { mockTasks, mockTaskDetail, mockRuleTables, mockTemplateMappings, mockAICapabilities } from './mockData';

// Mock服务配置
class MockService {
  constructor() {
    this.setupMock();
  }

  // 设置mock拦截器
  setupMock() {
    // 使用axios拦截器实现mock
    axios.interceptors.request.use(config => {
      // 根据请求URL返回对应的mock数据
      const response = this.getMockResponse(config);
      if (response) {
        // 返回mock数据，模拟API响应延迟
        return new Promise(resolve => {
          setTimeout(() => {
            resolve({ data: response });
          }, 300 + Math.random() * 500); // 300-800ms随机延迟
        });
      }
      return config;
    }, error => {
      return Promise.reject(error);
    });
  }

  // 根据请求获取mock响应
  getMockResponse(config) {
    const { url, method } = config;

    // 任务相关API
    if (url === '/api/tasks' && method === 'get') {
      return this.mockGetTasks(config);
    }

    if (url.startsWith('/api/tasks/') && url.endsWith('/download/original') && method === 'get') {
      return this.mockDownloadFile('original');
    }

    if (url.startsWith('/api/tasks/') && url.endsWith('/download/result') && method === 'get') {
      return this.mockDownloadFile('result');
    }

    if (url.startsWith('/api/tasks/') && url.endsWith('/download/diff') && method === 'get') {
      return this.mockDownloadFile('diff');
    }

    if (url.startsWith('/api/tasks/') && url.endsWith('/download/stats') && method === 'get') {
      return this.mockDownloadFile('stats');
    }

    if (url.startsWith('/api/tasks/') && method === 'get') {
      return this.mockGetTaskDetail(url);
    }

    if (url === '/api/tasks' && method === 'post') {
      return this.mockCreateTask(config);
    }

    // 规则相关API
    if (url === '/api/rules/tables' && method === 'get') {
      return this.mockGetRuleTables();
    }

    // 模板映射相关API
    if (url === '/api/template-mappings' && method === 'get') {
      return this.mockGetTemplateMappings();
    }

    if (url === '/api/template-mappings' && method === 'post') {
      return this.mockAddTemplateMapping(config);
    }

    if (url.startsWith('/api/template-mappings/') && method === 'patch') {
      return this.mockUpdateMappingStatus(url, config);
    }

    // AI能力配置相关API
    if (url === '/api/ai-capabilities' && method === 'get') {
      return this.mockGetAICapabilities();
    }

    if (url === '/api/ai-capabilities' && method === 'post') {
      return this.mockAddAICapability(config);
    }

    if (url.startsWith('/api/ai-capabilities/') && method === 'patch') {
      return this.mockUpdateCapabilityStatus(url, config);
    }

    return null; // 不拦截，正常请求
  }

  // 模拟获取任务列表
  mockGetTasks(config) {
    const { params } = config;
    let filteredTasks = [...mockTasks];

    // 应用过滤条件
    if (params?.file_type) {
      filteredTasks = filteredTasks.filter(task => task.file_type === params.file_type);
    }

    if (params?.status) {
      filteredTasks = filteredTasks.filter(task => task.status === params.status);
    }

    if (params?.unique_code) {
      filteredTasks = filteredTasks.filter(task => 
        task.unique_code.includes(params.unique_code)
      );
    }

    return {
      code: 200,
      message: 'success',
      data: {
        list: filteredTasks,
        total: filteredTasks.length
      }
    };
  }

  // 模拟获取任务详情
  mockGetTaskDetail(url) {
    const taskId = url.split('/')[3];
    return {
      code: 200,
      message: 'success',
      data: {
        ...mockTaskDetail,
        id: taskId
      }
    };
  }

  // 模拟创建任务
  mockCreateTask(config) {
    const { data } = config;
    const newTask = {
      id: `t_${String(Math.floor(Math.random() * 9000 + 1000))}`,
      file_type: data.file_type,
      unique_code: data.unique_code || `UC_${Date.now()}`,
      flight_no: data.file_type === 'customs' ? (data.flight_no || 'NH000') : '',
      declare_date: data.file_type === 'customs' ? (data.declare_date || '2026-01-20') : '',
      status: 'queued',
      created_at: new Date().toISOString()
    };

    return {
      code: 200,
      message: '任务创建成功',
      data: newTask
    };
  }

  // 模拟下载文件
  mockDownloadFile(fileType) {
    return {
      code: 200,
      message: 'success',
      data: {
        url: `/mock/files/${fileType}.xlsx`
      }
    };
  }

  // 模拟获取规则表列表
  mockGetRuleTables() {
    return {
      code: 200,
      message: 'success',
      data: {
        list: mockRuleTables,
        total: mockRuleTables.length
      }
    };
  }

  // 模拟获取模板映射列表
  mockGetTemplateMappings() {
    return {
      code: 200,
      message: 'success',
      data: {
        list: mockTemplateMappings,
        total: mockTemplateMappings.length
      }
    };
  }

  // 模拟新增模板映射
  mockAddTemplateMapping(config) {
    const { data } = config;
    const newMapping = {
      id: `tm_${String(Math.floor(Math.random() * 9000 + 1000))}`,
      ...data,
      enabled: data.enabled !== undefined ? data.enabled : true
    };

    return {
      code: 200,
      message: '新增模板映射成功',
      data: newMapping
    };
  }

  // 模拟更新模板映射状态
  mockUpdateMappingStatus(url, config) {
    const mappingId = url.split('/')[3];
    const { enabled } = config.data;

    return {
      code: 200,
      message: '更新状态成功',
      data: {
        id: mappingId,
        enabled
      }
    };
  }

  // 模拟获取AI能力配置列表
  mockGetAICapabilities() {
    return {
      code: 200,
      message: 'success',
      data: {
        list: mockAICapabilities,
        total: mockAICapabilities.length
      }
    };
  }

  // 模拟新增AI能力配置
  mockAddAICapability(config) {
    const { data } = config;
    const newCapability = {
      id: `aic_${String(Math.floor(Math.random() * 9000 + 1000))}`,
      ...data,
      enabled: data.enabled !== undefined ? data.enabled : true
    };

    return {
      code: 200,
      message: '新增AI配置成功',
      data: newCapability
    };
  }

  // 模拟更新AI能力配置状态
  mockUpdateCapabilityStatus(url, config) {
    const capabilityId = url.split('/')[3];
    const { enabled } = config.data;

    return {
      code: 200,
      message: '更新状态成功',
      data: {
        id: capabilityId,
        enabled
      }
    };
  }
}

// 初始化mock服务
const mockService = new MockService();
export default mockService;

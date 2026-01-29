const axios = require('axios');

// API配置
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 测试报告
const testReport = {
  totalTests: 0,
  passedTests: 0,
  failedTests: 0,
  results: []
};

// 获取认证令牌
async function getAuthToken() {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, 
      new URLSearchParams({
        username: 'admin',
        password: 'admin123'
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    return response.data.data.access_token;
  } catch (error) {
    console.error('获取认证令牌失败:', error.response?.data || error.message);
    return null;
  }
}

// 测试函数
async function testApi(endpoint, method = 'get', data = null, params = null, token = null) {
  testReport.totalTests++;
  const startTime = Date.now();
  
  try {
    const config = {
      method,
      url: `${API_BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      },
      data,
      params,
    };
    
    const response = await axios(config);
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    testReport.passedTests++;
    testReport.results.push({
      endpoint,
      method,
      status: 'PASS',
      statusCode: response.status,
      duration: `${duration}ms`,
      message: 'API call successful'
    });
    
    console.log(`✅ ${method.toUpperCase()} ${endpoint} - ${response.status} (${duration}ms)`);
    return response;
  } catch (error) {
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    testReport.failedTests++;
    testReport.results.push({
      endpoint,
      method,
      status: 'FAIL',
      statusCode: error.response?.status || 'N/A',
      duration: `${duration}ms`,
      message: error.response?.data?.detail || error.message
    });
    
    console.log(`❌ ${method.toUpperCase()} ${endpoint} - ${error.response?.status || 'ERROR'} (${duration}ms)`);
    console.log(`   Error: ${error.response?.data?.detail || error.message}`);
    return null;
  }
}

// 运行所有测试
async function runTests() {
  console.log('开始测试配置相关API...\n');
  
  // 获取认证令牌
  console.log('=== 获取认证令牌 ===');
  const token = await getAuthToken();
  if (!token) {
    console.error('无法获取认证令牌，测试终止');
    return;
  }
  console.log('✅ 成功获取认证令牌\n');
  
  // 测试文件定义API
  console.log('=== 测试文件定义API ===');
  await testApi('/admin/file-definitions', 'get', null, { page: 1, page_size: 10 }, token);
  await testApi('/file-definitions', 'get', null, { page: 1, page_size: 10 }, token);
  
  // 测试字段映射API
  console.log('\n=== 测试字段映射API ===');
  await testApi('/admin/field-pipelines', 'get', null, { page: 1, page_size: 10 }, token);
  await testApi('/field-pipelines', 'get', null, { page: 1, page_size: 10 }, token);
  
  // 测试规则定义API
  console.log('\n=== 测试规则定义API ===');
  await testApi('/admin/rule-definitions', 'get', null, { page: 1, page_size: 10 }, token);
  await testApi('/rule-definitions', 'get', null, { page: 1, page_size: 10 }, token);
  
  // 输出测试报告
  console.log('\n' + '='.repeat(50));
  console.log('测试报告');
  console.log('='.repeat(50));
  console.log(`总测试数: ${testReport.totalTests}`);
  console.log(`通过测试: ${testReport.passedTests}`);
  console.log(`失败测试: ${testReport.failedTests}`);
  console.log(`通过率: ${((testReport.passedTests / testReport.totalTests) * 100).toFixed(2)}%`);
  
  console.log('\n详细结果:');
  testReport.results.forEach((result, index) => {
    console.log(`${index + 1}. ${result.method.toUpperCase()} ${result.endpoint}`);
    console.log(`   状态: ${result.status} (${result.statusCode})`);
    console.log(`   耗时: ${result.duration}`);
    console.log(`   消息: ${result.message}`);
  });
  
  console.log('\n测试完成！');
}

// 执行测试
runTests();

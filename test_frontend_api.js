// 模拟前端API请求测试
const axios = require('axios');

// 创建axios实例，完全模拟前端配置
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加响应拦截器，模拟前端处理
instance.interceptors.response.use(
  response => {
    // 对于blob类型的响应，直接返回response，否则返回response.data
    if (response.config.responseType === 'blob') {
      return response;
    }
    return response.data;
  },
  error => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// 先登录获取token
async function login() {
  console.log('=== 测试登录API ===');
  try {
    // 使用表单数据，因为后端使用OAuth2PasswordRequestForm
    const response = await instance.post('/auth/login', {
      username: 'admin',
      password: 'admin123'
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      transformRequest: [(data) => {
        // 将JSON转换为表单数据格式
        return Object.keys(data)
          .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key])}`)
          .join('&');
      }]
    });
    
    console.log('登录响应:', JSON.stringify(response, null, 2));
    
    if (response.ok && response.data.access_token) {
      console.log('登录成功，获取到token');
      return response.data.access_token;
    } else {
      console.log('登录失败，响应结构不符合预期');
      return null;
    }
  } catch (error) {
    console.log('登录失败:', error.message);
    if (error.response) {
      console.log('登录失败状态码:', error.response.status);
      console.log('登录失败响应:', JSON.stringify(error.response.data, null, 2));
    }
    return null;
  }
}

// 模拟前端页面调用API
async function testFileDefinitions(token) {
  console.log('\n=== 测试文件定义API ===');
  try {
    const response = await instance.get('/file-definitions', {
      params: {
        page: 1,
        page_size: 20
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    console.log('响应状态:', '成功');
    console.log('响应结构:', JSON.stringify(response, null, 2));
    
    // 模拟前端页面处理
    if (response.ok) {
      console.log('前端处理:');
      console.log('  items:', response.data.items ? `${response.data.items.length} 条` : 'undefined');
      console.log('  total:', response.data.total);
      return true;
    } else {
      console.log('前端处理: 响应失败');
      return false;
    }
    
  } catch (error) {
    console.log('响应状态:', '失败');
    console.log('错误信息:', error.message);
    if (error.response) {
      console.log('响应状态码:', error.response.status);
      console.log('响应数据:', JSON.stringify(error.response.data, null, 2));
    }
    return false;
  }
}

// 测试字段映射API
async function testFieldPipelines(token) {
  console.log('\n=== 测试字段映射API ===');
  try {
    const response = await instance.get('/field-pipelines', {
      params: {
        page: 1,
        page_size: 20
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    console.log('响应状态:', '成功');
    console.log('响应结构:', JSON.stringify(response, null, 2));
    
    // 模拟前端页面处理
    if (response.ok) {
      console.log('前端处理:');
      console.log('  items:', response.data.items ? `${response.data.items.length} 条` : 'undefined');
      console.log('  total:', response.data.total);
      return true;
    } else {
      console.log('前端处理: 响应失败');
      return false;
    }
    
  } catch (error) {
    console.log('响应状态:', '失败');
    console.log('错误信息:', error.message);
    if (error.response) {
      console.log('响应状态码:', error.response.status);
      console.log('响应数据:', JSON.stringify(error.response.data, null, 2));
    }
    return false;
  }
}

// 测试规则定义API
async function testRuleDefinitions(token) {
  console.log('\n=== 测试规则定义API ===');
  try {
    const response = await instance.get('/rule-definitions', {
      params: {
        page: 1,
        page_size: 20
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    console.log('响应状态:', '成功');
    console.log('响应结构:', JSON.stringify(response, null, 2));
    
    // 模拟前端页面处理
    if (response.ok) {
      console.log('前端处理:');
      console.log('  items:', response.data.items ? `${response.data.items.length} 条` : 'undefined');
      console.log('  total:', response.data.total);
      return true;
    } else {
      console.log('前端处理: 响应失败');
      return false;
    }
    
  } catch (error) {
    console.log('响应状态:', '失败');
    console.log('错误信息:', error.message);
    if (error.response) {
      console.log('响应状态码:', error.response.status);
      console.log('响应数据:', JSON.stringify(error.response.data, null, 2));
    }
    return false;
  }
}

// 运行测试
async function runAllTests() {
  // 先登录获取token
  const token = await login();
  if (!token) {
    console.log('\n=== 测试失败：无法获取有效的token ===');
    return;
  }
  
  // 测试所有配置相关API
  const testResults = {
    fileDefinitions: await testFileDefinitions(token),
    fieldPipelines: await testFieldPipelines(token),
    ruleDefinitions: await testRuleDefinitions(token)
  };
  
  // 输出测试总结
  console.log('\n=== 测试总结 ===');
  console.log('文件定义API:', testResults.fileDefinitions ? '✅ 成功' : '❌ 失败');
  console.log('字段映射API:', testResults.fieldPipelines ? '✅ 成功' : '❌ 失败');
  console.log('规则定义API:', testResults.ruleDefinitions ? '✅ 成功' : '❌ 失败');
  
  // 检查是否所有测试都通过
  const allPassed = Object.values(testResults).every(result => result);
  console.log('\n整体测试结果:', allPassed ? '✅ 全部通过' : '❌ 部分失败');
}

runAllTests();

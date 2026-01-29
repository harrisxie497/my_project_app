// 测试用户管理API
const axios = require('axios');

// 创建axios实例
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加响应拦截器
instance.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// 先登录获取token
async function login() {
  try {
    const response = await instance.post('/auth/login', {
      username: 'admin',
      password: 'admin123'
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      transformRequest: [(data) => {
        return Object.keys(data)
          .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key])}`)
          .join('&');
      }]
    });
    
    if (response.ok && response.data.access_token) {
      return response.data.access_token;
    }
    return null;
  } catch (error) {
    console.log('登录失败:', error.message);
    return null;
  }
}

// 测试用户管理API - 带trailing slash
async function testUsersWithSlash(token) {
  console.log('\n=== 测试用户管理API（带trailing slash）===');
  try {
    const response = await instance.get('/users/', {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        page: 1,
        page_size: 20
      }
    });
    
    console.log('响应状态:', '成功');
    console.log('响应结构:', JSON.stringify(response, null, 2));
    
    if (response.ok) {
      console.log('获取用户列表成功');
      console.log('用户数量:', response.data.items ? response.data.items.length : 0);
      return true;
    } else {
      console.log('获取用户列表失败');
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

// 测试用户管理API - 不带trailing slash
async function testUsersWithoutSlash(token) {
  console.log('\n=== 测试用户管理API（不带trailing slash）===');
  try {
    const response = await instance.get('/users', {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        page: 1,
        page_size: 20
      }
    });
    
    console.log('响应状态:', '成功');
    console.log('响应结构:', JSON.stringify(response, null, 2));
    
    if (response.ok) {
      console.log('获取用户列表成功');
      console.log('用户数量:', response.data.items ? response.data.items.length : 0);
      return true;
    } else {
      console.log('获取用户列表失败');
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
async function runTests() {
  // 先登录获取token
  const token = await login();
  if (!token) {
    console.log('\n=== 测试失败：无法获取有效的token ===');
    return;
  }
  
  // 测试用户管理API
  await testUsersWithSlash(token);
  await testUsersWithoutSlash(token);
}

runTests();

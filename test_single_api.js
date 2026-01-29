const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000/api/v1';

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

// 测试API
async function testApi() {
  const token = await getAuthToken();
  if (!token) {
    console.error('无法获取认证令牌，测试终止');
    return;
  }
  console.log('成功获取认证令牌:', token);

  try {
    const response = await axios.get(`${API_BASE_URL}/admin/file-definitions`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        page: 1,
        page_size: 10
      }
    });
    console.log('API调用成功:', response.data);
  } catch (error) {
    console.error('API调用失败:', error.response?.data || error.message);
    console.error('完整错误信息:', error);
  }
}

testApi();

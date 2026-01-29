// 测试axios URL拼接
const axios = require('axios');

// 创建axios实例，模拟前端配置
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  timeout: 10000
});

// 测试不同URL格式的拼接结果
const testUrls = [
  '/file-definitions',    // 带斜杠前缀
  'file-definitions',     // 不带斜杠前缀
  '/admin/file-definitions', // 带/admin/前缀
  'admin/file-definitions'  // 带admin/前缀但没有斜杠
];

console.log('=== 测试URL拼接结果 ===');
testUrls.forEach(url => {
  // 使用axios的URL拼接逻辑
  const fullUrl = instance.defaults.baseURL + url.replace(/^\/+|\/+$/g, '');
  console.log(`baseURL + "${url}" = ${fullUrl}`);
});

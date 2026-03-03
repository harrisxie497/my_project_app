import axios from 'axios';

// 创建axios实例
const instance = axios.create({
  baseURL: '/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
instance.interceptors.request.use(
  config => {
    // 从本地存储获取token并添加到请求头
    const auth = localStorage.getItem('auth');
    console.log('请求拦截器 - auth:', auth);
    
    if (auth) {
      try {
        const authData = JSON.parse(auth);
        console.log('请求拦截器 - authData:', authData);
        if (authData.token) {
          config.headers.Authorization = `Bearer ${authData.token}`;
          console.log('请求拦截器 - 已添加 Authorization 头');
        }
      } catch (e) {
        console.error('请求拦截器 - 解析 auth 失败:', e);
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
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
    
    // 处理401未授权错误（登录过期或未登录）
    if (error.response && error.response.status === 401) {
      // 清除本地存储的认证信息
      localStorage.removeItem('auth');
      
      // 跳转到登录页面
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// 禁用axios的自动重定向，避免重定向时丢失Authorization头
instance.defaults.maxRedirects = 0;

export default instance;

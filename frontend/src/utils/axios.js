import axios from 'axios';

// 创建axios实例
const instance = axios.create({
  baseURL: '',
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
    if (auth) {
      const authData = JSON.parse(auth);
      if (authData.token) {
        config.headers.Authorization = `Bearer ${authData.token}`;
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
    return Promise.reject(error);
  }
);

// 禁用axios的自动重定向，避免重定向时丢失Authorization头
instance.defaults.maxRedirects = 0;

export default instance;

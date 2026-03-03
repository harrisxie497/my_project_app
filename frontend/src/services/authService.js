import axios from '../utils/axios';

// 认证相关API
const authService = {
  // 登录
  login(username, password) {
    // 创建一个新的 axios 实例，避免被全局配置影响
    const loginAxios = axios.create({
      baseURL: '/api/v1/',
      timeout: 10000
    });
    
    return loginAxios.post('/auth/login', {
      username,
      password
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      transformRequest: [(data) => {
        // 转换为form-urlencoded格式
        return Object.entries(data)
          .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
          .join('&');
      }]
    });
  },

  // 获取当前用户信息
  getMe() {
    return axios.get('/auth/me/');
  },

  // 登出
  logout() {
    return axios.post('/auth/logout/');
  },

  // 保存认证信息到本地存储
  saveAuth(authData) {
    console.log('保存认证信息到 localStorage:', authData);
    localStorage.setItem('auth', JSON.stringify(authData));
    console.log('已保存，验证读取:', localStorage.getItem('auth'));
  },

  // 从本地存储获取认证信息
  getAuth() {
    const auth = localStorage.getItem('auth');
    return auth ? JSON.parse(auth) : null;
  },

  // 清除本地存储的认证信息
  clearAuth() {
    localStorage.removeItem('auth');
  },

  // 检查是否已登录
  isLoggedIn() {
    const auth = this.getAuth();
    return auth && auth.loggedIn && auth.token;
  }
};

export default authService;
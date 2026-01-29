// 综合测试脚本：测试数据库连通性和API接口
const axios = require('axios');
const mysql = require('mysql2/promise');

// MySQL连接配置
const mysqlConfig = {
  host: '172.18.207.224',
  port: 3306,
  user: 'app',
  password: 'app123456',
  database: 'demo'
};

// 测试MySQL数据库连通性
async function testDatabaseConnection() {
  console.log('=== 测试MySQL数据库连通性 ===');
  
  try {
    // 创建数据库连接
    const connection = await mysql.createConnection(mysqlConfig);
    console.log('✅ MySQL数据库连接成功！');
    
    // 测试数据库查询
    const [rows] = await connection.execute('SELECT VERSION()');
    console.log(`MySQL版本: ${rows[0]['VERSION()']}`);
    
    // 测试查询用户表
    const [tables] = await connection.execute('SHOW TABLES LIKE ?', ['user%']);
    console.log('用户相关表:', tables.map(table => table[Object.keys(table)[0]]));
    
    // 测试查询用户数量
    if (tables.length > 0) {
      const [users] = await connection.execute('SELECT COUNT(*) as count FROM user');
      console.log(`用户数量: ${users[0].count}`);
    }
    
    // 关闭连接
    await connection.end();
    console.log('✅ MySQL数据库测试完成！');
    return true;
    
  } catch (error) {
    console.log('❌ MySQL数据库连接失败！');
    console.log('错误信息:', error.message);
    console.log('错误代码:', error.code);
    if (error.errno) {
      console.log('错误编号:', error.errno);
    }
    return false;
  }
}

// 测试后端API接口
async function testApiEndpoints() {
  console.log('\n=== 测试后端API接口 ===');
  
  try {
    // 测试健康检查接口
    console.log('测试健康检查接口...');
    const healthResponse = await axios.get('http://localhost:8000/health');
    console.log('✅ 健康检查接口成功:', healthResponse.status);
    console.log('健康检查响应:', healthResponse.data);
    
    // 测试登录接口
    console.log('\n测试登录接口...');
    const loginResponse = await axios.post('http://localhost:8000/api/v1/auth/login', {
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
    
    console.log('✅ 登录接口成功:', loginResponse.status);
    console.log('登录响应:', JSON.stringify(loginResponse.data, null, 2));
    
    // 获取token
    const token = loginResponse.data.data.access_token;
    console.log('获取到token:', token ? '✅ 成功' : '❌ 失败');
    
    // 测试用户管理API
    if (token) {
      console.log('\n测试用户管理API...');
      const usersResponse = await axios.get('http://localhost:8000/api/v1/users/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      console.log('✅ 用户管理API成功:', usersResponse.status);
      console.log('用户数量:', usersResponse.data.data.items.length);
      console.log('用户列表:', JSON.stringify(usersResponse.data.data.items, null, 2));
    }
    
    // 测试操作日志API
    if (token) {
      console.log('\n测试操作日志API...');
      const logsResponse = await axios.get('http://localhost:8000/api/v1/operation-logs', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      console.log('✅ 操作日志API成功:', logsResponse.status);
      console.log('操作日志数量:', logsResponse.data.data.items.length);
    }
    
    console.log('\n✅ 所有API测试完成！');
    return true;
    
  } catch (error) {
    console.log('❌ API测试失败！');
    console.log('错误信息:', error.message);
    if (error.response) {
      console.log('响应状态码:', error.response.status);
      console.log('响应数据:', JSON.stringify(error.response.data, null, 2));
    }
    return false;
  }
}

// 运行所有测试
async function runAllTests() {
  console.log('开始测试数据库连通性和API接口...');
  
  // 测试数据库连通性
  const dbConnected = await testDatabaseConnection();
  
  if (dbConnected) {
    // 测试API接口
    await testApiEndpoints();
  } else {
    console.log('\n⚠️  由于数据库连接失败，跳过API测试');
  }
  
  console.log('\n=== 测试完成 ===');
}

runAllTests();

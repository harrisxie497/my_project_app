# 前端容器化配置
# 使用官方 Node.js 18 镜像作为构建环境
FROM node:18-alpine as build

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目代码
COPY . .

# 构建生产版本
RUN npm run build

# 使用 nginx 作为运行环境
FROM nginx:alpine

# 复制构建好的文件到 nginx 静态文件目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义 nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
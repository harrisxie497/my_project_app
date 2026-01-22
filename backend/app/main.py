from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import router

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用实例，禁用自动重定向
app = FastAPI(
    title="日本清关Excel自动生成系统 API",
    description="日本清关Excel自动生成系统的后端API服务",
    version="1.0.0",
    redoc_url="/redoc",
    docs_url="/docs",
    # 禁用自动重定向，避免Authorization头丢失
    redirect_slashes=False
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "日本清关Excel自动生成系统 API 服务正常运行",
        "version": "1.0.0"
    }

# 根路径
@app.get("/")
def root():
    return {
        "message": "欢迎使用日本清关Excel自动生成系统 API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 导入API路由
app.include_router(router, prefix=settings.API_V1_STR)

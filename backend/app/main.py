from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging_config import setup_logging, get_logger
from app.api import router
import time

# 初始化日志系统
setup_logging()
logger = get_logger(__name__)

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 记录应用启动日志
logger.info(f"正在启动应用: {settings.APP_NAME} v1.0.0")
logger.info(f"数据库URL: {settings.DATABASE_URL}")
logger.info(f"API版本: {settings.API_V1_STR}")
logger.info(f"调试模式: {settings.DEBUG}")

# 创建FastAPI应用实例，与主API路由器保持一致，禁用自动重定向
app = FastAPI(
    title="日本清关Excel自动生成系统 API",
    description="日本清关Excel自动生成系统的后端API服务",
    version="1.0.0",
    redoc_url="/redoc",
    docs_url="/docs",
    # 与主API路由器保持一致，禁用自动重定向
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

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    记录所有HTTP请求的中间件
    
    记录请求方法、路径、客户端IP、处理时间等信息
    
    :param request: FastAPI请求对象
    :param call_next: 下一个中间件或路由处理器
    :return: 响应对象
    """
    start_time = time.time()
    
    # 记录请求信息
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path
    query_params = str(request.url.query) if request.url.query else ""
    
    logger.info(f"请求开始 - 方法: {method}, 路径: {path}, 参数: {query_params}, 客户端IP: {client_ip}")
    
    # 处理请求
    try:
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(f"请求完成 - 方法: {method}, 路径: {path}, 状态码: {response.status_code}, 处理时间: {process_time:.3f}s")
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    except Exception as e:
        # 记录错误
        process_time = time.time() - start_time
        logger.error(f"请求失败 - 方法: {method}, 路径: {path}, 错误: {str(e)}, 处理时间: {process_time:.3f}s")
        raise

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

# 简单测试路由
@app.get("/api/v1/test", tags=["test"])
async def test_route():
    return {"message": "Test route works!"}

# 导入API路由
app.include_router(router, prefix=settings.API_V1_STR)

# 记录应用启动完成
logger.info("应用启动完成，API服务已就绪")

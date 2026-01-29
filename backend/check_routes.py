from fastapi import FastAPI
from app.main import app

# 打印所有注册的路由
print("所有注册的路由:")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"- {route.path}")
    elif hasattr(route, 'url_path_for'):
        print(f"- {route.url_path_for}")
    else:
        print(f"- {route}")

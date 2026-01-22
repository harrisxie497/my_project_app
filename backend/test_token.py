from jose import jwt
from app.core.config import settings

# 测试JWT令牌解码
def test_token_decoding():
    # 示例令牌（从登录接口获取）
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2ODkxNDkzNn0.lOvIgroD6Sf2ugiI6BiR4Y4WbsztkUYGWoyjefkID6A"
    
    try:
        # 解码令牌
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"令牌解码成功: {payload}")
        return True
    except Exception as e:
        print(f"令牌解码失败: {e}")
        return False

if __name__ == "__main__":
    test_token_decoding()

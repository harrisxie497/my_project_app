import requests
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DeepSeekAIService:
    """DeepSeek AI服务"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        """
        初始化DeepSeek AI服务
        
        输入：
            - api_key: DeepSeek API密钥
            - base_url: API基础URL（默认：https://api.deepseek.com/v1）
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model = "deepseek-chat"
        self.max_retries = 3
        self.retry_delay = 2
        logger.info("DeepSeek AI服务初始化完成")
    
    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """
        调用DeepSeek聊天API（带重试机制）
        
        输入：
            - prompt: 用户提示词
            - system_prompt: 系统提示词（可选）
        
        输出：
            - AI响应文本
        """
        import time
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"调用DeepSeek API（第{attempt + 1}次），提示词长度：{len(prompt)}")
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                    logger.debug(f"ret系统提示词：{system_prompt}")
                messages.append({"role": "user", "content": prompt})
                logger.debug(f"ret用户提示词：{prompt}")
                
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 8192
                }
                
                logger.debug(f"发送的payload: {json.dumps(payload, ensure_ascii=False)}")
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=300
                )
                
                if response.status_code != 200:
                    logger.error(f"DeepSeek API返回错误状态码：{response.status_code}")
                    logger.error(f"响应内容：{response.text}")
                
                response.raise_for_status()
                result = response.json()
                
                content = result["choices"][0]["message"]["content"]
                logger.info(f"DeepSeek API调用成功，响应长度：{len(content)}")
                
                return content
                
            except requests.exceptions.Timeout as e:
                logger.warning(f"DeepSeek API调用超时（第{attempt + 1}次）：{str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"等待{self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"DeepSeek API调用超时，已重试{self.max_retries}次")
                    raise
            except requests.exceptions.RequestException as e:
                logger.warning(f"DeepSeek API调用失败（第{attempt + 1}次）：{str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"等待{self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"DeepSeek API调用失败，已重试{self.max_retries}次")
                    raise
            except Exception as e:
                logger.error(f"DeepSeek API调用异常（第{attempt + 1}次）：{str(e)}", exc_info=True)
                if attempt < self.max_retries - 1:
                    logger.info(f"等待{self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"DeepSeek API调用异常，已重试{self.max_retries}次")
                    raise

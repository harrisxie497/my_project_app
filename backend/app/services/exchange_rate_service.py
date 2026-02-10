import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict
import time

logger = logging.getLogger(__name__)

class ExchangeRateService:
    """汇率服务"""
    
    def __init__(self, api_key: str, base_url: str = "https://v6.exchangerate-api.com/v6"):
        """
        初始化汇率服务
        
        输入：
            - api_key: 汇率API密钥
            - base_url: API基础URL（默认：https://v6.exchangerate-api.com/v6）
        """
        self.api_key = api_key
        self.base_url = base_url
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        self.max_retries = 3
        self.retry_delay = 2
        logger.info("汇率服务初始化完成")
    
    def get_rate(self, from_currency: str, to_currency: str = "JPY") -> float:
        """
        获取汇率（带重试机制）
        
        输入：
            - from_currency: 源货币代码（如：USD）
            - to_currency: 目标货币代码（默认：JPY）
        
        输出：
            - 汇率（float）
        """
        try:
            cache_key = f"{from_currency}_{to_currency}"
            
            logger.info(f"获取汇率：{from_currency} -> {to_currency}")
            
            if from_currency == to_currency:
                logger.info(f"源货币和目标货币相同，汇率：1.0")
                return 1.0
            
            if cache_key in self.cache:
                cached_time, cached_rate = self.cache[cache_key]
                if datetime.now() - cached_time < self.cache_duration:
                    logger.info(f"使用缓存汇率：{cached_rate}")
                    return cached_rate
            
            # 使用重试机制获取汇率
            for attempt in range(self.max_retries):
                try:
                    logger.info(f"尝试获取汇率（第{attempt + 1}次）：{from_currency} -> {to_currency}")
                    
                    # 使用正确的API格式：{base_url}/{api_key}/latest/{base_currency}
                    url = f"{self.base_url}/{self.api_key}/latest/{from_currency}"
                    params = {
                        "symbols": to_currency
                    } if to_currency != "ALL" else {}

                    response = requests.get(url, params=params, timeout=30)
                    response.raise_for_status()

                    data = response.json()
                    rate = data["conversion_rates"][to_currency]
                    
                    self.cache[cache_key] = (datetime.now(), rate)
                    logger.info(f"获取汇率成功：{rate}，已缓存")
                    
                    return rate
                    
                except requests.exceptions.Timeout as e:
                    logger.warning(f"获取汇率超时（第{attempt + 1}次）：{from_currency} -> {to_currency}，错误：{str(e)}")
                    if attempt < self.max_retries - 1:
                        logger.info(f"等待{self.retry_delay}秒后重试...")
                        time.sleep(self.retry_delay)
                    else:
                        logger.error(f"获取汇率超时，已重试{self.max_retries}次：{from_currency} -> {to_currency}")
                        raise
                except requests.exceptions.RequestException as e:
                    logger.warning(f"获取汇率失败（第{attempt + 1}次）：{from_currency} -> {to_currency}，错误：{str(e)}")
                    if attempt < self.max_retries - 1:
                        logger.info(f"等待{self.retry_delay}秒后重试...")
                        time.sleep(self.retry_delay)
                    else:
                        logger.error(f"获取汇率失败，已重试{self.max_retries}次：{from_currency} -> {to_currency}")
                        raise
                except Exception as e:
                    logger.error(f"获取汇率异常（第{attempt + 1}次）：{from_currency} -> {to_currency}，错误：{str(e)}", exc_info=True)
                    if attempt < self.max_retries - 1:
                        logger.info(f"等待{self.retry_delay}秒后重试...")
                        time.sleep(self.retry_delay)
                    else:
                        logger.error(f"获取汇率异常，已重试{self.max_retries}次：{from_currency} -> {to_currency}")
                        raise
            
        except Exception as e:
            logger.error(f"获取汇率最终失败：{from_currency} -> {to_currency}，错误：{str(e)}", exc_info=True)
            raise

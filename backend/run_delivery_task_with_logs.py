"""
运行DELIVERY任务测试DEFAULT类型（带日志输出）
"""

import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_delivery.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

from app.core.database import SessionLocal
from app.services.delivery_processor import DeliveryProcessor

def run_delivery_task():
    """运行DELIVERY任务测试DEFAULT类型"""
    logger.info("=" * 100)
    logger.info("运行DELIVERY任务测试DEFAULT类型")
    logger.info("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 创建DeliveryProcessor实例
        task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_fc2fe5d3'
        header_params = {'mawb_no': '160-03270890', 'flight_no': '', 'arrival_date': ''}
        processor = DeliveryProcessor(db_session=db_session, task_dir=task_dir, file_type='DELIVERY', header_params=header_params)
        
        # 执行处理
        result = processor.process()
        
        logger.info(f"\n处理完成:")
        logger.info(f"  结果文件: {result.get('output_file') if result else None}")
        logger.info(f"  统计信息: {result.get('stats') if result else None}")
    
    except Exception as e:
        logger.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

if __name__ == "__main__":
    run_delivery_task()

import random
import logging
import time
from config import CRAWL_CONFIG, LOG_CONFIG

# 配置日志
logging.basicConfig(
    level=LOG_CONFIG['level'],
    format=LOG_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOG_CONFIG['file_path']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('douban_crawler')

def get_random_user_agent():
    """获取随机User-Agent"""
    return random.choice(CRAWL_CONFIG['user_agent_pool'])

def random_sleep():
    """随机延时"""
    delay = random.uniform(CRAWL_CONFIG['sleep_min'], CRAWL_CONFIG['sleep_max'])
    time.sleep(delay)
    logger.debug(f"随机延时: {delay:.2f}秒")

def retry(tries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == tries:
                        raise
                    logger.warning(f"尝试失败 {attempt}/{tries}: {e}，{delay}秒后重试")
                    time.sleep(delay)
        return wrapper
    return decorator
    
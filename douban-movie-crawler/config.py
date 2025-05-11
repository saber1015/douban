import os
import logging
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET')
}

# 爬取配置
CRAWL_CONFIG = {
    'base_url': os.getenv('BASE_URL'),
    'mode': os.getenv('CRAWL_MODE'),
    'sleep_min': float(os.getenv('SLEEP_MIN')),
    'sleep_max': float(os.getenv('SLEEP_MAX')),
    'retry_times': int(os.getenv('RETRY_TIMES')),
    'user_agent_pool': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    ]
}

# 日志配置
LOG_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crawler.log')
}

# Chrome驱动配置
DRIVER_CONFIG = {
    'executable_path': os.getenv('DRIVER_EXECUTABLE_PATH'),
    'headless': os.getenv('HEADLESS') == 'True'
}
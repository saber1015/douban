from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils import get_random_user_agent, retry
from config import DRIVER_CONFIG

@retry(tries=3, delay=2)
def create_driver():
    """创建浏览器驱动实例"""
    chrome_options = Options()
    
    # 设置随机User-Agent
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
        
    # 无头模式
    if DRIVER_CONFIG['headless']:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
    # 其他优化选项
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(DRIVER_CONFIG['executable_path'])
    return webdriver.Chrome(service=service, options=chrome_options)
    
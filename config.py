import os
from dotenv import load_dotenv

# 加载.env文件（与config.py同目录）
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    """应用配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aicove-secret-key-change-in-production'
    
    # Flask调试模式配置（默认关闭，避免ngrok重复创建问题）
    # 如需开启，在.env文件中设置 FLASK_DEBUG=True
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    # 暂时不使用数据库
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'mysql+pymysql://root:password@localhost/aicove?charset=utf8mb4'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = False
    
    # 分页配置
    POSTS_PER_PAGE = 10
    
    # 文件上传配置
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # AI 模型 API 配置（从.env文件读取）
    DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')  # 阿里云通义千问
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')  # DeepSeek
    KIMI_API_KEY = os.environ.get('KIMI_API_KEY', '')  # Kimi (Moonshot AI)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')  # Google Gemini
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')  # OpenAI
    VOLC_SEEDREAM_API_KEY = os.environ.get('VOLC_SEEDREAM_API_KEY', '')  # 火山引擎Seedream图像生成


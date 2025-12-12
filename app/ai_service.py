"""
多模型 AI 服务模块
支持：阿里云通义千问、DeepSeek、Kimi、Gemini、OpenAI
"""
from config import Config
import json
import requests

# ========== 阿里云 DashScope ==========
try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

if DASHSCOPE_AVAILABLE:
    dashscope.api_key = Config.DASHSCOPE_API_KEY

# ========== OpenAI ==========
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ========== Google Gemini ==========
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

if GEMINI_AVAILABLE:
    if Config.GEMINI_API_KEY:
        genai.configure(api_key=Config.GEMINI_API_KEY)


def chat_with_model(message, model='aliyun-qwen-turbo'):
    """
    使用指定模型进行对话
    
    Args:
        message: 用户消息
        model: 模型标识，格式：provider-model
            - aliyun-qwen-turbo / aliyun-qwen-plus / aliyun-qwen-max
            - deepseek-chat
            - kimi-moonshot-v1-8k
            - gemini-pro
            - openai-gpt-3.5-turbo / openai-gpt-4
    
    Returns:
        dict: {'success': bool, 'message': str, 'model': str}
    """
    if not message:
        return {
            'success': False,
            'message': '消息不能为空',
            'model': model
        }
    
    # 解析模型标识
    parts = model.split('-', 1)
    if len(parts) != 2:
        return {
            'success': False,
            'message': f'无效的模型标识: {model}',
            'model': model
        }
    
    provider = parts[0]
    model_name = parts[1]
    
    # 根据提供商调用相应的API
    if provider == 'aliyun':
        return _chat_aliyun(message, model_name)
    elif provider == 'deepseek':
        return _chat_deepseek(message, model_name)
    elif provider == 'kimi':
        return _chat_kimi(message, model_name)
    elif provider == 'gemini':
        return _chat_gemini(message, model_name)
    elif provider == 'openai':
        return _chat_openai(message, model_name)
    else:
        return {
            'success': False,
            'message': f'不支持的模型提供商: {provider}',
            'model': model
        }


def _chat_aliyun(message, model_name='qwen-turbo'):
    """阿里云通义千问"""
    if not DASHSCOPE_AVAILABLE:
        return {
            'success': False,
            'message': 'dashscope 模块未安装，请运行: pip install dashscope',
            'model': f'aliyun-{model_name}'
        }
    
    if not Config.DASHSCOPE_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置，请在.env文件中设置DASHSCOPE_API_KEY',
            'model': f'aliyun-{model_name}'
        }
    
    try:
        messages = [
            {'role': 'system', 'content': '你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。'},
            {'role': 'user', 'content': message}
        ]
        
        response = Generation.call(
            model=model_name,
            messages=messages,
            result_format='message'
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'message': response.output.choices[0].message.content,
                'model': f'aliyun-{model_name}'
            }
        else:
            return {
                'success': False,
                'message': f'API调用失败: {response.message}',
                'model': f'aliyun-{model_name}'
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'发生错误: {str(e)}',
            'model': f'aliyun-{model_name}'
        }


def _chat_deepseek(message, model_name='chat'):
    """DeepSeek"""
    if not Config.DEEPSEEK_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置，请在.env文件中设置DEEPSEEK_API_KEY',
            'model': f'deepseek-{model_name}'
        }
    
    try:
        url = 'https://api.deepseek.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Config.DEEPSEEK_API_KEY}'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': '你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。'},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        return {
            'success': True,
            'message': result['choices'][0]['message']['content'],
            'model': f'deepseek-{model_name}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'发生错误: {str(e)}',
            'model': f'deepseek-{model_name}'
        }


def _chat_kimi(message, model_name='moonshot-v1-8k'):
    """Kimi (Moonshot AI)"""
    if not Config.KIMI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置，请在.env文件中设置KIMI_API_KEY',
            'model': f'kimi-{model_name}'
        }
    
    try:
        url = 'https://api.moonshot.cn/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Config.KIMI_API_KEY}'
        }
        
        data = {
            'model': model_name,
            'messages': [
                {'role': 'system', 'content': '你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。'},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        return {
            'success': True,
            'message': result['choices'][0]['message']['content'],
            'model': f'kimi-{model_name}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'发生错误: {str(e)}',
            'model': f'kimi-{model_name}'
        }


def _chat_gemini(message, model_name='pro'):
    """Google Gemini"""
    if not GEMINI_AVAILABLE:
        return {
            'success': False,
            'message': 'google-generativeai 模块未安装，请运行: pip install google-generativeai',
            'model': f'gemini-{model_name}'
        }
    
    if not Config.GEMINI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置，请在.env文件中设置GEMINI_API_KEY',
            'model': f'gemini-{model_name}'
        }
    
    try:
        model = genai.GenerativeModel(f'gemini-{model_name}')
        
        prompt = f"""你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。

用户问题：{message}"""
        
        response = model.generate_content(prompt)
        
        return {
            'success': True,
            'message': response.text,
            'model': f'gemini-{model_name}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'发生错误: {str(e)}',
            'model': f'gemini-{model_name}'
        }


def _chat_openai(message, model_name='gpt-3.5-turbo'):
    """OpenAI"""
    if not OPENAI_AVAILABLE:
        return {
            'success': False,
            'message': 'openai 模块未安装，请运行: pip install openai',
            'model': f'openai-{model_name}'
        }
    
    if not Config.OPENAI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置，请在.env文件中设置OPENAI_API_KEY',
            'model': f'openai-{model_name}'
        }
    
    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'system', 'content': '你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。'},
                {'role': 'user', 'content': message}
            ],
            temperature=0.7
        )
        
        return {
            'success': True,
            'message': response.choices[0].message.content,
            'model': f'openai-{model_name}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'发生错误: {str(e)}',
            'model': f'openai-{model_name}'
        }


def ai_search(query, context_data=None):
    """
    使用AI进行智能搜索（默认使用阿里云）
    """
    if not DASHSCOPE_AVAILABLE or not Config.DASHSCOPE_API_KEY:
        return []
    
    try:
        search_prompt = f"""你是一个智能搜索助手。用户想要搜索："{query}"

请分析用户的搜索意图，并返回最相关的搜索关键词（3-5个），用逗号分隔。
只返回关键词，不要其他解释。"""
        
        messages = [
            {'role': 'user', 'content': search_prompt}
        ]
        
        response = Generation.call(
            model='qwen-turbo',
            messages=messages,
            result_format='message'
        )
        
        if response.status_code == 200:
            keywords = response.output.choices[0].message.content.strip()
            keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
            return keyword_list
        else:
            return []
    except Exception as e:
        print(f'AI搜索错误: {str(e)}')
        return []


def get_available_models():
    """
    获取可用的模型列表
    
    Returns:
        list: 模型列表，每个模型包含 value, name, provider, description
    """
    models = []
    
    # 阿里云通义千问
    if Config.DASHSCOPE_API_KEY:
        models.extend([
            {'value': 'aliyun-qwen-turbo', 'name': '通义千问 Turbo', 'provider': '阿里云', 'description': '快速响应，适合日常对话'},
            {'value': 'aliyun-qwen-plus', 'name': '通义千问 Plus', 'provider': '阿里云', 'description': '平衡性能与速度'},
            {'value': 'aliyun-qwen-max', 'name': '通义千问 Max', 'provider': '阿里云', 'description': '最强能力，适合复杂任务'},
        ])
    
    # DeepSeek
    if Config.DEEPSEEK_API_KEY:
        models.append({
            'value': 'deepseek-chat',
            'name': 'DeepSeek Chat',
            'provider': 'DeepSeek',
            'description': '高性能开源模型'
        })
    
    # Kimi
    if Config.KIMI_API_KEY:
        models.append({
            'value': 'kimi-moonshot-v1-8k',
            'name': 'Kimi Chat',
            'provider': 'Kimi',
            'description': '长文本理解能力强'
        })
    
    # Gemini
    if Config.GEMINI_API_KEY:
        models.append({
            'value': 'gemini-pro',
            'name': 'Gemini Pro',
            'provider': 'Google',
            'description': 'Google 多模态大模型'
        })
    
    # OpenAI
    if Config.OPENAI_API_KEY:
        models.extend([
            {'value': 'openai-gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo', 'provider': 'OpenAI', 'description': '快速且经济'},
            {'value': 'openai-gpt-4', 'name': 'GPT-4', 'provider': 'OpenAI', 'description': '最强能力，适合复杂任务'},
        ])
    
    # 如果没有配置任何模型，返回默认提示
    if not models:
        models.append({
            'value': 'none',
            'name': '未配置模型',
            'provider': '提示',
            'description': '请在.env文件中配置至少一个API密钥'
        })
    
    return models

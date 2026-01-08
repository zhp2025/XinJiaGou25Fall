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
            - gemini-1.5-flash (免费) / gemini-pro (付费)
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
    # 特殊处理 gemini-1.5-flash（包含多个连字符）
    if model.startswith('gemini-1.5-flash'):
        provider = 'gemini'
        model_name = '1.5-flash'
    elif model.startswith('gemini-'):
        parts = model.split('-', 1)
        provider = parts[0]
        model_name = parts[1]
    else:
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
        
        # 设置超时和重试
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
        # 处理模型名称：gemini-1.5-flash 或 gemini-pro
        # model_name 可能是 '1.5-flash' 或 'pro'
        if model_name == '1.5-flash':
            full_model_name = 'gemini-1.5-flash'
        elif model_name == 'pro':
            full_model_name = 'gemini-pro'
        else:
            full_model_name = f'gemini-{model_name}'
        
        model = genai.GenerativeModel(full_model_name)
        
        prompt = f"""你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。

用户问题：{message}"""
        
        response = model.generate_content(prompt)
        
        # 处理响应，确保有text属性
        if hasattr(response, 'text') and response.text:
            return {
                'success': True,
                'message': response.text,
                'model': full_model_name
            }
        else:
            # 尝试获取候选响应
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    if text:
                        return {
                            'success': True,
                            'message': text,
                            'model': full_model_name
                        }
            
            return {
                'success': False,
                'message': 'Gemini API返回了空响应',
                'model': full_model_name
            }
    except Exception as e:
        error_msg = str(e)
        # 提供更详细的错误信息
        if 'API key' in error_msg or 'authentication' in error_msg.lower():
            return {
                'success': False,
                'message': 'Gemini API密钥无效或未配置，请检查.env文件中的GEMINI_API_KEY',
                'model': f'gemini-{model_name}'
            }
        return {
            'success': False,
            'message': f'Gemini API错误: {error_msg}',
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
        
        # 确保模型名称正确（OpenAI的模型名称不需要前缀）
        if model_name.startswith('gpt-'):
            actual_model_name = model_name
        else:
            actual_model_name = model_name
        
        response = client.chat.completions.create(
            model=actual_model_name,
            messages=[
                {'role': 'system', 'content': '你是一个专业的AI助手，擅长回答关于人工智能、机器学习、深度学习等相关问题。请用中文回答。'},
                {'role': 'user', 'content': message}
            ],
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return {
                'success': True,
                'message': response.choices[0].message.content,
                'model': f'openai-{actual_model_name}'
            }
        else:
            return {
                'success': False,
                'message': 'OpenAI API返回了空响应',
                'model': f'openai-{actual_model_name}'
            }
    except Exception as e:
        error_msg = str(e)
        # 提供更详细的错误信息
        if 'API key' in error_msg or 'authentication' in error_msg.lower() or 'Invalid' in error_msg:
            return {
                'success': False,
                'message': 'OpenAI API密钥无效或未配置，请检查.env文件中的OPENAI_API_KEY',
                'model': f'openai-{model_name}'
            }
        elif 'rate limit' in error_msg.lower():
            return {
                'success': False,
                'message': 'OpenAI API请求频率过高，请稍后重试',
                'model': f'openai-{model_name}'
            }
        return {
            'success': False,
            'message': f'OpenAI API错误: {error_msg}',
            'model': f'openai-{model_name}'
        }


def ai_search(query, context_data=None):
    """
    智能搜索功能
    分析搜索意图，理解用户需求，返回最相关的搜索结果关键词
    """
    if not DASHSCOPE_AVAILABLE or not Config.DASHSCOPE_API_KEY:
        return []
    
    try:
        # 构建系统提示词，让AI理解搜索意图
        system_prompt = """你是一个专业的AI搜索助手。你的任务是分析用户的搜索意图，理解用户想要查找的内容，并返回最相关的搜索关键词。

用户可能搜索的内容类型包括：
- AI相关的文章、科普内容
- AI工具和模型
- AI术语和概念
- 技术教程和资源

请根据用户的搜索内容，分析其真实意图，返回3-5个最相关的搜索关键词（用逗号分隔）。
只返回关键词，不要其他解释。"""
        
        search_prompt = f"用户搜索：{query}\n\n请分析用户的搜索意图，返回最相关的搜索关键词："
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': search_prompt}
        ]
        
        # 进行搜索意图分析
        response = Generation.call(
            model='qwen-max',
            messages=messages,
            result_format='message',
            temperature=0.7
        )
        
        if response.status_code == 200:
            keywords = response.output.choices[0].message.content.strip()
            # 清理关键词，移除可能的标点符号和多余内容
            keyword_list = [k.strip().strip('.,;!?。，；！？') for k in keywords.split(',') if k.strip()]
            # 过滤空字符串和过短的关键词
            keyword_list = [k for k in keyword_list if len(k) > 1]
            return keyword_list[:5]  # 最多返回5个关键词
        else:
            print(f'AI搜索API错误: {response.status_code}')
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
        models.extend([
            {
                'value': 'gemini-1.5-flash',
                'name': 'Gemini 1.5 Flash',
                'provider': 'Google',
                'description': '免费版本，快速响应（推荐）'
            },
            {
                'value': 'gemini-pro',
                'name': 'Gemini Pro',
                'provider': 'Google',
                'description': '付费版本，更强能力'
            }
        ])
    
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


def chat_with_model_multi_turn(messages, model='aliyun-qwen-turbo'):
    """
    支持多轮对话的模型调用（原生支持多轮对话的模型）
    
    Args:
        messages: 消息列表，格式：[{'role': 'system', 'content': '...'}, {'role': 'user', 'content': '...'}, ...]
        model: 模型标识
    
    Returns:
        dict: {'success': bool, 'message': str, 'model': str}
    """
    if not messages or len(messages) == 0:
        return {
            'success': False,
            'message': '消息列表不能为空',
            'model': model
        }
    
    # 解析模型标识
    if model.startswith('gemini-1.5-flash'):
        provider = 'gemini'
        model_name = '1.5-flash'
    elif model.startswith('gemini-'):
        parts = model.split('-', 1)
        provider = parts[0]
        model_name = parts[1]
    else:
        parts = model.split('-', 1)
        if len(parts) != 2:
            return {
                'success': False,
                'message': f'无效的模型标识: {model}',
                'model': model
            }
        provider = parts[0]
        model_name = parts[1]
    
    # 根据提供商调用相应的多轮对话API
    if provider == 'aliyun':
        return _chat_aliyun_multi_turn(messages, model_name)
    elif provider == 'deepseek':
        return _chat_deepseek_multi_turn(messages, model_name)
    elif provider == 'kimi':
        return _chat_kimi_multi_turn(messages, model_name)
    elif provider == 'gemini':
        return _chat_gemini_multi_turn(messages, model_name)
    elif provider == 'openai':
        return _chat_openai_multi_turn(messages, model_name)
    else:
        # 不支持多轮对话的模型，回退到单轮模式
        last_user_message = next((msg['content'] for msg in reversed(messages) if msg['role'] == 'user'), '')
        if not last_user_message:
            return {
                'success': False,
                'message': '未找到用户消息',
                'model': model
            }
        return chat_with_model(last_user_message, model)


def _chat_aliyun_multi_turn(messages, model_name='qwen-turbo'):
    """阿里云通义千问多轮对话"""
    if not DASHSCOPE_AVAILABLE:
        return {
            'success': False,
            'message': 'dashscope 模块未安装',
            'model': f'aliyun-{model_name}'
        }
    
    if not Config.DASHSCOPE_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置',
            'model': f'aliyun-{model_name}'
        }
    
    try:
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


def _chat_deepseek_multi_turn(messages, model_name='chat'):
    """DeepSeek多轮对话"""
    if not Config.DEEPSEEK_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置',
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
            'messages': messages,
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


def _chat_kimi_multi_turn(messages, model_name='moonshot-v1-8k'):
    """Kimi多轮对话"""
    if not Config.KIMI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置',
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
            'messages': messages,
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


def _chat_gemini_multi_turn(messages, model_name='pro'):
    """Gemini多轮对话"""
    if not GEMINI_AVAILABLE:
        return {
            'success': False,
            'message': 'google-generativeai 模块未安装',
            'model': f'gemini-{model_name}'
        }
    
    if not Config.GEMINI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置',
            'model': f'gemini-{model_name}'
        }
    
    try:
        # 处理模型名称
        if model_name == '1.5-flash':
            full_model_name = 'gemini-1.5-flash'
        elif model_name == 'pro':
            full_model_name = 'gemini-pro'
        else:
            full_model_name = f'gemini-{model_name}'
        
        model = genai.GenerativeModel(full_model_name)
        
        # 提取system消息和最后一条用户消息
        system_content = None
        last_user_message = None
        
        for msg in messages:
            if msg['role'] == 'system':
                system_content = msg['content']
            elif msg['role'] == 'user':
                last_user_message = msg['content']
        
        # 构建提示词（包含system内容和用户消息）
        if system_content and last_user_message:
            prompt = f"{system_content}\n\n用户问题：{last_user_message}"
        elif last_user_message:
            prompt = last_user_message
        else:
            return {
                'success': False,
                'message': '未找到用户消息',
                'model': full_model_name
            }
        
        response = model.generate_content(prompt)
        
        # 处理响应
        if hasattr(response, 'text') and response.text:
            return {
                'success': True,
                'message': response.text,
                'model': full_model_name
            }
        else:
            # 尝试从candidates获取
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    if text:
                        return {
                            'success': True,
                            'message': text,
                            'model': full_model_name
                        }
        
        return {
            'success': False,
            'message': 'Gemini API返回了空响应',
            'model': full_model_name
        }
    except Exception as e:
        error_msg = str(e)
        if 'API key' in error_msg or 'authentication' in error_msg.lower():
            return {
                'success': False,
                'message': 'Gemini API密钥无效或未配置',
                'model': f'gemini-{model_name}'
            }
        return {
            'success': False,
            'message': f'Gemini API错误: {error_msg}',
            'model': f'gemini-{model_name}'
        }


def _chat_openai_multi_turn(messages, model_name='gpt-3.5-turbo'):
    """OpenAI多轮对话"""
    if not OPENAI_AVAILABLE:
        return {
            'success': False,
            'message': 'openai 模块未安装',
            'model': f'openai-{model_name}'
        }
    
    if not Config.OPENAI_API_KEY:
        return {
            'success': False,
            'message': 'API密钥未配置',
            'model': f'openai-{model_name}'
        }
    
    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # 确保模型名称正确
        if model_name.startswith('gpt-'):
            actual_model_name = model_name
        else:
            actual_model_name = model_name
        
        response = client.chat.completions.create(
            model=actual_model_name,
            messages=messages,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return {
                'success': True,
                'message': response.choices[0].message.content,
                'model': f'openai-{actual_model_name}'
            }
        else:
            return {
                'success': False,
                'message': 'OpenAI API返回了空响应',
                'model': f'openai-{actual_model_name}'
            }
    except Exception as e:
        error_msg = str(e)
        if 'API key' in error_msg or 'authentication' in error_msg.lower() or 'Invalid' in error_msg:
            return {
                'success': False,
                'message': 'OpenAI API密钥无效或未配置',
                'model': f'openai-{model_name}'
            }
        elif 'rate limit' in error_msg.lower():
            return {
                'success': False,
                'message': 'OpenAI API请求频率过高，请稍后重试',
                'model': f'openai-{model_name}'
            }
        return {
            'success': False,
            'message': f'OpenAI API错误: {error_msg}',
            'model': f'openai-{model_name}'
        }

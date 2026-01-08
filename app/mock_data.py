"""
模拟数据文件
在数据库建立之前使用模拟数据
"""
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'IA'),
    'charset': 'utf8mb4'
}

# 模拟用户数据（密码已加密）
MOCK_USERS = [
    {
        'id': 1,
        'username': 'admin',
        'nickname': '管理员',
        'email': 'admin@aicove.com',
        'password': generate_password_hash('admin123'),  # 使用哈希加密
        'role': 'super_admin',  # 第一个用户设为超级管理员
        'avatar': 'default.jpg',
        'security_question': '您母亲的名字是？',
        'security_answer': '妈妈',
        'interests': [],  # 用户感兴趣的领域
        'favorites': {},  # {type: {id: True/False}} 例如 {'article': {1: True}, 'forum': {2: False}}
        'likes': {},  # {type: {id: True/False}}
        'messages': [],  # 消息列表
        'first_login': False  # 是否首次登录
    },
    {
        'id': 2,
        'username': 'testuser',
        'nickname': '测试用户',
        'email': 'test@aicove.com',
        'password': generate_password_hash('test123'),  # 使用哈希加密
        'role': 'user',
        'avatar': 'default.jpg',
        'security_question': '您最喜欢的颜色是？',
        'security_answer': '蓝色',
        'interests': [],
        'favorites': {},
        'likes': {},
        'messages': [],
        'first_login': True
    }
]

# 收藏记录存储 {user_id: {type: {id: timestamp}}}
USER_FAVORITES = {}

# 点赞记录存储 {user_id: {type: {id: timestamp}}}
USER_LIKES = {}

# 消息存储 {user_id: [messages]}
USER_MESSAGES = {}

# 搜索日志（用于热门搜索词统计）
# 格式: {search_query: {'count': int, 'last_search': datetime}}
SEARCH_LOGS = {}

# 模拟文章数据
MOCK_ARTICLES = [
    {
        'id': 1,
        'title': '什么是大语言模型（LLM）？',
        'content': '大语言模型（Large Language Model, LLM）是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。它们通过在海量文本数据上训练，学习语言的统计规律和语义关系。',
        'category': '热门科普',
        'cover_image': None,
        'views': 150,
        'likes': 25,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=5),
        'is_featured': True
    },
    {
        'id': 2,
        'title': 'ChatGPT 的工作原理',
        'content': 'ChatGPT 基于 Transformer 架构，使用自注意力机制处理序列数据。它通过预训练和微调两个阶段，学习语言的生成模式，能够根据上下文生成连贯的回复。',
        'category': '热门科普',
        'cover_image': None,
        'views': 200,
        'likes': 35,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=3),
        'is_featured': True,
        'url': 'https://openai.com/research/gpt-3'
    },
    {
        'id': 3,
        'title': 'AI 在医疗领域的应用',
        'content': '人工智能在医疗领域有着广泛的应用，包括医学影像分析、疾病诊断、药物研发等。AI 技术能够帮助医生提高诊断准确率，缩短诊断时间。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 120,
        'likes': 20,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=1),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.CY/recent'
    },
    {
        'id': 4,
        'title': '深度学习在图像识别中的突破',
        'content': '深度学习技术，特别是卷积神经网络（CNN），在图像识别领域取得了革命性的突破。从 AlexNet 到 ResNet，再到 Vision Transformer，准确率不断提升。',
        'category': '热门科普',
        'cover_image': None,
        'views': 180,
        'likes': 30,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=7),
        'is_featured': True,
        'url': 'https://arxiv.org/abs/1512.03385'
    },
    {
        'id': 5,
        'title': 'AI 最新研究进展',
        'content': '近期 AI 研究领域出现了多项重要进展，包括多模态大模型、强化学习新算法等。这些进展为 AI 应用开辟了新的可能性。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 90,
        'likes': 15,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(hours=12),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.AI/recent'
    },
    {
        'id': 6,
        'title': 'Transformer架构详解',
        'content': 'Transformer架构是自然语言处理领域的革命性突破，通过自注意力机制实现了并行计算，大大提升了训练效率。本文将深入解析Transformer的工作原理。',
        'category': '热门科普',
        'cover_image': None,
        'views': 320,
        'likes': 58,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=2),
        'is_featured': True,
        'url': 'https://arxiv.org/abs/1706.03762'
    },
    {
        'id': 7,
        'title': 'GPT-4技术解析',
        'content': 'GPT-4是OpenAI发布的最新大语言模型，在多个基准测试中表现优异。本文详细介绍了GPT-4的技术特点、能力边界和应用场景。',
        'category': '热门科普',
        'cover_image': None,
        'views': 450,
        'likes': 72,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=4),
        'is_featured': True,
        'url': 'https://openai.com/research/gpt-4'
    },
    {
        'id': 8,
        'title': 'AI在自动驾驶中的应用',
        'content': '自动驾驶技术是AI在交通领域的重要应用，通过计算机视觉、传感器融合和决策算法，实现车辆的自主导航。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 280,
        'likes': 45,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=6),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.CV/recent'
    },
    {
        'id': 9,
        'title': '深度学习框架对比：PyTorch vs TensorFlow',
        'content': 'PyTorch和TensorFlow是目前最流行的两个深度学习框架。本文从易用性、性能、生态系统等多个维度进行对比分析。',
        'category': '热门科普',
        'cover_image': None,
        'views': 380,
        'likes': 65,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=8),
        'is_featured': True,
        'url': 'https://pytorch.org/tutorials/'
    },
    {
        'id': 10,
        'title': 'AI生成内容（AIGC）的发展趋势',
        'content': 'AIGC技术正在改变内容创作方式，从文本生成到图像创作，AI正在成为创意工作者的重要工具。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 220,
        'likes': 38,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=10),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.CL/recent'
    },
    {
        'id': 11,
        'title': '神经网络优化技巧',
        'content': '介绍深度学习中常用的优化技巧，包括学习率调整、批量归一化、残差连接等方法，帮助提升模型性能。',
        'category': '热门科普',
        'cover_image': None,
        'views': 290,
        'likes': 52,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=12),
        'is_featured': True,
        'url': 'https://arxiv.org/list/cs.LG/recent'
    },
    {
        'id': 12,
        'title': '大模型训练的成本与挑战',
        'content': '训练大语言模型需要巨大的计算资源和数据，本文分析了训练成本、技术挑战以及可能的解决方案。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 180,
        'likes': 32,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=14),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.CL/recent'
    },
    {
        'id': 13,
        'title': '计算机视觉中的目标检测',
        'content': '目标检测是计算机视觉的核心任务之一，从R-CNN到YOLO，算法不断演进，准确率和速度持续提升。',
        'category': '热门科普',
        'cover_image': None,
        'views': 340,
        'likes': 61,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=16),
        'is_featured': True,
        'url': 'https://arxiv.org/list/cs.CV/recent'
    },
    {
        'id': 14,
        'title': 'AI在金融科技中的应用',
        'content': 'AI技术在金融领域有广泛应用，包括风险评估、欺诈检测、智能投顾等，正在改变传统金融服务模式。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 250,
        'likes': 42,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=18),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.CY/recent'
    },
    {
        'id': 15,
        'title': '强化学习入门指南',
        'content': '强化学习是机器学习的重要分支，通过与环境交互学习最优策略。本文介绍强化学习的基本概念和常用算法。',
        'category': '热门科普',
        'cover_image': None,
        'views': 270,
        'likes': 48,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=20),
        'is_featured': True,
        'url': 'https://arxiv.org/list/cs.LG/recent'
    },
    {
        'id': 16,
        'title': '多模态AI的发展与应用',
        'content': '多模态AI能够同时处理文本、图像、音频等多种类型的数据，为AI应用开辟了新的可能性。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 210,
        'likes': 36,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=22),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.MM/recent'
    },
    {
        'id': 17,
        'title': '自然语言处理中的预训练模型',
        'content': '预训练模型如BERT、GPT等通过大规模无标注数据预训练，然后在特定任务上微调，取得了显著效果。',
        'category': '热门科普',
        'cover_image': None,
        'views': 360,
        'likes': 68,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=24),
        'is_featured': True,
        'url': 'https://arxiv.org/list/cs.CL/recent'
    },
    {
        'id': 18,
        'title': 'AI芯片的发展现状',
        'content': 'AI芯片是AI计算的基础设施，从GPU到TPU，再到专用AI芯片，硬件创新推动AI能力不断提升。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 190,
        'likes': 34,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=26),
        'is_featured': False,
        'url': 'https://arxiv.org/list/cs.AR/recent'
    },
    {
        'id': 19,
        'title': '生成式AI的伦理问题',
        'content': '生成式AI能够创作文本、图像等内容，但也带来了版权、真实性等伦理问题，需要建立相应的治理框架。',
        'category': '最新资讯',
        'cover_image': None,
        'views': 240,
        'likes': 41,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=28),
        'is_featured': False,
        'url': 'https://www.example.com/generative-ai-ethics'
    },
    {
        'id': 20,
        'title': 'AI模型压缩与部署',
        'content': '模型压缩技术能够减小模型体积、降低计算需求，使AI模型能够在边缘设备上高效运行。',
        'category': '热门科普',
        'cover_image': None,
        'views': 310,
        'likes': 55,
        'author_id': 1,
        'created_at': datetime.now() - timedelta(days=30),
        'is_featured': True,
        'url': 'https://www.example.com/model-compression'
    }
]

# 模拟工具数据
MOCK_TOOLS = [
    {
        'id': 1,
        'name': 'ChatGPT',
        'description': 'OpenAI 开发的大语言模型，支持对话、写作、编程等多种任务',
        'category': '大模型',
        'url': 'https://chat.openai.com',
        'icon': '🤖',
        'rating': 4.8,
        'rating_count': 1000
    },
    {
        'id': 2,
        'name': 'Midjourney',
        'description': '强大的 AI 图像生成工具，能够根据文本描述生成高质量图像',
        'category': '图像生成',
        'url': 'https://www.midjourney.com',
        'icon': '🎨',
        'rating': 4.7,
        'rating_count': 800
    },
    {
        'id': 3,
        'name': 'GitHub Copilot',
        'description': 'AI 编程助手，能够根据代码上下文自动生成代码',
        'category': '编程',
        'url': 'https://github.com/features/copilot',
        'icon': '💻',
        'rating': 4.6,
        'rating_count': 600
    },
    {
        'id': 4,
        'name': 'GPT-4',
        'description': 'OpenAI 最新的大语言模型，在多个任务上表现优异',
        'category': '大模型',
        'url': 'https://openai.com',
        'icon': '🧠',
        'rating': 4.9,
        'rating_count': 1200
    },
    {
        'id': 6,
        'name': 'Gemini',
        'description': 'Google 开发的多模态大语言模型，支持文本、图像、视频等多种输入',
        'category': '大模型',
        'url': 'https://deepmind.google/technologies/gemini/',
        'icon': '⭐',
        'rating': 4.8,
        'rating_count': 1100
    },
    {
        'id': 7,
        'name': '通义千问',
        'description': '阿里云开发的大语言模型，支持中文对话和多种任务',
        'category': '大模型',
        'url': 'https://tongyi.aliyun.com/',
        'icon': '🌟',
        'rating': 4.7,
        'rating_count': 900
    },
    {
        'id': 8,
        'name': 'Stable Diffusion',
        'description': '开源的图像生成模型，可以根据文本描述生成高质量图像',
        'category': '图像生成',
        'url': 'https://stability.ai/',
        'icon': '🎨',
        'rating': 4.6,
        'rating_count': 1200
    },
    {
        'id': 9,
        'name': 'DALL-E 2',
        'description': 'OpenAI开发的图像生成模型，能够根据文本描述生成创意图像',
        'category': '图像生成',
        'url': 'https://openai.com/dall-e-2',
        'icon': '🖼️',
        'rating': 4.8,
        'rating_count': 1500
    },
    {
        'id': 10,
        'name': 'Notion AI',
        'description': 'AI驱动的笔记和协作工具，支持智能写作和内容生成',
        'category': '写作',
        'url': 'https://www.notion.so/product/ai',
        'icon': '📝',
        'rating': 4.5,
        'rating_count': 800
    },
    {
        'id': 11,
        'name': 'Jasper',
        'description': 'AI内容创作工具，帮助营销人员快速生成高质量文案',
        'category': '写作',
        'url': 'https://www.jasper.ai/',
        'icon': '✍️',
        'rating': 4.4,
        'rating_count': 700
    },
    {
        'id': 12,
        'name': 'DeepL',
        'description': 'AI翻译工具，提供高质量的机器翻译服务，支持多种语言',
        'category': '翻译',
        'url': 'https://www.deepl.com/',
        'icon': '🌐',
        'rating': 4.7,
        'rating_count': 2000
    },
    {
        'id': 13,
        'name': 'Cursor',
        'description': 'AI代码编辑器，基于GPT技术提供智能代码补全和生成',
        'category': '编程',
        'url': 'https://cursor.sh/',
        'icon': '💻',
        'rating': 4.6,
        'rating_count': 1000
    },
    {
        'id': 14,
        'name': 'Codeium',
        'description': '免费的AI代码补全工具，支持多种编程语言和IDE',
        'category': '编程',
        'url': 'https://codeium.com/',
        'icon': '🔧',
        'rating': 4.5,
        'rating_count': 900
    },
    {
        'id': 15,
        'name': 'Runway ML',
        'description': 'AI视频编辑和生成工具，支持视频特效、背景移除等功能',
        'category': '视频',
        'url': 'https://runwayml.com/',
        'icon': '🎬',
        'rating': 4.6,
        'rating_count': 1100
    },
    {
        'id': 16,
        'name': 'Synthesia',
        'description': 'AI视频生成平台，可以创建AI虚拟人物视频',
        'category': '视频',
        'url': 'https://www.synthesia.io/',
        'icon': '🎥',
        'rating': 4.4,
        'rating_count': 600
    },
    {
        'id': 17,
        'name': 'Perplexity',
        'description': 'AI搜索引擎，提供基于AI的智能搜索和问答服务',
        'category': '搜索',
        'url': 'https://www.perplexity.ai/',
        'icon': '🔍',
        'rating': 4.7,
        'rating_count': 1300
    },
    {
        'id': 18,
        'name': 'Character.AI',
        'description': 'AI角色对话平台，可以与各种AI角色进行对话互动',
        'category': '对话',
        'url': 'https://character.ai/',
        'icon': '💬',
        'rating': 4.5,
        'rating_count': 1500
    },
    {
        'id': 19,
        'name': 'ElevenLabs',
        'description': 'AI语音合成工具，可以生成自然流畅的语音',
        'category': '语音',
        'url': 'https://elevenlabs.io/',
        'icon': '🎤',
        'rating': 4.6,
        'rating_count': 800
    },
    {
        'id': 20,
        'name': 'Whisper',
        'description': 'OpenAI开发的语音识别模型，支持多语言语音转文字',
        'category': '语音',
        'url': 'https://openai.com/research/whisper',
        'icon': '🎧',
        'rating': 4.8,
        'rating_count': 1400
    }
]

# 模拟案例数据
MOCK_CASES = [
    {
        'id': 1,
        'title': 'AI 辅助医学影像诊断',
        'description': '使用深度学习技术分析医学影像，帮助医生快速准确地识别病变',
        'industry': 'AI+医疗',
        'image': None,
        'external_link': '#',
        'tags': '深度学习,医学影像,诊断',
        'created_at': datetime.now() - timedelta(days=10)
    },
    {
        'id': 2,
        'title': '智能教育平台',
        'description': '基于 AI 的个性化学习系统，根据学生特点提供定制化教学内容',
        'industry': 'AI+教育',
        'image': None,
        'external_link': 'https://www.example.com/ai-education-platform',
        'tags': '个性化学习,教育,AI',
        'created_at': datetime.now() - timedelta(days=8)
    },
    {
        'id': 3,
        'title': 'AI 科研助手',
        'description': '利用 AI 技术加速科研文献检索和分析，提高研究效率',
        'industry': 'AI+科研',
        'image': None,
        'external_link': 'https://www.example.com/ai-research-assistant',
        'tags': '科研,文献检索,AI',
        'created_at': datetime.now() - timedelta(days=6)
    },
    {
        'id': 4,
        'title': '智能办公系统',
        'description': 'AI 驱动的办公自动化系统，提升工作效率',
        'industry': 'AI+办公',
        'image': None,
        'external_link': 'https://www.example.com/ai-office-system',
        'tags': '办公自动化,效率,AI',
        'created_at': datetime.now() - timedelta(days=4)
    },
    {
        'id': 5,
        'title': 'AI 艺术创作平台',
        'description': '使用生成式AI技术创作艺术作品，支持多种艺术风格',
        'industry': 'AI+艺术',
        'image': None,
        'external_link': 'https://www.example.com/ai-art-platform',
        'tags': '艺术创作,生成式AI,创意',
        'created_at': datetime.now() - timedelta(days=12)
    },
    {
        'id': 6,
        'title': '智能医疗诊断系统',
        'description': '基于深度学习的医疗影像分析系统，辅助医生进行疾病诊断',
        'industry': 'AI+医疗',
        'image': None,
        'external_link': '#',
        'tags': '医疗诊断,深度学习,影像分析',
        'created_at': datetime.now() - timedelta(days=9)
    },
    {
        'id': 7,
        'title': '个性化在线教育',
        'description': 'AI驱动的个性化学习平台，根据学生能力调整教学内容',
        'industry': 'AI+教育',
        'image': None,
        'external_link': '#',
        'tags': '在线教育,个性化学习,AI',
        'created_at': datetime.now() - timedelta(days=7)
    },
    {
        'id': 8,
        'title': '智能文档处理',
        'description': 'AI自动识别和处理各类文档，提高办公效率',
        'industry': 'AI+办公',
        'image': None,
        'external_link': '#',
        'tags': '文档处理,OCR,办公自动化',
        'created_at': datetime.now() - timedelta(days=5)
    }
]

# 模拟术语数据
MOCK_TERMS = [
    {
        'id': 1,
        'term': 'LLM',
        'definition': '大语言模型（Large Language Model），是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。',
        'category': 'LLM',
        'related_terms': '2,3',
        'examples': 'ChatGPT, GPT-4, Gemini',
        'image_path': 'images/concepts/concept_1_llm.jpg',
        'video_url': 'https://www.youtube.com/watch?v=zjkBMFhNj_g',
        'video_title': '什么是大语言模型？',
        'video_description': '深入浅出地解释大语言模型的工作原理和应用场景'
    },
    {
        'id': 2,
        'term': 'Transformer',
        'definition': 'Transformer 是一种基于自注意力机制的神经网络架构，广泛应用于自然语言处理任务。',
        'category': 'Transformer',
        'related_terms': '1',
        'examples': 'BERT, GPT, T5',
        'image_path': 'images/concepts/concept_2_transformer.png',
        'video_url': 'https://www.youtube.com/watch?v=U0s0f995w14',
        'video_title': 'Transformer架构详解',
        'video_description': '详细解释Transformer的编码器-解码器结构和自注意力机制'
    },
    {
        'id': 3,
        'term': '扩散模型',
        'definition': '扩散模型（Diffusion Model）是一种生成模型，通过逐步去噪过程生成高质量图像。',
        'category': '扩散模型',
        'related_terms': None,
        'examples': 'DALL-E 2, Stable Diffusion, Midjourney'
    },
    {
        'id': 4,
        'term': '神经网络',
        'definition': '神经网络是模拟人脑神经元连接的计算模型，由多个层和节点组成。',
        'category': '核心概念',
        'related_terms': '2',
        'examples': '多层感知机, CNN, RNN',
        'image_path': 'images/concepts/concept_4_neural_network.jpg',
        'video_url': 'https://www.youtube.com/watch?v=aircAruvnKk',
        'video_title': '神经网络基础',
        'video_description': '介绍神经网络的基本结构、工作原理和训练过程'
    },
    {
        'id': 5,
        'term': '深度学习',
        'definition': '深度学习是机器学习的一个分支，使用多层神经网络来学习数据的表示。',
        'category': '核心概念',
        'related_terms': '4',
        'examples': '深度神经网络, 卷积神经网络',
        'image_path': 'images/concepts/concept_5_deep_learning.png',
        'video_url': 'https://www.youtube.com/watch?v=CS4cs9xVecg',
        'video_title': '深度学习入门',
        'video_description': '吴恩达教授的深度学习课程，系统介绍深度学习的基本概念和应用'
    },
    {
        'id': 6,
        'term': '机器学习',
        'definition': '机器学习是人工智能的一个分支，通过算法让计算机从数据中学习规律，无需显式编程。',
        'category': '核心概念',
        'related_terms': '5',
        'examples': '监督学习, 无监督学习, 强化学习'
    },
    {
        'id': 7,
        'term': '卷积神经网络',
        'definition': '卷积神经网络（CNN）是一种专门用于处理图像数据的深度学习架构，通过卷积层提取特征。',
        'category': '核心概念',
        'related_terms': '4,5',
        'examples': 'LeNet, AlexNet, ResNet',
        'image_path': 'images/concepts/concept_7_cnn.jpg',
        'video_url': 'https://www.youtube.com/watch?v=ArPaAX_PhIs',
        'video_title': '卷积神经网络详解',
        'video_description': '深入讲解CNN的卷积层、池化层和全连接层的设计原理'
    },
    {
        'id': 8,
        'term': '强化学习',
        'definition': '强化学习是机器学习的一个分支，通过与环境交互来学习最优策略，常用于游戏AI和机器人控制。',
        'category': '核心概念',
        'related_terms': '6',
        'examples': 'Q-learning, Deep Q-Network, AlphaGo'
    },
    {
        'id': 9,
        'term': 'BERT',
        'definition': 'BERT（Bidirectional Encoder Representations from Transformers）是Google开发的预训练语言模型，使用双向Transformer编码器。',
        'category': 'LLM',
        'related_terms': '2',
        'examples': 'BERT-base, BERT-large'
    },
    {
        'id': 10,
        'term': 'GPT',
        'definition': 'GPT（Generative Pre-trained Transformer）是OpenAI开发的生成式预训练Transformer模型，采用自回归方式生成文本。',
        'category': 'LLM',
        'related_terms': '2,1',
        'examples': 'GPT-2, GPT-3, GPT-4'
    },
    {
        'id': 11,
        'term': '注意力机制',
        'definition': '注意力机制（Attention Mechanism）允许模型在处理序列时关注不同位置的信息，是Transformer架构的核心。',
        'category': 'Transformer',
        'related_terms': '2',
        'examples': '自注意力, 多头注意力',
        'image_path': 'images/concepts/concept_11_attention.png',
        'video_url': 'https://www.youtube.com/watch?v=U0s0f995w14',
        'video_title': '注意力机制详解',
        'video_description': '详细解释注意力机制的数学原理和实际应用'
    },
    {
        'id': 12,
        'term': '自注意力',
        'definition': '自注意力（Self-Attention）是注意力机制的一种，允许序列中的每个位置关注序列中的所有位置。',
        'category': 'Transformer',
        'related_terms': '11,2',
        'examples': 'Scaled Dot-Product Attention'
    },
    {
        'id': 13,
        'term': 'RNN',
        'definition': '循环神经网络（Recurrent Neural Network）是一种处理序列数据的神经网络，具有记忆能力。',
        'category': '核心概念',
        'related_terms': '4',
        'examples': 'LSTM, GRU'
    },
    {
        'id': 14,
        'term': 'LSTM',
        'definition': '长短期记忆网络（Long Short-Term Memory）是一种特殊的RNN，能够学习长期依赖关系。',
        'category': '核心概念',
        'related_terms': '13',
        'examples': '双向LSTM, 堆叠LSTM'
    },
    {
        'id': 15,
        'term': 'GAN',
        'definition': '生成对抗网络（Generative Adversarial Network）由生成器和判别器组成，通过对抗训练生成数据。',
        'category': '核心概念',
        'related_terms': '5',
        'examples': 'DCGAN, StyleGAN, CycleGAN',
        'image_path': 'images/concepts/concept_15_gan.jpg',
        'video_url': 'https://www.youtube.com/watch?v=Sw9r8CL98N8',
        'video_title': '生成对抗网络（GAN）原理',
        'video_description': '介绍GAN的工作原理，包括生成器和判别器的对抗训练过程'
    },
    {
        'id': 16,
        'term': 'ResNet',
        'definition': '残差网络（Residual Network）通过残差连接解决深层网络训练难题，是深度学习的重要突破。',
        'category': '核心概念',
        'related_terms': '7,5',
        'examples': 'ResNet-50, ResNet-101',
        'image_path': 'images/concepts/concept_16_resnet.png',
        'video_url': 'https://www.youtube.com/watch?v=GWt6Fu05voI',
        'video_title': 'ResNet残差网络详解',
        'video_description': '何凯明团队讲解ResNet的创新思想和实现细节'
    },
    {
        'id': 17,
        'term': '迁移学习',
        'definition': '迁移学习是将在一个任务上训练的模型应用到相关任务上的技术，可以显著减少训练数据需求。',
        'category': '核心概念',
        'related_terms': '5,6',
        'examples': '预训练模型, 微调'
    },
    {
        'id': 18,
        'term': '预训练',
        'definition': '预训练是在大规模数据上训练模型，学习通用特征表示，然后可以在特定任务上微调。',
        'category': '核心概念',
        'related_terms': '17,1',
        'examples': 'BERT预训练, GPT预训练'
    },
    {
        'id': 19,
        'term': '微调',
        'definition': '微调（Fine-tuning）是在预训练模型基础上，使用特定任务数据继续训练的过程。',
        'category': '核心概念',
        'related_terms': '17,18',
        'examples': 'BERT微调, GPT微调'
    },
    {
        'id': 20,
        'term': '监督学习',
        'definition': '监督学习使用标注数据训练模型，学习从输入到输出的映射关系。',
        'category': '核心概念',
        'related_terms': '6',
        'examples': '分类, 回归'
    },
    {
        'id': 21,
        'term': '无监督学习',
        'definition': '无监督学习从未标注数据中学习数据的内在结构和模式。',
        'category': '核心概念',
        'related_terms': '6',
        'examples': '聚类, 降维'
    },
    {
        'id': 22,
        'term': '梯度下降',
        'definition': '梯度下降是优化神经网络参数的主要方法，通过沿着损失函数梯度的反方向更新参数。',
        'category': '核心概念',
        'related_terms': '5',
        'examples': '随机梯度下降, 批量梯度下降'
    },
    {
        'id': 23,
        'term': '反向传播',
        'definition': '反向传播算法用于计算神经网络中每个参数的梯度，是训练深度网络的关键技术。',
        'category': '核心概念',
        'related_terms': '22,4',
        'examples': '链式法则, 梯度计算'
    },
    {
        'id': 24,
        'term': '过拟合',
        'definition': '过拟合是模型在训练数据上表现很好，但在测试数据上表现较差的现象。',
        'category': '核心概念',
        'related_terms': '6',
        'examples': '正则化,  dropout'
    },
    {
        'id': 25,
        'term': '正则化',
        'definition': '正则化是防止过拟合的技术，通过添加惩罚项来约束模型复杂度。',
        'category': '核心概念',
        'related_terms': '24',
        'examples': 'L1正则化, L2正则化'
    },
    {
        'id': 26,
        'term': 'Dropout',
        'definition': 'Dropout是一种正则化技术，在训练时随机丢弃部分神经元，防止过拟合。',
        'category': '核心概念',
        'related_terms': '24,25',
        'examples': '随机失活'
    },
    {
        'id': 27,
        'term': '激活函数',
        'definition': '激活函数为神经网络引入非线性，使网络能够学习复杂模式。',
        'category': '核心概念',
        'related_terms': '4',
        'examples': 'ReLU, Sigmoid, Tanh'
    },
    {
        'id': 28,
        'term': 'ReLU',
        'definition': 'ReLU（Rectified Linear Unit）是最常用的激活函数，计算简单且能缓解梯度消失问题。',
        'category': '核心概念',
        'related_terms': '27',
        'examples': 'Leaky ReLU, ELU'
    },
    {
        'id': 29,
        'term': '损失函数',
        'definition': '损失函数衡量模型预测与真实值之间的差异，是训练优化的目标。',
        'category': '核心概念',
        'related_terms': '22',
        'examples': '交叉熵, 均方误差'
    },
    {
        'id': 30,
        'term': '交叉熵',
        'definition': '交叉熵是分类任务常用的损失函数，衡量预测概率分布与真实分布的差异。',
        'category': '核心概念',
        'related_terms': '29',
        'examples': '二元交叉熵, 多类交叉熵'
    }
]

# 模拟资源数据
MOCK_RESOURCES = [
    {
        'id': 1,
        'title': '深度学习',
        'author': 'Ian Goodfellow',
        'type': '书籍',
        'description': '深度学习领域的经典教材，全面介绍深度学习的基础理论和实践方法。',
        'cover_image': None,
        'url': 'https://www.deeplearningbook.org/',
        'created_at': datetime.now() - timedelta(days=20)
    },
    {
        'id': 2,
        'title': 'Attention Is All You Need',
        'author': 'Vaswani et al.',
        'type': '论文',
        'description': 'Transformer 架构的原始论文，提出了自注意力机制。',
        'cover_image': None,
        'url': 'https://arxiv.org/abs/1706.03762',
        'created_at': datetime.now() - timedelta(days=15)
    },
    {
        'id': 3,
        'title': '机器学习课程',
        'author': 'Andrew Ng',
        'type': '课程',
        'description': 'Coursera 上的经典机器学习课程，适合初学者。',
        'cover_image': None,
        'url': 'https://www.coursera.org/learn/machine-learning',
        'created_at': datetime.now() - timedelta(days=10)
    },
    # 吴恩达课程推荐
    {
        'id': 4,
        'title': 'Machine Learning Full Course - 10 Hours | Machine Learning Course For Beginners',
        'author': 'Andrew Ng (吴恩达)',
        'type': '课程',
        'description': '斯坦福大学机器学习课程的完整版，由吴恩达教授主讲。涵盖监督学习、无监督学习、推荐系统等核心内容，适合初学者系统学习机器学习基础知识。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=GwIo3gDZCVQ',
        'created_at': datetime.now() - timedelta(days=30)
    },
    {
        'id': 5,
        'title': 'Deep Learning Specialization - Neural Networks and Deep Learning',
        'author': 'Andrew Ng (吴恩达)',
        'type': '课程',
        'description': '深度学习专项课程的第一门课程，深入讲解神经网络的基础知识，包括前向传播、反向传播、梯度下降等核心概念，是深入学习深度学习的必备基础。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=CS4cs9xVecg',
        'created_at': datetime.now() - timedelta(days=28)
    },
    {
        'id': 6,
        'title': 'Improving Deep Neural Networks: Hyperparameter tuning, Regularization and Optimization',
        'author': 'Andrew Ng (吴恩达)',
        'type': '课程',
        'description': '深度学习专项课程的第二门课程，专注于提升神经网络性能的技术，包括超参数调优、正则化方法、优化算法等实用技巧，帮助构建更高效的深度学习模型。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=1waHlpKiNyY',
        'created_at': datetime.now() - timedelta(days=26)
    },
    {
        'id': 7,
        'title': 'Structuring Machine Learning Projects',
        'author': 'Andrew Ng (吴恩达)',
        'type': '课程',
        'description': '机器学习项目实战课程，教授如何系统性地组织和执行机器学习项目，包括如何诊断模型问题、选择合适的评估指标、进行误差分析等，非常适合实际项目应用。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=dFX8k1kXhOw',
        'created_at': datetime.now() - timedelta(days=24)
    },
    {
        'id': 8,
        'title': 'Convolutional Neural Networks (CNN)',
        'author': 'Andrew Ng (吴恩达)',
        'type': '课程',
        'description': '卷积神经网络专项课程，详细介绍CNN的架构设计、卷积层、池化层、经典网络结构（LeNet、AlexNet、VGG、ResNet）等内容，是计算机视觉领域的核心课程。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=ArPaAX_PhIs',
        'created_at': datetime.now() - timedelta(days=22)
    },
    # 何凯明课程推荐
    {
        'id': 9,
        'title': 'Deep Residual Learning for Image Recognition (ResNet)',
        'author': 'Kaiming He (何凯明)',
        'type': '课程',
        'description': '何凯明团队在ResNet论文的讲解，介绍了残差网络的创新思想，通过跳跃连接解决了深层网络训练难题，是深度学习历史上的重要突破，对理解现代深度网络架构至关重要。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=GWt6Fu05voI',
        'created_at': datetime.now() - timedelta(days=20)
    },
    {
        'id': 10,
        'title': 'Mask R-CNN for Object Detection and Segmentation',
        'author': 'Kaiming He (何凯明)',
        'type': '课程',
        'description': 'Mask R-CNN方法的详细讲解，该方法结合了目标检测和实例分割，在COCO数据集上取得了优异的性能。何凯明团队详细介绍了该方法的架构设计和技术细节，是计算机视觉领域的经典工作。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=g7z4mkfRj44',
        'created_at': datetime.now() - timedelta(days=18)
    },
    {
        'id': 11,
        'title': 'Focal Loss for Dense Object Detection (RetinaNet)',
        'author': 'Kaiming He (何凯明)',
        'type': '课程',
        'description': 'RetinaNet和Focal Loss的讲解，解决了目标检测中类别不平衡的问题。该方法通过重新设计损失函数，使模型能够更好地处理难易样本，在单阶段检测器中取得了突破性成果。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=6jUqhp3jXyM',
        'created_at': datetime.now() - timedelta(days=16)
    },
    {
        'id': 12,
        'title': 'Batch Normalization: Accelerating Deep Network Training',
        'author': 'Kaiming He (何凯明)',
        'type': '课程',
        'description': '批量归一化技术的深入讲解，该技术通过规范化层输入，加速了深度网络的训练过程，提高了训练稳定性。何凯明团队详细解释了BN的原理、实现和应用场景，对理解深度学习训练技巧很有帮助。',
        'cover_image': None,
        'url': 'https://www.youtube.com/watch?v=DtEq44FTPM4',
        'created_at': datetime.now() - timedelta(days=14)
    },
    # 额外资源数据以支持分页
    {
        'id': 13,
        'title': 'Pattern Recognition and Machine Learning',
        'author': 'Christopher Bishop',
        'type': '书籍',
        'description': '模式识别与机器学习的经典教材，全面介绍统计学习方法、贝叶斯推理和机器学习算法。',
        'cover_image': None,
        'url': 'https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf',
        'created_at': datetime.now() - timedelta(days=13)
    },
    {
        'id': 14,
        'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
        'author': 'Devlin et al.',
        'type': '论文',
        'description': 'BERT模型的原始论文，介绍了双向Transformer预训练方法，在多个NLP任务上取得了突破性成果。',
        'cover_image': None,
        'url': 'https://arxiv.org/abs/1810.04805',
        'created_at': datetime.now() - timedelta(days=12)
    },
    {
        'id': 15,
        'title': 'Nature Machine Intelligence',
        'author': 'Nature Publishing Group',
        'type': '期刊',
        'description': 'Nature机器智能期刊，发表高质量的AI和机器学习研究论文，涵盖理论研究和实际应用。',
        'cover_image': None,
        'url': 'https://www.nature.com/natmachintell/',
        'created_at': datetime.now() - timedelta(days=11)
    },
    {
        'id': 16,
        'title': 'Stanford CS224N: Natural Language Processing with Deep Learning',
        'author': 'Christopher Manning',
        'type': '课程',
        'description': '斯坦福大学CS224N课程，深入讲解自然语言处理中的深度学习技术，包括词向量、RNN、Transformer等。',
        'cover_image': None,
        'url': 'https://web.stanford.edu/class/cs224n/',
        'created_at': datetime.now() - timedelta(days=9)
    },
    {
        'id': 17,
        'title': 'GPT-3: Language Models are Few-Shot Learners',
        'author': 'Brown et al.',
        'type': '论文',
        'description': 'GPT-3论文，展示了大规模语言模型的few-shot学习能力，为现代LLM的发展奠定了基础。',
        'cover_image': None,
        'url': 'https://arxiv.org/abs/2005.14165',
        'created_at': datetime.now() - timedelta(days=8)
    },
    {
        'id': 18,
        'title': 'Journal of Machine Learning Research',
        'author': 'JMLR',
        'type': '期刊',
        'description': '机器学习研究期刊，是机器学习领域的顶级期刊，发表高质量的理论和应用研究。',
        'cover_image': None,
        'url': 'https://www.jmlr.org/',
        'created_at': datetime.now() - timedelta(days=7)
    }
]

# 模拟伦理专题数据
MOCK_ETHICS_TOPICS = [
    {
        'id': 1,
        'title': 'AI 安全',
        'slug': 'ai-safety',
        'description': '探讨 AI 系统的安全性问题，包括对抗攻击、模型鲁棒性等',
        'background': '随着 AI 技术的快速发展，AI 系统的安全性问题日益凸显。如何确保 AI 系统在各种情况下都能安全可靠地运行，是一个重要的研究课题。',
        'key_issues': '对抗样本攻击、模型鲁棒性、系统可靠性、安全部署',
        'expert_views': '专家认为，AI 安全需要从多个维度进行保障，包括模型设计、训练过程、部署环境等。',
        'likes': 45,
        'views': 320,
        'created_at': datetime.now() - timedelta(days=30)
    },
    {
        'id': 2,
        'title': 'AI 偏见与公平',
        'slug': 'ai-bias-fairness',
        'description': '讨论 AI 系统中的偏见问题，以及如何实现算法公平',
        'background': 'AI 系统可能从训练数据中学习到偏见，导致对某些群体的不公平对待。',
        'key_issues': '数据偏见、算法偏见、公平性评估、去偏见方法',
        'expert_views': '实现算法公平需要从数据收集、模型设计、评估指标等多个环节进行考虑。',
        'likes': 38,
        'views': 350,
        'created_at': datetime.now() - timedelta(days=25)
    },
    {
        'id': 3,
        'title': 'AI 与就业',
        'slug': 'ai-employment',
        'description': '探讨 AI 技术对就业市场的影响',
        'background': 'AI 技术的快速发展正在改变就业市场，既有创造新岗位的机会，也有替代传统岗位的风险。',
        'key_issues': '岗位替代、新岗位创造、技能转型、职业规划',
        'expert_views': '专家建议，应该积极适应 AI 时代，学习新技能，拥抱变化。',
        'likes': 52,
        'views': 480,
        'created_at': datetime.now() - timedelta(days=20)
    },
    {
        'id': 4,
        'title': '数据隐私',
        'slug': 'data-privacy',
        'description': '讨论 AI 应用中的数据隐私保护问题',
        'background': 'AI 系统需要大量数据进行训练，如何保护用户隐私是一个重要挑战。',
        'key_issues': '数据收集、数据使用、隐私保护、合规性',
        'expert_views': '需要在技术创新和隐私保护之间找到平衡。',
        'likes': 41,
        'views': 280,
        'created_at': datetime.now() - timedelta(days=15)
    },
    {
        'id': 5,
        'title': 'AI 与人类智能',
        'slug': 'ai-human-intelligence',
        'description': '探讨 AI 与人类智能的关系，以及 AI 是否能够真正理解',
        'background': '随着 AI 能力的提升，关于 AI 是否具有真正理解能力、是否能够超越人类智能的讨论日益激烈。',
        'key_issues': '理解能力、意识问题、智能本质、人机关系',
        'expert_views': '专家认为，当前 AI 虽然在某些任务上超越人类，但缺乏真正的理解和意识。',
        'likes': 52,
        'views': 410,
        'created_at': datetime.now() - timedelta(days=10)
    },
    {
        'id': 6,
        'title': 'AI 治理与监管',
        'slug': 'ai-governance',
        'description': '讨论 AI 技术的治理框架和监管政策',
        'background': '随着 AI 技术的广泛应用，如何建立有效的治理和监管机制成为重要议题。',
        'key_issues': '监管政策、治理框架、国际协调、标准制定',
        'expert_views': '需要建立多层次、多主体的 AI 治理体系，平衡创新与风险。',
        'likes': 38,
        'views': 290,
        'created_at': datetime.now() - timedelta(days=8)
    }
]

# 学习路径数据
MOCK_LEARNING_PATHS = {
    'beginner': {
        'title': '"小白"学习路径',
        'description': '适合AI零基础的学习者，从最基础的概念开始，循序渐进',
        'steps': [
            {
                'id': 1,
                'title': 'AI 基础概念介绍',
                'description': '了解什么是人工智能、机器学习、深度学习等基础概念',
                'type': '文章',
                'resources': [
                    {'title': '什么是人工智能？', 'url': 'https://zh.wikipedia.org/wiki/人工智能', 'type': '文章'},
                    {'title': '机器学习入门指南', 'url': 'https://www.example.com/ml-guide', 'type': '教程'},
                    {'title': 'AI基础视频课程', 'url': 'https://www.example.com/ai-video', 'type': '视频'}
                ],
                'duration': '2小时',
                'difficulty': '入门'
            },
            {
                'id': 2,
                'title': '常见 AI 应用场景',
                'description': '了解AI在日常生活和工作中的实际应用',
                'type': '案例',
                'resources': [
                    {'title': 'AI应用案例集', 'url': '#', 'type': '案例'},
                    {'title': 'ChatGPT使用指南', 'url': 'https://www.example.com/chatgpt-guide', 'type': '教程'},
                    {'title': 'AI工具推荐', 'url': '#', 'type': '工具'}
                ],
                'duration': '1.5小时',
                'difficulty': '入门'
            },
            {
                'id': 3,
                'title': '视频教程：AI 入门指南',
                'description': '通过视频学习AI基础知识，更直观易懂',
                'type': '视频',
                'resources': [
                    {'title': 'AI入门视频课程', 'url': 'https://www.example.com/ai-course', 'type': '视频'},
                    {'title': '机器学习实战视频', 'url': 'https://www.example.com/ml-practice', 'type': '视频'},
                    {'title': '深度学习入门', 'url': 'https://www.example.com/dl-intro', 'type': '视频'}
                ],
                'duration': '3小时',
                'difficulty': '入门'
            },
            {
                'id': 4,
                'title': '实践项目：使用 AI 工具',
                'description': '通过实际操作，体验AI工具的强大功能',
                'type': '实践',
                'resources': [
                    {'title': 'AI工具实践指南', 'url': '#', 'type': '教程'},
                    {'title': 'ChatGPT实战项目', 'url': 'https://www.example.com/chatgpt-project', 'type': '项目'},
                    {'title': '图像生成工具使用', 'url': '#', 'type': '教程'}
                ],
                'duration': '2小时',
                'difficulty': '入门'
            }
        ]
    },
    'professional': {
        'title': '"职场人"应用路径',
        'description': '帮助职场人士快速掌握AI工具，提升工作效率',
        'steps': [
            {
                'id': 5,
                'title': 'AI 在工作场景中的应用',
                'description': '了解AI如何改变工作方式，提升工作效率',
                'type': '案例',
                'resources': [
                    {'title': 'AI办公应用案例', 'url': '#', 'type': '案例'},
                    {'title': '智能文档处理', 'url': 'https://www.example.com/doc-ai', 'type': '教程'},
                    {'title': 'AI辅助决策', 'url': 'https://www.example.com/ai-decision', 'type': '文章'}
                ],
                'duration': '2小时',
                'difficulty': '初级'
            },
            {
                'id': 6,
                'title': 'AI 工具使用技巧',
                'description': '掌握常用AI工具的高级使用技巧',
                'type': '教程',
                'resources': [
                    {'title': 'ChatGPT高级技巧', 'url': 'https://www.example.com/chatgpt-advanced', 'type': '教程'},
                    {'title': 'AI写作工具使用', 'url': 'https://www.example.com/ai-writing', 'type': '教程'},
                    {'title': 'AI数据分析工具', 'url': 'https://www.example.com/ai-analytics', 'type': '教程'}
                ],
                'duration': '2.5小时',
                'difficulty': '初级'
            },
            {
                'id': 7,
                'title': '案例学习：行业最佳实践',
                'description': '学习各行业AI应用的最佳实践案例',
                'type': '案例',
                'resources': [
                    {'title': '金融行业AI应用', 'url': 'https://www.example.com/finance-ai', 'type': '案例'},
                    {'title': '医疗行业AI应用', 'url': 'https://www.example.com/medical-ai', 'type': '案例'},
                    {'title': '教育行业AI应用', 'url': 'https://www.example.com/education-ai', 'type': '案例'}
                ],
                'duration': '3小时',
                'difficulty': '中级'
            },
            {
                'id': 8,
                'title': '提升工作效率的 AI 方法',
                'description': '学习如何利用AI工具大幅提升工作效率',
                'type': '实践',
                'resources': [
                    {'title': 'AI工作流程优化', 'url': 'https://www.example.com/workflow-ai', 'type': '教程'},
                    {'title': '自动化办公方案', 'url': 'https://www.example.com/automation', 'type': '教程'},
                    {'title': 'AI辅助项目管理', 'url': 'https://www.example.com/project-ai', 'type': '教程'}
                ],
                'duration': '2.5小时',
                'difficulty': '中级'
            }
        ]
    },
    'student': {
        'title': '"学生"进阶路径',
        'description': '适合有一定基础的学生，深入学习AI理论和实践',
        'steps': [
            {
                'id': 9,
                'title': '数学基础：线性代数、概率论',
                'description': '掌握AI学习所需的数学基础知识',
                'type': '课程',
                'resources': [
                    {'title': '线性代数课程', 'url': 'https://www.example.com/linear-algebra', 'type': '课程'},
                    {'title': '概率论与数理统计', 'url': 'https://www.example.com/probability', 'type': '课程'},
                    {'title': '微积分基础', 'url': 'https://www.example.com/calculus', 'type': '课程'}
                ],
                'duration': '20小时',
                'difficulty': '中级'
            },
            {
                'id': 10,
                'title': '机器学习算法原理',
                'description': '深入学习各种机器学习算法的原理和实现',
                'type': '课程',
                'resources': [
                    {'title': '机器学习算法详解', 'url': 'https://www.example.com/ml-algorithms', 'type': '课程'},
                    {'title': '监督学习算法', 'url': 'https://www.example.com/supervised-learning', 'type': '课程'},
                    {'title': '无监督学习算法', 'url': 'https://www.example.com/unsupervised-learning', 'type': '课程'}
                ],
                'duration': '30小时',
                'difficulty': '中级'
            },
            {
                'id': 11,
                'title': '深度学习框架使用',
                'description': '学习PyTorch、TensorFlow等深度学习框架',
                'type': '实践',
                'resources': [
                    {'title': 'PyTorch入门教程', 'url': 'https://www.example.com/pytorch', 'type': '教程'},
                    {'title': 'TensorFlow实战', 'url': 'https://www.example.com/tensorflow', 'type': '教程'},
                    {'title': '深度学习项目实战', 'url': 'https://www.example.com/dl-project', 'type': '项目'}
                ],
                'duration': '25小时',
                'difficulty': '高级'
            },
            {
                'id': 12,
                'title': '算法推导与实践',
                'description': '深入理解算法背后的数学原理，并通过实践加深理解',
                'type': '实践',
                'resources': [
                    {'title': '反向传播算法推导', 'url': 'https://www.example.com/backprop', 'type': '文章'},
                    {'title': '梯度下降优化', 'url': 'https://www.example.com/gradient-descent', 'type': '文章'},
                    {'title': '神经网络实现', 'url': 'https://www.example.com/nn-implement', 'type': '项目'}
                ],
                'duration': '20小时',
                'difficulty': '高级'
            }
        ]
    }
}

# 模拟论坛帖子数据
MOCK_FORUM_POSTS = [
    {
        'id': 1,
        'title': '如何开始学习 AI？',
        'content': '我是一个 AI 初学者，想了解如何系统地学习人工智能。请问应该从哪里开始？',
        'user_id': 2,
        'category': '问答',
        'views': 120,
        'likes': 15,
        'created_at': datetime.now() - timedelta(days=5),
        'comments_count': 8
    },
    {
        'id': 2,
        'title': '分享：使用 ChatGPT 提高工作效率的经验',
        'content': '最近在工作中大量使用 ChatGPT，发现它确实能显著提高工作效率。分享一下我的使用经验...',
        'user_id': 2,
        'category': '分享',
        'views': 200,
        'likes': 35,
        'created_at': datetime.now() - timedelta(days=3),
        'comments_count': 12
    },
    {
        'id': 3,
        'title': '如何选择合适的AI模型？',
        'content': '在选择AI模型时，需要考虑任务类型、数据规模、计算资源等多个因素。不同的模型有不同的特点和适用场景。',
        'user_id': 2,
        'category': '问答',
        'views': 85,
        'likes': 18,
        'created_at': datetime.now() - timedelta(days=4),
        'comments_count': 8
    },
    {
        'id': 4,
        'title': 'Transformer架构的优势是什么？',
        'content': 'Transformer架构通过自注意力机制实现了并行计算，相比RNN有更好的训练效率，同时能够捕捉长距离依赖关系。',
        'user_id': 1,
        'category': '讨论',
        'views': 120,
        'likes': 25,
        'created_at': datetime.now() - timedelta(days=5),
        'comments_count': 15
    },
    {
        'id': 5,
        'title': '推荐一些AI学习资源',
        'content': '想学习AI，但不知道从哪里开始。希望有经验的朋友推荐一些好的学习资源，包括书籍、课程、论文等。',
        'user_id': 2,
        'category': '求助',
        'views': 95,
        'likes': 22,
        'created_at': datetime.now() - timedelta(days=6),
        'comments_count': 20
    },
    {
        'id': 6,
        'title': 'AI在医疗领域的应用案例分享',
        'content': '最近在研究AI在医疗领域的应用，发现了很多有趣的案例。想和大家分享一下，也希望能听到更多的案例。',
        'user_id': 1,
        'category': '分享',
        'views': 150,
        'likes': 30,
        'created_at': datetime.now() - timedelta(days=7),
        'comments_count': 18
    },
    {
        'id': 7,
        'title': '深度学习框架选择：PyTorch还是TensorFlow？',
        'content': '作为初学者，在选择深度学习框架时很纠结。PyTorch和TensorFlow各有优势，不知道应该选择哪一个。',
        'user_id': 2,
        'category': '问答',
        'views': 110,
        'likes': 20,
        'created_at': datetime.now() - timedelta(days=8),
        'comments_count': 12
    },
    {
        'id': 8,
        'title': 'GPT-4的使用体验分享',
        'content': '最近使用了GPT-4，感觉在多个任务上都有很好的表现。想和大家分享一下使用体验，也希望能交流一些使用技巧。',
        'user_id': 1,
        'category': '分享',
        'views': 180,
        'likes': 35,
        'created_at': datetime.now() - timedelta(days=9),
        'comments_count': 25
    },
    {
        'id': 9,
        'title': '如何理解注意力机制？',
        'content': '注意力机制是Transformer的核心，但理解起来有些困难。有没有通俗易懂的解释或者可视化资源？',
        'user_id': 2,
        'category': '求助',
        'views': 100,
        'likes': 19,
        'created_at': datetime.now() - timedelta(days=10),
        'comments_count': 14
    },
    {
        'id': 10,
        'title': 'AI生成内容的版权问题讨论',
        'content': '随着AIGC技术的发展，AI生成内容的版权归属成为一个热点话题。大家怎么看这个问题？',
        'user_id': 1,
        'category': '讨论',
        'views': 140,
        'likes': 28,
        'created_at': datetime.now() - timedelta(days=11),
        'comments_count': 22
    },
    {
        'id': 11,
        'title': '推荐一些好用的AI工具',
        'content': '想收集一些实用的AI工具，包括图像生成、文本处理、代码辅助等各个方面的工具。',
        'user_id': 2,
        'category': '求助',
        'views': 130,
        'likes': 24,
        'created_at': datetime.now() - timedelta(days=12),
        'comments_count': 19
    },
    {
        'id': 12,
        'title': '神经网络反向传播算法详解',
        'content': '反向传播是训练神经网络的关键算法，通过链式法则计算梯度。本文详细解释反向传播的原理和实现。',
        'user_id': 1,
        'category': '分享',
        'views': 160,
        'likes': 32,
        'created_at': datetime.now() - timedelta(days=13),
        'comments_count': 16
    },
    {
        'id': 13,
        'title': '如何评估AI模型的性能？',
        'content': '评估AI模型性能需要选择合适的指标，不同任务有不同的评估方法。想了解一下常用的评估指标和方法。',
        'user_id': 2,
        'category': '问答',
        'views': 105,
        'likes': 21,
        'created_at': datetime.now() - timedelta(days=14),
        'comments_count': 11
    },
    {
        'id': 14,
        'title': 'AI伦理问题思考',
        'content': 'AI技术的发展带来了很多伦理问题，包括偏见、隐私、就业等。我们应该如何应对这些挑战？',
        'user_id': 1,
        'category': '讨论',
        'views': 170,
        'likes': 38,
        'created_at': datetime.now() - timedelta(days=15),
        'comments_count': 28
    },
    {
        'id': 15,
        'title': '大模型训练的技术细节',
        'content': '想了解大模型训练过程中的一些技术细节，包括数据预处理、模型架构设计、训练策略等。',
        'user_id': 2,
        'category': '问答',
        'views': 125,
        'likes': 26,
        'created_at': datetime.now() - timedelta(days=16),
        'comments_count': 17
    }
]

# 模拟评论数据（按帖子ID组织）
MOCK_COMMENTS = {
    1: [  # 帖子ID为1的评论
        {
            'id': 1,
            'user_id': 2,
            'content': '这篇文章写得太好了！让我对AI有了更深入的理解。',
            'created_at': datetime.now() - timedelta(hours=2),
            'likes': 15,
            'replies': [
                {
                    'id': 11,
                    'user_id': 3,
                    'content': '同感！特别是关于Transformer的部分，解释得很清楚。',
                    'created_at': datetime.now() - timedelta(hours=1),
                    'likes': 5
                }
            ]
        },
        {
            'id': 2,
            'user_id': 3,
            'content': '请问有没有相关的实践项目可以推荐？',
            'created_at': datetime.now() - timedelta(hours=5),
            'likes': 8,
            'replies': []
        },
        {
            'id': 3,
            'user_id': 4,
            'content': '感谢分享，收藏了！',
            'created_at': datetime.now() - timedelta(hours=8),
            'likes': 3,
            'replies': []
        },
        {
            'id': 4,
            'user_id': 5,
            'content': '这个技术在实际应用中有什么限制吗？',
            'created_at': datetime.now() - timedelta(days=1),
            'likes': 12,
            'replies': [
                {
                    'id': 12,
                    'user_id': 1,
                    'content': '主要限制是计算资源需求较大，需要GPU支持。',
                    'created_at': datetime.now() - timedelta(hours=20),
                    'likes': 7
                }
            ]
        },
        {
            'id': 5,
            'user_id': 2,
            'content': '期待更多关于深度学习的文章！',
            'created_at': datetime.now() - timedelta(days=1, hours=5),
            'likes': 6,
            'replies': []
        },
        {
            'id': 6,
            'user_id': 3,
            'content': '这个解释比我在其他地方看到的都要清晰。',
            'created_at': datetime.now() - timedelta(days=2),
            'likes': 9,
            'replies': []
        },
        {
            'id': 7,
            'user_id': 4,
            'content': '有没有相关的视频教程推荐？',
            'created_at': datetime.now() - timedelta(days=2, hours=3),
            'likes': 4,
            'replies': []
        },
        {
            'id': 8,
            'user_id': 5,
            'content': '这个技术栈现在在业界应用广泛吗？',
            'created_at': datetime.now() - timedelta(days=3),
            'likes': 11,
            'replies': [
                {
                    'id': 13,
                    'user_id': 1,
                    'content': '是的，很多大公司都在使用，比如Google、OpenAI等。',
                    'created_at': datetime.now() - timedelta(days=2, hours=10),
                    'likes': 8
                }
            ]
        },
        {
            'id': 9,
            'user_id': 2,
            'content': '对于初学者来说，这个难度如何？',
            'created_at': datetime.now() - timedelta(days=3, hours=8),
            'likes': 5,
            'replies': []
        },
        {
            'id': 10,
            'user_id': 3,
            'content': '感谢楼主的详细解答，受益匪浅！',
            'created_at': datetime.now() - timedelta(days=4),
            'likes': 7,
            'replies': []
        }
    ],
    2: [  # 帖子ID为2的评论
        {
            'id': 21,
            'user_id': 3,
            'content': '这个工具确实很好用，我已经在用了一段时间了。',
            'created_at': datetime.now() - timedelta(hours=1),
            'likes': 10,
            'replies': []
        },
        {
            'id': 22,
            'user_id': 4,
            'content': '请问免费版和付费版有什么区别？',
            'created_at': datetime.now() - timedelta(hours=3),
            'likes': 6,
            'replies': []
        },
        {
            'id': 23,
            'user_id': 5,
            'content': '有没有中文支持？',
            'created_at': datetime.now() - timedelta(hours=6),
            'likes': 8,
            'replies': []
        },
        {
            'id': 24,
            'user_id': 2,
            'content': '这个工具的输出质量如何？',
            'created_at': datetime.now() - timedelta(days=1),
            'likes': 5,
            'replies': []
        },
        {
            'id': 25,
            'user_id': 3,
            'content': '推荐给需要的朋友！',
            'created_at': datetime.now() - timedelta(days=1, hours=5),
            'likes': 4,
            'replies': []
        },
        {
            'id': 26,
            'user_id': 4,
            'content': '有没有使用教程？',
            'created_at': datetime.now() - timedelta(days=2),
            'likes': 7,
            'replies': []
        },
        {
            'id': 27,
            'user_id': 5,
            'content': '这个工具支持哪些格式？',
            'created_at': datetime.now() - timedelta(days=2, hours=8),
            'likes': 3,
            'replies': []
        },
        {
            'id': 28,
            'user_id': 2,
            'content': '感谢分享，已经收藏了！',
            'created_at': datetime.now() - timedelta(days=3),
            'likes': 6,
            'replies': []
        }
    ]
}

# 为所有帖子添加默认评论（如果帖子没有评论）
for post in MOCK_FORUM_POSTS:
    if post['id'] not in MOCK_COMMENTS:
        MOCK_COMMENTS[post['id']] = []
    # 基于真实评论数据更新评论数
    post['comments_count'] = len(MOCK_COMMENTS.get(post['id'], []))

# 模拟消息数据
MOCK_MESSAGES = {
    1: [  # 用户ID为1的消息
        {
            'id': 1,
            'type': 'reply',  # reply, like, favorite
            'content': '用户"张三"回复了您的评论',
            'related_id': 1,  # 评论ID或帖子ID
            'related_type': 'comment',
            'from_user_id': 2,
            'created_at': datetime.now() - timedelta(hours=1),
            'read': False
        },
        {
            'id': 2,
            'type': 'like',
            'content': '用户"李四"点赞了您的帖子',
            'related_id': 1,
            'related_type': 'post',
            'from_user_id': 3,
            'created_at': datetime.now() - timedelta(hours=3),
            'read': False
        },
        {
            'id': 3,
            'type': 'favorite',
            'content': '用户"王五"收藏了您的帖子',
            'related_id': 1,
            'related_type': 'post',
            'from_user_id': 4,
            'created_at': datetime.now() - timedelta(days=1),
            'read': True
        }
    ]
}

# 模拟用户收藏数据
MOCK_FAVORITES = {
    1: [2, 3],  # 用户ID为1收藏了帖子ID 2和3
    2: [1, 4],
    3: [1, 2, 5]
}

# 模拟用户点赞数据
MOCK_LIKES = {
    'posts': {
        1: [2, 3, 4],  # 帖子ID为1被用户2,3,4点赞
        2: [1, 3, 5]
    },
    'comments': {
        1: [2, 3],  # 评论ID为1被用户2,3点赞
        2: [1, 4, 5]
    },
    'replies': {
        11: [1, 2]  # 回复ID为11被用户1,2点赞
    }
}

# 确保所有评论和回复都有对应的点赞数据初始化
if 'comments' not in MOCK_LIKES:
    MOCK_LIKES['comments'] = {}
if 'replies' not in MOCK_LIKES:
    MOCK_LIKES['replies'] = {}

for post_id, comments_list in MOCK_COMMENTS.items():
    for comment in comments_list:
        comment_id = comment['id']
        if comment_id not in MOCK_LIKES['comments']:
            MOCK_LIKES['comments'][comment_id] = []
        # 处理回复
        for reply in comment.get('replies', []):
            reply_id = reply['id']
            if reply_id not in MOCK_LIKES['replies']:
                MOCK_LIKES['replies'][reply_id] = []

# 初始化点赞数据，确保每个帖子的点赞数基于真实数据
if 'posts' not in MOCK_LIKES:
    MOCK_LIKES['posts'] = {}
for post in MOCK_FORUM_POSTS:
    post_id = post['id']
    if post_id not in MOCK_LIKES['posts']:
        MOCK_LIKES['posts'][post_id] = []
    # 基于真实点赞数据更新点赞数
    post['likes'] = len(MOCK_LIKES['posts'][post_id])

# 模拟访问统计数据 {date_str: count}
MOCK_VISIT_STATS = {}

# AI使用历史记录（临时存储，实际应使用数据库）
MOCK_AI_USAGE_HISTORY = []

def get_user_by_username(username):
    """根据用户名获取用户（优先从数据库，如果找不到则从MOCK_USERS）"""
    # 首先尝试从数据库读取
    try:
        import pymysql
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        db_user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if db_user:
            # 将数据库用户格式转换为与MOCK_USERS一致的格式
            user_data = {
                'id': db_user['id'],
                'username': db_user['username'],
                'nickname': db_user.get('nickname', db_user['username']),
                'email': db_user['email'],
                'password': db_user['password_hash'],  # 数据库中是password_hash，转换为password
                'role': db_user.get('role', 'user'),
                'avatar': db_user.get('avatar', 'default.jpg'),
                'security_question': '',  # 数据库中没有此字段，设为空
                'security_answer': '',
                'interests': [],
                'favorites': {},
                'likes': {},
                'messages': [],
                'first_login': False
            }
            return user_data
    except ImportError:
        # pymysql未安装，跳过数据库查询
        pass
    except Exception as e:
        # 如果数据库连接失败或表不存在，继续使用MOCK_USERS
        # 只在调试模式下打印错误，避免生产环境日志过多
        import sys
        if hasattr(sys, '_getframe') and '--debug' in sys.argv:
            print(f"从数据库读取用户失败: {str(e)}，使用MOCK_USERS")
        pass
    
    # 如果数据库中没有找到，从MOCK_USERS中查找
    for user in MOCK_USERS:
        if user['username'] == username:
            return user
    return None

def get_user_by_id(user_id):
    """根据ID获取用户（优先从数据库，如果找不到则从MOCK_USERS）"""
    # 首先尝试从数据库读取
    try:
        import pymysql
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        db_user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if db_user:
            # 将数据库用户格式转换为与MOCK_USERS一致的格式
            user_data = {
                'id': db_user['id'],
                'username': db_user['username'],
                'nickname': db_user.get('nickname', db_user['username']),
                'email': db_user['email'],
                'password': db_user['password_hash'],  # 数据库中是password_hash，转换为password
                'role': db_user.get('role', 'user'),
                'avatar': db_user.get('avatar', 'default.jpg'),
                'security_question': '',  # 数据库中没有此字段，设为空
                'security_answer': '',
                'interests': [],
                'favorites': {},
                'likes': {},
                'messages': [],
                'first_login': False
            }
            return user_data
    except ImportError:
        # pymysql未安装，跳过数据库查询
        pass
    except Exception as e:
        # 如果数据库连接失败或表不存在，继续使用MOCK_USERS
        # 只在调试模式下打印错误，避免生产环境日志过多
        import sys
        if hasattr(sys, '_getframe') and '--debug' in sys.argv:
            print(f"从数据库读取用户失败: {str(e)}，使用MOCK_USERS")
        pass
    
    # 如果数据库中没有找到，从MOCK_USERS中查找
    for user in MOCK_USERS:
        if user['id'] == user_id:
            return user
    return None

def get_all_terms_from_db():
    """从数据库获取所有术语（优先从数据库，如果失败则从MOCK_TERMS）"""
    try:
        import pymysql
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM terms ORDER BY id")
        db_terms = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if db_terms:
            # 将数据库术语格式转换为与MOCK_TERMS一致的格式
            terms = []
            for db_term in db_terms:
                term_data = {
                    'id': db_term['id'],
                    'term': db_term['term'],
                    'definition': db_term['definition'],
                    'category': db_term.get('category', ''),
                    'related_terms': db_term.get('related_terms'),
                    'examples': db_term.get('examples'),
                    'image_path': db_term.get('image_path'),
                    'video_url': db_term.get('video_url'),
                    'video_title': db_term.get('video_title'),
                    'video_description': db_term.get('video_description'),
                    'knowledge_graph_json': db_term.get('knowledge_graph_json')
                }
                terms.append(term_data)
            return terms
    except ImportError:
        # pymysql未安装，跳过数据库查询
        pass
    except Exception as e:
        # 如果数据库连接失败或表不存在，继续使用MOCK_TERMS
        import sys
        if hasattr(sys, '_getframe') and '--debug' in sys.argv:
            print(f"从数据库读取术语失败: {str(e)}，使用MOCK_TERMS")
        pass
    
    # 如果数据库中没有找到，返回MOCK_TERMS
    return MOCK_TERMS


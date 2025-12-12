"""
模拟数据文件
在数据库建立之前使用模拟数据
"""
from datetime import datetime, timedelta

# 模拟用户数据
MOCK_USERS = [
    {
        'id': 1,
        'username': 'admin',
        'email': 'admin@aicove.com',
        'password': 'admin123',  # 实际应用中应该使用哈希
        'role': 'admin'
    },
    {
        'id': 2,
        'username': 'testuser',
        'email': 'test@aicove.com',
        'password': 'test123',
        'role': 'user'
    }
]

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
        'is_featured': True
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
        'is_featured': False
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
        'is_featured': True
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
        'is_featured': False
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
        'id': 5,
        'name': 'Claude',
        'description': 'Anthropic 开发的安全、可靠的大语言模型',
        'category': '大模型',
        'url': 'https://www.anthropic.com',
        'icon': '🤖',
        'rating': 4.7,
        'rating_count': 900
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
        'external_link': '#',
        'tags': '个性化学习,教育,AI',
        'created_at': datetime.now() - timedelta(days=8)
    },
    {
        'id': 3,
        'title': 'AI 科研助手',
        'description': '利用 AI 技术加速科研文献检索和分析，提高研究效率',
        'industry': 'AI+科研',
        'image': None,
        'external_link': '#',
        'tags': '科研,文献检索,AI',
        'created_at': datetime.now() - timedelta(days=6)
    },
    {
        'id': 4,
        'title': '智能办公系统',
        'description': 'AI 驱动的办公自动化系统，提升工作效率',
        'industry': 'AI+办公',
        'image': None,
        'external_link': '#',
        'tags': '办公自动化,效率,AI',
        'created_at': datetime.now() - timedelta(days=4)
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
        'examples': 'ChatGPT, GPT-4, Claude'
    },
    {
        'id': 2,
        'term': 'Transformer',
        'definition': 'Transformer 是一种基于自注意力机制的神经网络架构，广泛应用于自然语言处理任务。',
        'category': 'Transformer',
        'related_terms': '1',
        'examples': 'BERT, GPT, T5'
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
        'examples': '多层感知机, CNN, RNN'
    },
    {
        'id': 5,
        'term': '深度学习',
        'definition': '深度学习是机器学习的一个分支，使用多层神经网络来学习数据的表示。',
        'category': '核心概念',
        'related_terms': '4',
        'examples': '深度神经网络, 卷积神经网络'
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
        'url': '#',
        'created_at': datetime.now() - timedelta(days=20)
    },
    {
        'id': 2,
        'title': 'Attention Is All You Need',
        'author': 'Vaswani et al.',
        'type': '论文',
        'description': 'Transformer 架构的原始论文，提出了自注意力机制。',
        'cover_image': None,
        'url': '#',
        'created_at': datetime.now() - timedelta(days=15)
    },
    {
        'id': 3,
        'title': '机器学习课程',
        'author': 'Andrew Ng',
        'type': '课程',
        'description': 'Coursera 上的经典机器学习课程，适合初学者。',
        'cover_image': None,
        'url': '#',
        'created_at': datetime.now() - timedelta(days=10)
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
        'created_at': datetime.now() - timedelta(days=15)
    }
]

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
    }
]

# 模拟评论数据
MOCK_COMMENTS = []

def get_user_by_username(username):
    """根据用户名获取用户"""
    for user in MOCK_USERS:
        if user['username'] == username:
            return user
    return None

def get_user_by_id(user_id):
    """根据ID获取用户"""
    for user in MOCK_USERS:
        if user['id'] == user_id:
            return user
    return None


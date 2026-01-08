# -*- coding: utf-8 -*-
"""
标记体系模块
统一管理所有标记和分类，基于标记体系.xlsx中的定义
"""

# 网站功能模块
FUNCTIONAL_MODULES = {
    '首页': {
        'variants': ['网站首页', 'Home'],
        'children': ['新手引导', '热门科普', '最新资讯', '搜索', '热门大模型', '其他功能入口']
    },
    'AI 基础': {
        'variants': ['AI 基础知识'],
        'children': ['核心概念', 'AI 发展史', '学习路径']
    },
    'AI 实验室': {
        'variants': ['AI 实验模块', 'AILab'],
        'children': ['AI 游乐场', '模型透视']
    },
    '应用场景': {
        'variants': ['AI 应用领域'],
        'children': ['案例库', 'AI工具箱']
    },
    '伦理与未来': {
        'variants': ['AI 伦理', 'AI 未来趋势'],
        'children': ['AI安全', '数据隐私', 'AI偏见与公平', 'AI与就业']
    },
    '资源中心': {
        'variants': ['学习资源库'],
        'children': ['推荐阅读', '课程推荐', 'AI术语表']
    },
    '社区': {
        'variants': ['互动社区', 'Community'],
        'children': ['问答论坛', 'AI 助教', '关于我们', '隐私政策', '使用指南']
    },
    '站内搜索': {
        'variants': ['网站检索'],
        'children': ['普通搜索', '高级检索', 'AI检索']
    }
}

# 内容类型
CONTENT_TYPES = {
    '科普文章': {
        'variants': ['科普帖子', '图文科普'],
        'children': ['入门概念解析', '技术趋势分析', '案例图文', '热点追踪']
    },
    '科普视频': {
        'variants': ['视频科普', '教程视频'],
        'children': ['核心概念讲解', '工具使用教程', '论文精读视频', '行业应用演示']
    },
    '资讯动态': {
        'variants': ['行业动态', 'AI 新闻'],
        'children': ['技术突破', '行业政策', '企业动态', '新模型发布']
    }
}

# 学习难度
DIFFICULTY_LEVELS = {
    '入门级': {
        'variants': ['新手友好型', '小白级'],
        'children': ['基础概念讲解']
    },
    '进阶级': {
        'variants': ['应用级', '实操级'],
        'children': ['工具使用指南', '行业应用技巧', '进阶概念解析', '代码入门教程']
    },
    '专业级': {
        'variants': ['科研级', '深度级'],
        'children': ['论文精读', '技术原理拆解', '模型训练优化', '开源项目实操']
    }
}

# 用户角色
USER_ROLES = {
    '新手小白': {
        'variants': ['无 AI 基础用户', '入门者'],
        'description': '想了解 AI 基础、零代码体验需求、避免专业黑话的用户'
    },
    '职场人': {
        'variants': ['职场从业者'],
        'description': '需 AI 提升工作效率、关注 AI+办公应用、担忧就业影响的用户'
    },
    '学生': {
        'variants': ['大学生', '高校学生'],
        'description': '计算机相关专业、非专业兴趣学习、课程作业 / Pre 辅助需求的用户'
    },
    '科研人员': {
        'variants': ['博士生', '研究人员', 'AI 研究者'],
        'description': '追踪技术前沿、论文撰写、模型优化、文献梳理需求的用户'
    }
}

# 技术方向
TECH_DIRECTIONS = {
    'LLM': {
        'variants': ['大语言模型', '大型语言模型'],
        'children': ['ChatGPT', '文心一言', '豆包']
    },
    'Transformer': {
        'variants': ['Transformer 架构'],
        'children': ['注意力机制', '编码器 - 解码器', '预训练模型基础']
    },
    '扩散模型': {
        'variants': ['Diffusion 模型'],
        'children': ['图像生成', '视频生成', '时序一致性优化']
    },
    '神经网络': {
        'variants': ['神经网络模型'],
        'children': ['卷积池化层', '全连接网络', '词向量空间', '模型透视', '迁移学习']
    },
    '图像生成': {
        'variants': ['文生图', '图生图'],
        'children': ['海报生成', '创意设计', '图像优化']
    },
    '视频生成': {
        'variants': ['文生视频', '视频优化'],
        'children': ['时序一致性', '跨帧注意力机制', '视频内容生成']
    },
    'RAG': {
        'variants': ['检索增强生成'],
        'children': ['站内答疑', '知识库检索', '精准问答']
    }
}

# 伦理议题
ETHICS_TOPICS = {
    'AI 安全': {
        'variants': ['人工智能安全'],
        'children': ['模型安全', '数据泄露防护', '恶意使用规避']
    },
    '数据隐私': {
        'variants': ['隐私保护'],
        'children': ['用户数据使用规范', '隐私政策', '数据匿名化']
    },
    'AI 偏见': {
        'variants': ['算法偏见', '公平性问题'],
        'children': ['数据偏见', '决策公平性', '弱势群体保护']
    },
    '就业影响': {
        'variants': ['AI 与就业', '职场替代焦虑'],
        'children': ['人机协作', '职业技能升级', '新岗位创造']
    }
}

# 工具资源
TOOL_RESOURCES = {
    '开源代码': {
        'variants': ['开源项目', '代码资源'],
        'children': ['Github 项目', 'Huggingface 模型', '代码教程', '实操案例'],
        'note': '可提供部分GitHub或huggingface开源项目跳转链接'
    },
    'AI 工具箱': {
        'variants': ['实用 AI 工具', '工具推荐'],
        'children': ['办公工具', '创作工具', '科研工具', '测评推荐']
    },
    '问答论坛': {
        'variants': ['社区问答', '用户提问'],
        'children': ['长尾疑问解答', 'UGC 知识库', '专业人士答疑']
    }
}

# 标记映射函数
def get_tag_category(tag):
    """根据标记返回其所属的分类"""
    tag_lower = tag.lower()
    
    # 检查功能模块
    for module, data in FUNCTIONAL_MODULES.items():
        if module == tag or tag in data.get('variants', []):
            return 'functional_module'
        if tag in data.get('children', []):
            return 'functional_module'
    
    # 检查内容类型
    for content_type, data in CONTENT_TYPES.items():
        if content_type == tag or tag in data.get('variants', []):
            return 'content_type'
        if tag in data.get('children', []):
            return 'content_type'
    
    # 检查学习难度
    for level, data in DIFFICULTY_LEVELS.items():
        if level == tag or tag in data.get('variants', []):
            return 'difficulty_level'
    
    # 检查用户角色
    for role, data in USER_ROLES.items():
        if role == tag or tag in data.get('variants', []):
            return 'user_role'
    
    # 检查技术方向
    for tech, data in TECH_DIRECTIONS.items():
        if tech == tag or tag in data.get('variants', []):
            return 'tech_direction'
        if tag in data.get('children', []):
            return 'tech_direction'
    
    # 检查伦理议题
    for topic, data in ETHICS_TOPICS.items():
        if topic == tag or tag in data.get('variants', []):
            return 'ethics_topic'
        if tag in data.get('children', []):
            return 'ethics_topic'
    
    # 检查工具资源
    for resource, data in TOOL_RESOURCES.items():
        if resource == tag or tag in data.get('variants', []):
            return 'tool_resource'
        if tag in data.get('children', []):
            return 'tool_resource'
    
    return 'unknown'

def normalize_tag(tag):
    """规范化标记，返回优选术语"""
    tag_lower = tag.lower()
    
    all_tags = {}
    all_tags.update(FUNCTIONAL_MODULES)
    all_tags.update(CONTENT_TYPES)
    all_tags.update(DIFFICULTY_LEVELS)
    all_tags.update(USER_ROLES)
    all_tags.update(TECH_DIRECTIONS)
    all_tags.update(ETHICS_TOPICS)
    all_tags.update(TOOL_RESOURCES)
    
    # 检查是否为优选术语
    if tag in all_tags:
        return tag
    
    # 检查变体
    for preferred_term, data in all_tags.items():
        variants = data.get('variants', [])
        if tag in variants:
            return preferred_term
        
        # 检查子词
        children = data.get('children', [])
        if tag in children:
            return preferred_term
    
    return tag

def get_all_tags_by_category():
    """按分类返回所有标记"""
    return {
        'functional_modules': list(FUNCTIONAL_MODULES.keys()),
        'content_types': list(CONTENT_TYPES.keys()),
        'difficulty_levels': list(DIFFICULTY_LEVELS.keys()),
        'user_roles': list(USER_ROLES.keys()),
        'tech_directions': list(TECH_DIRECTIONS.keys()),
        'ethics_topics': list(ETHICS_TOPICS.keys()),
        'tool_resources': list(TOOL_RESOURCES.keys())
    }

def get_valid_categories_for_articles():
    """获取文章的有效分类（基于内容类型）"""
    return list(CONTENT_TYPES.keys())

def get_valid_categories_for_tools():
    """获取工具的有效分类（基于技术方向）"""
    tech_categories = list(TECH_DIRECTIONS.keys())
    # 添加常用的工具分类
    tech_categories.extend(['图像生成', '写作', '翻译', '编程', '研究', 'PPT制作'])
    return tech_categories

def get_valid_categories_for_cases():
    """获取案例的有效分类（基于行业）"""
    # 从应用场景的子词中提取
    return ['AI+艺术', 'AI+创意', 'AI+医疗', 'AI+教育', 'AI+科研', 'AI+办公', 'AI+金融']

def get_valid_categories_for_terms():
    """获取术语的有效分类（基于技术方向）"""
    return list(TECH_DIRECTIONS.keys()) + ['核心概念']

def normalize_article_category(category):
    """规范化文章分类"""
    if not category:
        return None
    
    # 映射旧分类到新分类
    category_mapping = {
        '热门科普': '科普文章',
        '最新资讯': '资讯动态',
        '科普': '科普文章',
        '资讯': '资讯动态',
        '新闻': '资讯动态'
    }
    
    normalized = category_mapping.get(category, category)
    
    # 检查是否在有效分类中
    valid_categories = get_valid_categories_for_articles()
    if normalized in valid_categories:
        return normalized
    
    # 如果不在，尝试规范化
    return normalize_tag(normalized)

def normalize_tool_category(category):
    """规范化工具分类"""
    if not category:
        return None
    
    # 映射旧分类到新分类
    category_mapping = {
        '大模型': 'LLM',
        'LLM': 'LLM'
    }
    
    normalized = category_mapping.get(category, category)
    
    # 检查是否在有效分类中
    valid_categories = get_valid_categories_for_tools()
    if normalized in valid_categories:
        return normalized
    
    return normalize_tag(normalized)

def normalize_term_category(category):
    """规范化术语分类"""
    if not category:
        return None
    
    # 检查是否在有效分类中
    valid_categories = get_valid_categories_for_terms()
    if category in valid_categories:
        return category
    
    return normalize_tag(category)


"""
数据库初始化脚本
用于创建数据库表并插入示例数据
"""
from app import create_app, db
from app.models import (
    User, Article, Tool, Case, ForumPost, Comment,
    Term, Resource, EthicsTopic
)
from config import Config

def init_database():
    """初始化数据库"""
    app = create_app(Config)
    
    with app.app_context():
        # 删除所有表（谨慎使用）
        # db.drop_all()
        
        # 创建所有表
        db.create_all()
        
        # 创建示例用户
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@aicove.com')
            admin.set_password('admin123')
            admin.role = 'admin'
            db.session.add(admin)
            
            test_user = User(username='testuser', email='test@aicove.com')
            test_user.set_password('test123')
            db.session.add(test_user)
        
        # 创建示例文章
        if Article.query.count() == 0:
            articles = [
                Article(
                    title='什么是大语言模型（LLM）？',
                    content='大语言模型（Large Language Model, LLM）是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。它们通过在海量文本数据上训练，学习语言的统计规律和语义关系。',
                    category='热门科普',
                    is_featured=True,
                    views=150,
                    likes=25
                ),
                Article(
                    title='ChatGPT 的工作原理',
                    content='ChatGPT 基于 Transformer 架构，使用自注意力机制处理序列数据。它通过预训练和微调两个阶段，学习语言的生成模式，能够根据上下文生成连贯的回复。',
                    category='热门科普',
                    is_featured=True,
                    views=200,
                    likes=35
                ),
                Article(
                    title='AI 在医疗领域的应用',
                    content='人工智能在医疗领域有着广泛的应用，包括医学影像分析、疾病诊断、药物研发等。AI 技术能够帮助医生提高诊断准确率，缩短诊断时间。',
                    category='最新资讯',
                    views=120,
                    likes=20
                ),
            ]
            for article in articles:
                db.session.add(article)
        
        # 创建示例工具
        if Tool.query.count() == 0:
            tools = [
                Tool(
                    name='ChatGPT',
                    description='OpenAI 开发的大语言模型，支持对话、写作、编程等多种任务',
                    category='大模型',
                    url='https://chat.openai.com',
                    rating=4.8,
                    rating_count=1000
                ),
                Tool(
                    name='Midjourney',
                    description='强大的 AI 图像生成工具，能够根据文本描述生成高质量图像',
                    category='图像生成',
                    url='https://www.midjourney.com',
                    rating=4.7,
                    rating_count=800
                ),
                Tool(
                    name='GitHub Copilot',
                    description='AI 编程助手，能够根据代码上下文自动生成代码',
                    category='编程',
                    url='https://github.com/features/copilot',
                    rating=4.6,
                    rating_count=600
                ),
            ]
            for tool in tools:
                db.session.add(tool)
        
        # 创建示例案例
        if Case.query.count() == 0:
            cases = [
                Case(
                    title='AI 辅助医学影像诊断',
                    description='使用深度学习技术分析医学影像，帮助医生快速准确地识别病变',
                    industry='AI+医疗',
                    tags='深度学习,医学影像,诊断',
                    external_link='#'
                ),
                Case(
                    title='智能教育平台',
                    description='基于 AI 的个性化学习系统，根据学生特点提供定制化教学内容',
                    industry='AI+教育',
                    tags='个性化学习,教育,AI',
                    external_link='#'
                ),
            ]
            for case in cases:
                db.session.add(case)
        
        # 创建示例术语
        if Term.query.count() == 0:
            terms = [
                Term(
                    term='LLM',
                    definition='大语言模型（Large Language Model），是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。',
                    category='LLM',
                    examples='ChatGPT, GPT-4, Claude'
                ),
                Term(
                    term='Transformer',
                    definition='Transformer 是一种基于自注意力机制的神经网络架构，广泛应用于自然语言处理任务。',
                    category='Transformer',
                    examples='BERT, GPT, T5'
                ),
                Term(
                    term='扩散模型',
                    definition='扩散模型（Diffusion Model）是一种生成模型，通过逐步去噪过程生成高质量图像。',
                    category='扩散模型',
                    examples='DALL-E 2, Stable Diffusion, Midjourney'
                ),
            ]
            for term in terms:
                db.session.add(term)
        
        # 创建示例资源
        if Resource.query.count() == 0:
            resources = [
                Resource(
                    title='深度学习',
                    author='Ian Goodfellow',
                    type='书籍',
                    description='深度学习领域的经典教材，全面介绍深度学习的基础理论和实践方法。',
                    url='#'
                ),
                Resource(
                    title='Attention Is All You Need',
                    author='Vaswani et al.',
                    type='论文',
                    description='Transformer 架构的原始论文，提出了自注意力机制。',
                    url='#'
                ),
            ]
            for resource in resources:
                db.session.add(resource)
        
        # 创建示例伦理专题
        if EthicsTopic.query.count() == 0:
            topics = [
                EthicsTopic(
                    title='AI 安全',
                    slug='ai-safety',
                    description='探讨 AI 系统的安全性问题，包括对抗攻击、模型鲁棒性等',
                    background='随着 AI 技术的快速发展，AI 系统的安全性问题日益凸显。如何确保 AI 系统在各种情况下都能安全可靠地运行，是一个重要的研究课题。',
                    key_issues='对抗样本攻击、模型鲁棒性、系统可靠性、安全部署',
                    expert_views='专家认为，AI 安全需要从多个维度进行保障，包括模型设计、训练过程、部署环境等。'
                ),
                EthicsTopic(
                    title='AI 偏见与公平',
                    slug='ai-bias-fairness',
                    description='讨论 AI 系统中的偏见问题，以及如何实现算法公平',
                    background='AI 系统可能从训练数据中学习到偏见，导致对某些群体的不公平对待。',
                    key_issues='数据偏见、算法偏见、公平性评估、去偏见方法',
                    expert_views='实现算法公平需要从数据收集、模型设计、评估指标等多个环节进行考虑。'
                ),
            ]
            for topic in topics:
                db.session.add(topic)
        
        # 提交所有更改
        db.session.commit()
        print('数据库初始化完成！')
        print('默认管理员账号：admin / admin123')
        print('测试用户账号：testuser / test123')

if __name__ == '__main__':
    init_database()


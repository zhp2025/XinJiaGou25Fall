from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.mock_data import (
    MOCK_ARTICLES, MOCK_TOOLS, MOCK_CASES, MOCK_TERMS, 
    MOCK_RESOURCES, MOCK_ETHICS_TOPICS, MOCK_FORUM_POSTS,
    get_user_by_username, get_user_by_id
)
from app import MockUser
from datetime import datetime

# 主蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页"""
    # 获取热门科普文章
    popular_articles = [a for a in MOCK_ARTICLES if a['category'] == '热门科普' and a.get('is_featured', False)]
    popular_articles = sorted(popular_articles, key=lambda x: x['views'], reverse=True)[:6]
    
    # 获取最新资讯
    latest_news = [a for a in MOCK_ARTICLES if a['category'] == '最新资讯']
    latest_news = sorted(latest_news, key=lambda x: x['created_at'], reverse=True)[:6]
    
    # 获取热门大模型（从工具中筛选）
    popular_models = [t for t in MOCK_TOOLS if t['category'] in ['大模型', 'LLM']]
    popular_models = sorted(popular_models, key=lambda x: x['rating'], reverse=True)[:6]
    
    return render_template('index.html', 
                         popular_articles=popular_articles,
                         latest_news=latest_news,
                         popular_models=popular_models)


@main_bp.route('/ai-basics')
def ai_basics():
    """AI基础模块"""
    # 获取核心概念（术语）
    core_concepts = [t for t in MOCK_TERMS if t['category'] in ['LLM', 'Transformer', '扩散模型', '核心概念']]
    
    return render_template('ai_basics.html', core_concepts=core_concepts)


@main_bp.route('/ai-lab')
def ai_lab():
    """AI实验室模块"""
    return render_template('ai_lab.html')


@main_bp.route('/applications')
def applications():
    """应用场景模块"""
    # 获取所有案例
    cases = sorted(MOCK_CASES, key=lambda x: x['created_at'], reverse=True)
    
    # 获取所有工具
    tools = sorted(MOCK_TOOLS, key=lambda x: x['rating'], reverse=True)
    
    return render_template('applications.html', cases=cases, tools=tools)


@main_bp.route('/ethics')
def ethics():
    """伦理与未来模块"""
    topics = sorted(MOCK_ETHICS_TOPICS, key=lambda x: x['created_at'], reverse=True)
    return render_template('ethics.html', topics=topics)


@main_bp.route('/ethics/<slug>')
def ethics_topic(slug):
    """伦理专题详情页"""
    topic = next((t for t in MOCK_ETHICS_TOPICS if t['slug'] == slug), None)
    if not topic:
        flash('专题不存在')
        return redirect(url_for('main.ethics'))
    
    # 模拟评论（暂时为空）
    comments = []
    
    return render_template('ethics_topic.html', topic=topic, comments=comments)


@main_bp.route('/resources')
def resources():
    """资源中心模块"""
    # 获取所有术语（按字母排序）
    terms = sorted(MOCK_TERMS, key=lambda x: x['term'])
    
    # 获取推荐阅读资源
    resources = sorted(MOCK_RESOURCES, key=lambda x: x['created_at'], reverse=True)
    
    return render_template('resources.html', terms=terms, resources=resources)


@main_bp.route('/community')
def community():
    """社区模块"""
    # 获取热门帖子
    hot_posts = sorted(MOCK_FORUM_POSTS, key=lambda x: (x['likes'], x['views']), reverse=True)[:10]
    
    # 为帖子添加作者信息
    for post in hot_posts:
        user = get_user_by_id(post['user_id'])
        if user:
            display_name = user.get('nickname', user['username'])
            post['author'] = {'username': display_name}
        else:
            post['author'] = {'username': '未知用户'}
        post['comments_count'] = post.get('comments_count', 0)
    
    return render_template('community.html', hot_posts=hot_posts)


@main_bp.route('/community/forum')
def forum():
    """问答论坛"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 为帖子添加作者信息
    posts_list = []
    for post in MOCK_FORUM_POSTS:
        user = get_user_by_id(post['user_id'])
        post_copy = post.copy()
        post_copy['author'] = {'username': user['username']} if user else {'username': '未知用户'}
        post_copy['comments_count'] = post.get('comments_count', 0)
        posts_list.append(post_copy)
    
    posts_list = sorted(posts_list, key=lambda x: x['created_at'], reverse=True)
    
    # 简单分页
    total = len(posts_list)
    start = (page - 1) * per_page
    end = start + per_page
    posts = posts_list[start:end]
    
    # 创建分页对象（模拟）
    class Pagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
        
        def iter_pages(self, left_edge=1, right_edge=1, left_current=2, right_current=2):
            last = self.pages
            for num in range(1, last + 1):
                if num <= left_edge or \
                   (num > self.page - left_current - 1 and num < self.page + right_current) or \
                   num > last - right_edge:
                    yield num
                else:
                    yield None
    
    pagination = Pagination(posts, page, per_page, total)
    
    return render_template('forum.html', posts=pagination)


@main_bp.route('/community/forum/<int:post_id>')
def forum_post(post_id):
    """论坛帖子详情"""
    post = next((p for p in MOCK_FORUM_POSTS if p['id'] == post_id), None)
    if not post:
        flash('帖子不存在')
        return redirect(url_for('main.forum'))
    
    post['views'] += 1
    user = get_user_by_id(post['user_id'])
    post['author'] = {'username': user['username']} if user else {'username': '未知用户'}
    
    # 模拟评论（暂时为空）
    comments = []
    
    return render_template('forum_post.html', post=post, comments=comments)


@main_bp.route('/community/ai-assistant')
def ai_assistant():
    """AI助教（RAG站内答疑）"""
    return render_template('ai_assistant.html')


@main_bp.route('/community/about')
def about():
    """关于我们"""
    return render_template('about.html')


@main_bp.route('/community/privacy')
def privacy():
    """隐私政策"""
    return render_template('privacy.html')


@main_bp.route('/community/guide')
def guide():
    """使用指南"""
    return render_template('guide.html')


@main_bp.route('/search')
def search():
    """站内搜索"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'general')  # general, advanced, ai
    category = request.args.get('category', '')
    time_range = request.args.get('time_range', '')
    region = request.args.get('region', '')
    
    results = []
    
    if query:
        if search_type == 'ai':
            # AI搜索（简化版，实际应使用语义搜索）
            results = perform_ai_search(query)
        else:
            # 普通搜索
            results = perform_general_search(query, category, time_range, region)
    
    return render_template('search.html', 
                         query=query,
                         search_type=search_type,
                         results=results)


def perform_general_search(query, category, time_range, region):
    """执行普通搜索"""
    results = []
    query_lower = query.lower()
    
    # 搜索文章
    for article in MOCK_ARTICLES:
        if query_lower in article['title'].lower() or query_lower in article['content'].lower():
            results.append({
                'type': 'article',
                'title': article['title'],
                'content': article['content'][:200] + '...',
                'url': url_for('main.article_detail', id=article['id']),
                'date': article['created_at']
            })
    
    # 搜索工具
    for tool in MOCK_TOOLS:
        if query_lower in tool['name'].lower() or query_lower in tool['description'].lower():
            results.append({
                'type': 'tool',
                'title': tool['name'],
                'content': tool['description'][:200] + '...',
                'url': tool['url'],
                'date': datetime.now()
            })
    
    # 搜索术语
    for term in MOCK_TERMS:
        if query_lower in term['term'].lower() or query_lower in term['definition'].lower():
            results.append({
                'type': 'term',
                'title': term['term'],
                'content': term['definition'][:200] + '...',
                'url': '#',
                'date': datetime.now()
            })
    
    return results


def perform_ai_search(query):
    """执行AI搜索 - 使用阿里云通义千问进行智能搜索"""
    from app.ai_service import ai_search
    
    # 使用AI分析搜索意图并提取关键词
    keywords = ai_search(query)
    
    if keywords:
        # 使用AI提取的关键词进行搜索
        results = []
        for keyword in keywords:
            keyword_results = perform_general_search(keyword, '', '', '')
            results.extend(keyword_results)
        
        # 去重并排序
        seen = set()
        unique_results = []
        for result in results:
            result_key = result['title']
            if result_key not in seen:
                seen.add(result_key)
                unique_results.append(result)
        
        return unique_results[:20]  # 限制返回数量
    else:
        # 如果AI搜索失败，回退到普通搜索
        return perform_general_search(query, '', '', '')


@main_bp.route('/article/<int:id>')
def article_detail(id):
    """文章详情页"""
    article = next((a for a in MOCK_ARTICLES if a['id'] == id), None)
    if not article:
        flash('文章不存在')
        return redirect(url_for('main.index'))
    
    article['views'] += 1
    user = get_user_by_id(article['author_id'])
    if user:
        display_name = user.get('nickname', user['username'])
        article['author'] = {'username': display_name}
    else:
        article['author'] = {'username': '系统'}
    
    # 模拟评论（暂时为空）
    comments = []
    
    return render_template('article_detail.html', article=article, comments=comments)


# 认证蓝图
auth_bp = Blueprint('auth', __name__)

# API蓝图
api_bp = Blueprint('api', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user_data = get_user_by_username(username)
        
        # 使用check_password_hash验证密码
        from werkzeug.security import check_password_hash
        if user_data and check_password_hash(user_data['password'], password):
            user = MockUser(user_data)
            login_user(user, remember=True)
            # 检查是否是首次登录
            first_login = user_data.get('first_login', False)
            return jsonify({
                'success': True, 
                'message': '登录成功',
                'first_login': first_login
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    from app.mock_data import MOCK_USERS
    import random
    import string
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        nickname = data.get('nickname', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password')
        security_question = data.get('security_question', '').strip()
        security_answer = data.get('security_answer', '').strip()
        interests = data.get('interests', [])
        
        # 必填字段验证
        if not username:
            return jsonify({'success': False, 'message': '账号不能为空'})
        if not password:
            return jsonify({'success': False, 'message': '密码不能为空'})
        if not security_question:
            return jsonify({'success': False, 'message': '二级问题不能为空'})
        if not security_answer:
            return jsonify({'success': False, 'message': '问题答案不能为空'})
        
        # 检查用户名是否已存在
        if get_user_by_username(username):
            return jsonify({'success': False, 'message': '账号已存在'})
        
        # 检查邮箱是否已存在（如果提供了邮箱）
        if email:
            for user in MOCK_USERS:
                if user.get('email') == email:
                    return jsonify({'success': False, 'message': '邮箱已被注册'})
        
        # 如果没有提供昵称，随机生成10位英文字符
        if not nickname:
            nickname = ''.join(random.choices(string.ascii_letters, k=10))
        
        # 创建新用户（密码加密）
        from werkzeug.security import generate_password_hash
        new_id = max([u['id'] for u in MOCK_USERS], default=0) + 1
        new_user = {
            'id': new_id,
            'username': username,
            'nickname': nickname,
            'email': email if email else None,
            'password': generate_password_hash(password),
            'role': 'user',
            'avatar': None,
            'security_question': security_question,
            'security_answer': security_answer,
            'interests': interests if interests else [],
            'favorites': {},
            'likes': {},
            'messages': [],
            'first_login': True
        }
        MOCK_USERS.append(new_user)
        
        # 自动登录
        user = MockUser(new_user)
        login_user(user, remember=True)
        
        return jsonify({'success': True, 'message': '注册成功', 'nickname': nickname})
    
    return render_template('register.html')


@api_bp.route('/auth/security-question', methods=['GET'])
def get_security_question_by_username():
    """根据用户名获取二级问题"""
    username = request.args.get('username')
    user_data = get_user_by_username(username)
    if user_data:
        return jsonify({'success': True, 'question': user_data.get('security_question', '')})
    return jsonify({'success': False, 'message': '用户不存在'})


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """忘记密码"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        security_answer = data.get('security_answer')
        new_password = data.get('new_password')
        
        user_data = get_user_by_username(username)
        if not user_data:
            return jsonify({'success': False, 'message': '用户名不存在'})
        
        # 验证二级问题答案
        if user_data.get('security_answer', '').lower() != security_answer.lower():
            return jsonify({'success': False, 'message': '二级问题答案错误'})
        
        # 更新密码（加密存储）
        from werkzeug.security import generate_password_hash
        user_data['password'] = generate_password_hash(new_password)
        
        return jsonify({'success': True, 'message': '密码重置成功，请重新登录'})
    
    return render_template('forgot_password.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出')
    return redirect(url_for('main.index'))


@api_bp.route('/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    """AI聊天接口（AI实验室）- 支持多模型"""
    from app.ai_service import chat_with_model
    
    data = request.get_json()
    message = data.get('message', '')
    model = data.get('model', 'aliyun-qwen-turbo')
    
    if not message:
        return jsonify({
            'success': False,
            'message': '消息不能为空',
            'model': model
        })
    
    # 调用对应模型的API
    response = chat_with_model(message, model)
    return jsonify(response)


@api_bp.route('/forum/post', methods=['POST'])
@login_required
def create_forum_post():
    """创建论坛帖子"""
    data = request.get_json()
    # 模拟创建帖子（实际应该保存到数据库）
    new_id = max([p['id'] for p in MOCK_FORUM_POSTS], default=0) + 1
    return jsonify({'success': True, 'post_id': new_id, 'message': '帖子发布成功（模拟数据，实际应保存到数据库）'})


@api_bp.route('/forum/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """添加评论"""
    data = request.get_json()
    # 模拟添加评论
    return jsonify({'success': True, 'comment_id': 1, 'message': '评论发表成功（模拟数据）'})


# 存储用户的点赞状态（模拟数据）
# 格式：{ user_id: { post_id: bool } }
FORUM_LIKES = {}
ETHICS_LIKES = {}

@api_bp.route('/forum/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """点赞/取消点赞帖子"""
    from app.mock_data import USER_LIKES
    post = next((p for p in MOCK_FORUM_POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({'success': False, 'message': '帖子不存在'})
    
    user_id = current_user.id
    
    # 初始化用户点赞记录
    if user_id not in FORUM_LIKES:
        FORUM_LIKES[user_id] = {}
    if user_id not in USER_LIKES:
        USER_LIKES[user_id] = {'forum': {}}
    if 'forum' not in USER_LIKES[user_id]:
        USER_LIKES[user_id]['forum'] = {}
    
    # 检查当前点赞状态
    is_liked = FORUM_LIKES[user_id].get(post_id, False)
    
    # 切换点赞状态
    if is_liked:
        # 取消点赞
        post['likes'] -= 1
        FORUM_LIKES[user_id][post_id] = False
        USER_LIKES[user_id]['forum'][str(post_id)] = None  # 删除记录
        is_liked = False
    else:
        # 点赞
        post['likes'] += 1
        FORUM_LIKES[user_id][post_id] = True
        USER_LIKES[user_id]['forum'][str(post_id)] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_liked = True
    
    return jsonify({
        'success': True, 
        'likes': post['likes'],
        'is_liked': is_liked
    })


@api_bp.route('/ethics/<int:topic_id>/like', methods=['POST'])
@login_required
def like_ethics_topic(topic_id):
    """点赞/取消点赞伦理专题"""
    from app.mock_data import USER_LIKES
    topic = next((t for t in MOCK_ETHICS_TOPICS if t['id'] == topic_id), None)
    if not topic:
        return jsonify({'success': False, 'message': '专题不存在'})
    
    user_id = current_user.id
    
    # 初始化用户点赞记录
    if user_id not in ETHICS_LIKES:
        ETHICS_LIKES[user_id] = {}
    if user_id not in USER_LIKES:
        USER_LIKES[user_id] = {'ethics': {}}
    if 'ethics' not in USER_LIKES[user_id]:
        USER_LIKES[user_id]['ethics'] = {}
    
    # 检查当前点赞状态
    is_liked = ETHICS_LIKES[user_id].get(topic_id, False)
    
    # 切换点赞状态
    if is_liked:
        # 取消点赞
        topic['likes'] -= 1
        ETHICS_LIKES[user_id][topic_id] = False
        USER_LIKES[user_id]['ethics'][str(topic_id)] = None  # 删除记录
        is_liked = False
    else:
        # 点赞
        topic['likes'] += 1
        ETHICS_LIKES[user_id][topic_id] = True
        USER_LIKES[user_id]['ethics'][str(topic_id)] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_liked = True
    
    return jsonify({
        'success': True, 
        'likes': topic['likes'],
        'is_liked': is_liked
    })


# 收藏功能API
@api_bp.route('/article/<int:article_id>/favorite', methods=['POST'])
@login_required
def favorite_article(article_id):
    """收藏/取消收藏文章"""
    from app.mock_data import USER_FAVORITES
    article = next((a for a in MOCK_ARTICLES if a['id'] == article_id), None)
    if not article:
        return jsonify({'success': False, 'message': '文章不存在'})
    
    user_id = current_user.id
    if user_id not in USER_FAVORITES:
        USER_FAVORITES[user_id] = {}
    if 'article' not in USER_FAVORITES[user_id]:
        USER_FAVORITES[user_id]['article'] = {}
    
    # 切换收藏状态
    is_favorited = article_id in USER_FAVORITES[user_id]['article']
    if is_favorited:
        del USER_FAVORITES[user_id]['article'][article_id]
        is_favorited = False
    else:
        USER_FAVORITES[user_id]['article'][article_id] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_favorited = True
    
    return jsonify({'success': True, 'is_favorited': is_favorited})


@api_bp.route('/forum/<int:post_id>/favorite', methods=['POST'])
@login_required
def favorite_forum_post(post_id):
    """收藏/取消收藏论坛帖子"""
    from app.mock_data import USER_FAVORITES
    post = next((p for p in MOCK_FORUM_POSTS if p['id'] == post_id), None)
    if not post:
        return jsonify({'success': False, 'message': '帖子不存在'})
    
    user_id = current_user.id
    if user_id not in USER_FAVORITES:
        USER_FAVORITES[user_id] = {}
    if 'forum' not in USER_FAVORITES[user_id]:
        USER_FAVORITES[user_id]['forum'] = {}
    
    # 切换收藏状态
    is_favorited = post_id in USER_FAVORITES[user_id]['forum']
    if is_favorited:
        del USER_FAVORITES[user_id]['forum'][post_id]
        is_favorited = False
    else:
        USER_FAVORITES[user_id]['forum'][post_id] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_favorited = True
    
    return jsonify({'success': True, 'is_favorited': is_favorited})


@api_bp.route('/ethics/<int:topic_id>/favorite', methods=['POST'])
@login_required
def favorite_ethics_topic(topic_id):
    """收藏/取消收藏伦理专题"""
    from app.mock_data import USER_FAVORITES
    topic = next((t for t in MOCK_ETHICS_TOPICS if t['id'] == topic_id), None)
    if not topic:
        return jsonify({'success': False, 'message': '专题不存在'})
    
    user_id = current_user.id
    if user_id not in USER_FAVORITES:
        USER_FAVORITES[user_id] = {}
    if 'ethics' not in USER_FAVORITES[user_id]:
        USER_FAVORITES[user_id]['ethics'] = {}
    
    # 切换收藏状态
    is_favorited = topic_id in USER_FAVORITES[user_id]['ethics']
    if is_favorited:
        del USER_FAVORITES[user_id]['ethics'][topic_id]
        is_favorited = False
    else:
        USER_FAVORITES[user_id]['ethics'][topic_id] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_favorited = True
    
    return jsonify({'success': True, 'is_favorited': is_favorited})


@api_bp.route('/ethics/<int:topic_id>/comment', methods=['POST'])
@login_required
def add_ethics_comment(topic_id):
    """添加伦理专题评论"""
    data = request.get_json()
    # 模拟添加评论
    return jsonify({'success': True, 'comment_id': 1, 'message': '评论发表成功（模拟数据）'})


@api_bp.route('/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    from app.ai_service import get_available_models
    models = get_available_models()
    return jsonify({'success': True, 'models': models})


# 个人中心路由
@main_bp.route('/profile')
@login_required
def profile():
    """个人中心"""
    return render_template('profile.html')


# 个人中心API
@api_bp.route('/profile/favorites', methods=['GET'])
@login_required
def get_favorites():
    """获取收藏列表"""
    from app.mock_data import USER_FAVORITES, MOCK_ARTICLES, MOCK_FORUM_POSTS, MOCK_ETHICS_TOPICS
    user_id = current_user.id
    favorites = USER_FAVORITES.get(user_id, {})
    
    result = []
    # 处理文章收藏
    if 'article' in favorites and isinstance(favorites['article'], dict):
        for article_id, timestamp in favorites['article'].items():
            if timestamp:  # 只显示已收藏的
                article = next((a for a in MOCK_ARTICLES if a['id'] == int(article_id)), None)
                if article:
                    result.append({
                        'type': '文章',
                        'title': article['title'],
                        'url': url_for('main.article_detail', id=article['id']),
                        'timestamp': timestamp
                    })
    
    # 处理论坛帖子收藏
    if 'forum' in favorites and isinstance(favorites['forum'], dict):
        for post_id, timestamp in favorites['forum'].items():
            if timestamp:  # 只显示已收藏的
                post = next((p for p in MOCK_FORUM_POSTS if p['id'] == int(post_id)), None)
                if post:
                    result.append({
                        'type': '论坛帖子',
                        'title': post['title'],
                        'url': url_for('main.forum_post', post_id=post['id']),
                        'timestamp': timestamp
                    })
    
    # 处理伦理专题收藏
    if 'ethics' in favorites and isinstance(favorites['ethics'], dict):
        for topic_id, timestamp in favorites['ethics'].items():
            if timestamp:  # 只显示已收藏的
                topic = next((t for t in MOCK_ETHICS_TOPICS if t['id'] == int(topic_id)), None)
                if topic:
                    result.append({
                        'type': '伦理专题',
                        'title': topic['title'],
                        'url': url_for('main.ethics_topic', slug=topic['slug']),
                        'timestamp': timestamp
                    })
    
    # 按时间倒序排列
    result.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({'success': True, 'favorites': result})


@api_bp.route('/profile/likes', methods=['GET'])
@login_required
def get_likes():
    """获取点赞记录"""
    from app.mock_data import USER_LIKES, MOCK_FORUM_POSTS, MOCK_ETHICS_TOPICS
    
    user_id = current_user.id
    likes = USER_LIKES.get(user_id, {})
    
    result = []
    # 论坛帖子点赞
    if 'forum' in likes and isinstance(likes['forum'], dict):
        for post_id, timestamp in likes['forum'].items():
            if timestamp:  # 只显示已点赞的
                post = next((p for p in MOCK_FORUM_POSTS if p['id'] == int(post_id)), None)
                if post:
                    result.append({
                        'type': '论坛帖子',
                        'title': post['title'],
                        'url': url_for('main.forum_post', post_id=post['id']),
                        'timestamp': timestamp
                    })
    
    # 伦理专题点赞
    if 'ethics' in likes and isinstance(likes['ethics'], dict):
        for topic_id, timestamp in likes['ethics'].items():
            if timestamp:  # 只显示已点赞的
                topic = next((t for t in MOCK_ETHICS_TOPICS if t['id'] == int(topic_id)), None)
                if topic:
                    result.append({
                        'type': '伦理专题',
                        'title': topic['title'],
                        'url': url_for('main.ethics_topic', slug=topic['slug']),
                        'timestamp': timestamp
                    })
    
    # 按时间倒序排列
    result.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({'success': True, 'likes': result})


@api_bp.route('/profile/messages', methods=['GET'])
@login_required
def get_messages():
    """获取消息列表"""
    from app.mock_data import USER_MESSAGES
    user_id = current_user.id
    messages = USER_MESSAGES.get(user_id, [])
    # 按时间倒序排列
    messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify({'success': True, 'messages': messages})


@api_bp.route('/profile/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    """标记消息为已读"""
    from app.mock_data import USER_MESSAGES
    user_id = current_user.id
    messages = USER_MESSAGES.get(user_id, [])
    for msg in messages:
        if msg.get('id') == message_id:
            msg['read'] = True
            break
    return jsonify({'success': True})


@api_bp.route('/auth/check-first-login', methods=['GET'])
@login_required
def check_first_login():
    """检查是否首次登录"""
    from app.mock_data import get_user_by_id
    user_data = get_user_by_id(current_user.id)
    if user_data:
        return jsonify({'success': True, 'first_login': user_data.get('first_login', False)})
    return jsonify({'success': False})


@api_bp.route('/profile/interests', methods=['POST'])
@login_required
def update_interests():
    """更新用户兴趣"""
    from app.mock_data import get_user_by_id
    data = request.get_json()
    interests = data.get('interests', [])
    
    user_data = get_user_by_id(current_user.id)
    if user_data:
        user_data['interests'] = interests
        user_data['first_login'] = False  # 标记已设置兴趣
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': '用户不存在'})


@api_bp.route('/profile/security-question', methods=['GET'])
@login_required
def get_security_question():
    """获取二级问题"""
    from app.mock_data import get_user_by_id
    user_data = get_user_by_id(current_user.id)
    if user_data:
        return jsonify({'success': True, 'question': user_data.get('security_question', '')})
    return jsonify({'success': False, 'message': '用户不存在'})


@api_bp.route('/profile/password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    from app.mock_data import get_user_by_id, MOCK_USERS
    data = request.get_json()
    security_answer = data.get('security_answer', '')
    new_password = data.get('new_password', '')
    
    user_data = get_user_by_id(current_user.id)
    if not user_data:
        return jsonify({'success': False, 'message': '用户不存在'})
    
    # 验证二级问题答案
    if user_data.get('security_answer', '').lower() != security_answer.lower():
        return jsonify({'success': False, 'message': '二级问题答案错误'})
    
        # 更新密码（加密存储）
        from werkzeug.security import generate_password_hash
        user_data['password'] = generate_password_hash(new_password)
        # 强制退出（不提醒用户）
    from flask_login import logout_user
    logout_user()
    
    return jsonify({'success': True, 'message': '密码修改成功，请重新登录'})


@api_bp.route('/profile/security', methods=['POST'])
@login_required
def change_security():
    """修改二级密码"""
    from app.mock_data import get_user_by_id
    data = request.get_json()
    current_answer = data.get('current_answer', '')
    new_question = data.get('new_question', '')
    new_answer = data.get('new_answer', '')
    
    user_data = get_user_by_id(current_user.id)
    if not user_data:
        return jsonify({'success': False, 'message': '用户不存在'})
    
    # 验证当前二级问题答案
    if user_data.get('security_answer', '').lower() != current_answer.lower():
        return jsonify({'success': False, 'message': '当前二级问题答案错误'})
    
    # 更新二级问题
    user_data['security_question'] = new_question
    user_data['security_answer'] = new_answer
    
    return jsonify({'success': True, 'message': '二级密码修改成功'})


@api_bp.route('/profile/username', methods=['POST'])
@login_required
def update_username():
    """更新昵称"""
    from app.mock_data import get_user_by_id, get_user_by_username
    data = request.get_json()
    new_username = data.get('username', '').strip()
    
    if not new_username:
        return jsonify({'success': False, 'message': '昵称不能为空'})
    
    # 检查用户名是否已存在
    existing_user = get_user_by_username(new_username)
    if existing_user and existing_user['id'] != current_user.id:
        return jsonify({'success': False, 'message': '用户名已存在'})
    
    user_data = get_user_by_id(current_user.id)
    if user_data:
        user_data['username'] = new_username
        return jsonify({'success': True, 'message': '昵称更新成功'})
    
    return jsonify({'success': False, 'message': '用户不存在'})


@api_bp.route('/profile/avatar', methods=['POST'])
@login_required
def upload_avatar():
    """上传头像"""
    from werkzeug.utils import secure_filename
    import os
    from app.mock_data import get_user_by_id
    
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'message': '没有上传文件'})
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'})
    
    # 检查文件类型
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'success': False, 'message': '只支持图片格式'})
    
    # 保存文件
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = secure_filename(f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    # 更新用户头像
    user_data = get_user_by_id(current_user.id)
    if user_data:
        # 使用相对路径，前端会通过url_for处理
        avatar_path = f'uploads/avatars/{filename}'
        user_data['avatar'] = avatar_path
        # 返回完整URL路径
        from flask import url_for
        avatar_url = url_for('static', filename=avatar_path)
        return jsonify({'success': True, 'avatar_url': avatar_url})
    
    return jsonify({'success': False, 'message': '用户不存在'})


@api_bp.route('/ai-assistant', methods=['POST'])
@login_required
def ai_assistant_api():
    """AI助教接口 - 支持多模型RAG问答"""
    from app.ai_service import chat_with_model
    from config import Config
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({
            'success': False,
            'message': '问题不能为空'
        })
    
    # 构建RAG提示词（可以结合站内知识库）
    rag_prompt = f"""你是一个专业的AI学习助手，专门回答关于人工智能的问题。

用户问题：{question}

请基于你的知识，为用户提供准确、详细的回答。如果涉及具体的技术概念，请给出清晰的解释和示例。
回答要专业但易懂，适合不同背景的学习者。"""
    
    # 优先使用阿里云，如果没有配置则尝试其他模型
    model = 'aliyun-qwen-turbo'
    if not Config.DASHSCOPE_API_KEY:
        # 按优先级尝试其他模型
        if Config.DEEPSEEK_API_KEY:
            model = 'deepseek-chat'
        elif Config.KIMI_API_KEY:
            model = 'kimi-moonshot-v1-8k'
        elif Config.GEMINI_API_KEY:
            model = 'gemini-1.5-flash'  # 优先使用免费版本
        elif Config.OPENAI_API_KEY:
            model = 'openai-gpt-3.5-turbo'
    
    # 调用API
    response = chat_with_model(rag_prompt, model)
    
    if response['success']:
        # 模拟来源信息（实际应该从知识库检索）
        sources = ['AI基础 > 核心概念', '资源中心 > 推荐阅读']
        
        return jsonify({
            'success': True,
            'answer': response['message'],
            'sources': sources
        })
    else:
        return jsonify({
            'success': False,
            'message': response['message']
        })

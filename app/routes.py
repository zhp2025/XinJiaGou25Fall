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
    popular_models = sorted(popular_models, key=lambda x: x['rating'], reverse=True)[:4]
    
    # 获取热门帖子（用于社区排行榜）
    hot_posts = sorted(MOCK_FORUM_POSTS, key=lambda x: (x['likes'], x['views']), reverse=True)[:5]
    # 为帖子添加作者信息
    for post in hot_posts:
        user = get_user_by_id(post['user_id'])
        if user:
            display_name = user.get('nickname', user['username'])
            post['author'] = {'username': display_name}
        else:
            post['author'] = {'username': '未知用户'}
        post['comments_count'] = post.get('comments_count', 0)
    
    return render_template('index.html', 
                         popular_articles=popular_articles,
                         latest_news=latest_news,
                         popular_models=popular_models,
                         hot_posts=hot_posts)


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
    # 获取搜索关键词
    search_query = request.args.get('q', '').strip()
    
    # 获取所有帖子
    all_posts = MOCK_FORUM_POSTS.copy()
    
    # 如果有搜索关键词，进行过滤
    if search_query:
        search_query_lower = search_query.lower()
        filtered_posts = []
        for post in all_posts:
            # 搜索标题和内容
            title_match = search_query_lower in post.get('title', '').lower()
            content_match = search_query_lower in post.get('content', '').lower()
            if title_match or content_match:
                filtered_posts.append(post)
        all_posts = filtered_posts
    
    # 排序：如果有搜索，按相关性（匹配度）排序；否则按热门度排序
    if search_query:
        # 搜索时按匹配度排序（标题匹配优先）
        def sort_key(post):
            title_match = search_query_lower in post.get('title', '').lower()
            return (not title_match, -post.get('likes', 0), -post.get('views', 0))
        hot_posts = sorted(all_posts, key=sort_key)[:20]
    else:
        # 默认按热门度排序
        hot_posts = sorted(all_posts, key=lambda x: (x['likes'], x['views']), reverse=True)[:10]
    
    # 为帖子添加作者信息
    for post in hot_posts:
        user = get_user_by_id(post['user_id'])
        if user:
            display_name = user.get('nickname', user['username'])
            post['author'] = {'username': display_name}
        else:
            post['author'] = {'username': '未知用户'}
        post['comments_count'] = post.get('comments_count', 0)
    
    return render_template('community.html', hot_posts=hot_posts, search_query=search_query)


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


@api_bp.route('/playground/<tool_type>', methods=['POST'])
@login_required
def playground_tool(tool_type):
    """AI游乐场工具接口 - 每个工具使用专门的agent"""
    from app.ai_service import chat_with_model
    from config import Config
    
    data = request.get_json()
    user_input = data.get('input', '')
    model = data.get('model', 'aliyun-qwen-turbo')
    conversation = data.get('conversation', [])  # 对话历史（仅编程工具使用）
    
    if not user_input:
        return jsonify({
            'success': False,
            'message': '输入内容不能为空'
        })
    
    # 为每个工具定义专门的agent提示词
    agent_prompts = {
        'image-gen': """你是一个专业的AI图像生成助手。用户会描述他们想要生成的图像，你需要：
1. 理解用户的描述
2. 优化和扩展描述，使其更适合图像生成
3. 提供详细的图像生成提示词（prompt）

注意：你只负责生成提示词，不直接生成图像。请用中文回复。""",
        'writing': """你是一个专业的AI写作助手。你的任务是帮助用户进行各种写作工作，包括：
- 文章写作
- 文案创作
- 内容优化
- 创意写作

请根据用户的需求，提供高质量的写作内容。用中文回复。""",
        'translation': """你是一个专业的AI翻译助手。你的任务是：
1. 准确翻译用户提供的文本
2. 保持原文的语气和风格
3. 提供多种翻译选项（如果适用）

请用中文回复。""",
        'programming': """你是一个专业的AI编程助手。你的任务是：
1. 帮助用户编写代码
2. 调试和优化代码
3. 解释代码逻辑
4. 提供编程建议

请用中文回复，代码部分使用代码块格式（```语言名\n代码\n```）。如果用户的问题涉及代码，请提供完整的、可运行的代码。""",
        'research': """你是一个专业的AI研究助手。你的任务是：
1. 深入分析用户提出的问题
2. 提供全面的研究视角
3. 引用相关理论和实践
4. 提供多角度的思考

请用中文回复，内容要专业、深入、全面。""",
        'ppt': """你是一个专业的PPT制作助手。你的任务是：
1. 根据用户的需求，生成PPT的大纲和内容
2. 为每个幻灯片提供标题和要点
3. 提供结构化的内容，方便制作PPT
4. 使用Markdown格式输出，便于后续处理

输出格式：
# 幻灯片1标题
- 要点1
- 要点2

# 幻灯片2标题
- 要点1
- 要点2

请用中文回复。"""
    }
    
    # 获取对应工具的agent提示词
    system_prompt = agent_prompts.get(tool_type, '你是一个专业的AI助手。请用中文回复。')
    
    # 如果是编程工具且有对话历史，构建多轮对话
    if tool_type == 'programming' and conversation:
        # 构建对话消息列表
        messages = [{'role': 'system', 'content': system_prompt}]
        # 添加历史对话
        for msg in conversation:
            messages.append({'role': msg['role'], 'content': msg['content']})
        # 添加当前用户输入
        messages.append({'role': 'user', 'content': user_input})
        
        # 调用支持多轮对话的API
        response = chat_with_model_multi_turn(messages, model)
    else:
        # 单轮对话
        full_message = f"{system_prompt}\n\n用户需求：{user_input}"
        response = chat_with_model(full_message, model)
    
    if response['success']:
        result = {
            'success': True,
            'output': response['message'],
            'model': response.get('model', model)
        }
        
        # 如果是PPT制作，标记为PPT格式
        if tool_type == 'ppt':
            result['type'] = 'ppt'
        
        # 如果是编程工具，识别代码语言
        if tool_type == 'programming':
            language = detect_code_language(response['message'])
            result['language'] = language
        
        return jsonify(result)
    else:
        return jsonify({
            'success': False,
            'message': response['message']
        })


def detect_code_language(text):
    """检测代码语言类型"""
    import re
    
    # 检查代码块中的语言标识
    code_block_pattern = r'```(\w+)?\n'
    matches = re.findall(code_block_pattern, text)
    if matches:
        lang = matches[0].lower() if matches[0] else ''
        if lang:
            return lang
    
    # 检查代码块结束标记前的语言
    code_block_pattern2 = r'```(\w+)?\s*\n'
    match = re.search(code_block_pattern2, text)
    if match and match.group(1):
        return match.group(1).lower()
    
    # 根据关键词和代码特征判断
    text_lower = text.lower()
    
    # Python特征
    if any(keyword in text for keyword in ['def ', 'import ', 'from ', 'print(', '__init__', 'if __name__']):
        return 'python'
    # JavaScript特征
    elif any(keyword in text for keyword in ['function ', 'const ', 'let ', 'var ', '=>', 'console.log']):
        return 'javascript'
    # Java特征
    elif 'public class' in text or 'public static void main' in text:
        return 'java'
    # C/C++特征
    elif '#include' in text or 'using namespace' in text:
        return 'cpp'
    # HTML特征
    elif '<html' in text_lower or '<div' in text_lower or '<body' in text_lower:
        return 'html'
    # CSS特征
    elif re.search(r'\{[^}]*:[^}]*\}', text) and ('color:' in text_lower or 'margin:' in text_lower):
        return 'css'
    # SQL特征
    elif any(keyword in text_lower for keyword in ['select ', 'from ', 'where ', 'insert into', 'create table']):
        return 'sql'
    # TypeScript特征
    elif 'interface ' in text or 'type ' in text or ': string' in text or ': number' in text:
        return 'typescript'
    # Go特征
    elif 'package ' in text or 'func ' in text or 'import (' in text:
        return 'go'
    # Rust特征
    elif 'fn ' in text and 'let ' in text:
        return 'rust'
    
    return 'txt'


def chat_with_model_multi_turn(messages, model='aliyun-qwen-turbo'):
    """支持多轮对话的模型调用"""
    from app.ai_service import chat_with_model
    
    # 将对话历史转换为上下文文本
    # 保留最近的对话历史（最多10轮）
    recent_messages = messages[-10:] if len(messages) > 10 else messages
    
    conversation_text = ""
    for msg in recent_messages[1:]:  # 跳过system消息
        role = "用户" if msg['role'] == 'user' else "助手"
        conversation_text += f"{role}：{msg['content']}\n\n"
    
    # 构建包含上下文的完整消息
    system_prompt = recent_messages[0]['content'] if recent_messages else "你是一个专业的AI助手。"
    full_message = f"{system_prompt}\n\n以下是对话历史：\n{conversation_text}\n请根据对话历史回答用户的最新问题。"
    
    return chat_with_model(full_message, model)




@api_bp.route('/playground/code/download', methods=['POST'])
@login_required
def download_code():
    """下载代码文件"""
    from flask import send_file
    from io import BytesIO
    
    data = request.get_json()
    code_content = data.get('code', '')
    extension = data.get('extension', 'txt')
    
    if not code_content:
        return jsonify({
            'success': False,
            'message': '代码内容不能为空'
        })
    
    try:
        # 提取代码块中的代码（如果有代码块标记）
        import re
        
        # 尝试提取代码块
        code_block_pattern = r'```(?:\w+)?\s*\n(.*?)```'
        matches = re.findall(code_block_pattern, code_content, re.DOTALL)
        if matches:
            # 使用第一个代码块
            code_content = matches[0].strip()
        else:
            # 如果没有代码块标记，尝试提取可能的代码部分
            # 查找包含代码特征的行
            lines = code_content.split('\n')
            code_lines = []
            in_code = False
            for line in lines:
                # 检测代码特征
                if any(keyword in line for keyword in ['def ', 'function', 'class ', 'import ', 'const ', 'let ', 'var ', 'public ', 'private ']):
                    in_code = True
                if in_code:
                    code_lines.append(line)
                # 如果遇到空行且已有代码，可能代码结束
                if in_code and not line.strip() and len(code_lines) > 5:
                    break
            
            if code_lines:
                code_content = '\n'.join(code_lines).strip()
        
        # 创建文件
        code_io = BytesIO()
        code_io.write(code_content.encode('utf-8'))
        code_io.seek(0)
        
        # 确定MIME类型
        mime_types = {
            'py': 'text/x-python',
            'js': 'text/javascript',
            'ts': 'text/typescript',
            'java': 'text/x-java-source',
            'cpp': 'text/x-c++',
            'c': 'text/x-c',
            'html': 'text/html',
            'css': 'text/css',
            'sql': 'text/x-sql',
            'sh': 'text/x-shellscript',
            'json': 'application/json',
            'xml': 'application/xml',
            'yml': 'text/yaml',
            'md': 'text/markdown',
            'txt': 'text/plain'
        }
        
        mime_type = mime_types.get(extension, 'text/plain')
        
        return send_file(
            code_io,
            mimetype=mime_type,
            as_attachment=True,
            download_name=f'code.{extension}'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成代码文件失败: {str(e)}'
        })


@api_bp.route('/playground/ppt/download', methods=['POST'])
@login_required
def download_ppt():
    """生成并下载PPT文件"""
    from pptx import Presentation
    from io import BytesIO
    from flask import send_file
    import os
    
    data = request.get_json()
    ppt_content = data.get('content', '')
    
    if not ppt_content:
        return jsonify({
            'success': False,
            'message': 'PPT内容不能为空'
        })
    
    try:
        # 创建新的PPT，不使用模板
        prs = Presentation()
        
        # 解析Markdown格式的内容，自动检测和调整页面
        slides_data = []
        slides = ppt_content.split('#')
        
        for slide_content in slides:
            slide_content = slide_content.strip()
            if not slide_content:
                continue
            
            lines = slide_content.split('\n')
            title = lines[0].strip()
            if not title:
                continue
            
            # 清理标题：移除"幻灯片X："这样的前缀
            import re
            title = re.sub(r'^幻灯片\d+[：:]\s*', '', title)
            title = re.sub(r'^Slide\s+\d+[：:]\s*', '', title, flags=re.IGNORECASE)
            
            # 提取要点
            bullet_points = []
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    bullet_points.append(line.lstrip('-•*').strip())
                elif line:
                    bullet_points.append(line)
            
            # 自动检测内容是否适合单页，如果内容过多则自动分页
            MAX_POINTS_PER_SLIDE = 6  # 每页最多6个要点
            MAX_TITLE_LENGTH = 50  # 标题最大长度
            MAX_POINT_LENGTH = 100  # 每个要点最大长度
            
            # 如果标题过长，截断
            if len(title) > MAX_TITLE_LENGTH:
                title = title[:MAX_TITLE_LENGTH] + '...'
            
            # 如果要点过多或单个要点过长，需要分页
            if len(bullet_points) > MAX_POINTS_PER_SLIDE:
                # 分页处理
                total_pages = (len(bullet_points) + MAX_POINTS_PER_SLIDE - 1) // MAX_POINTS_PER_SLIDE
                for i in range(0, len(bullet_points), MAX_POINTS_PER_SLIDE):
                    page_points = bullet_points[i:i + MAX_POINTS_PER_SLIDE]
                    # 截断过长的要点
                    page_points = [p[:MAX_POINT_LENGTH] + '...' if len(p) > MAX_POINT_LENGTH else p for p in page_points]
                    
                    page_title = title
                    if total_pages > 1:
                        page_title = f"{title}（{i//MAX_POINTS_PER_SLIDE + 1}/{total_pages}）"
                    
                    slides_data.append({
                        'title': page_title,
                        'points': page_points
                    })
            else:
                # 单页内容，截断过长的要点
                bullet_points = [p[:MAX_POINT_LENGTH] + '...' if len(p) > MAX_POINT_LENGTH else p for p in bullet_points]
                
                slides_data.append({
                    'title': title,
                    'points': bullet_points
                })
        
        # 如果没有幻灯片，创建一个默认的
        if not slides_data:
            slides_data.append({
                'title': 'PPT内容',
                'points': []
            })
        
        # 创建幻灯片并添加内容
        for i, slide_data in enumerate(slides_data):
            # 选择合适的布局
            # 0: 标题幻灯片, 1: 标题和内容, 5: 仅标题
            if i == 0 and len(slides_data) > 1:
                # 第一张幻灯片使用标题幻灯片（布局0）
                layout_index = 0
            else:
                # 其他幻灯片使用标题和内容布局（布局1）
                layout_index = 1
            
            # 确保布局索引有效
            if layout_index >= len(prs.slide_layouts):
                layout_index = 0
            
            # 创建幻灯片
            try:
                slide = prs.slides.add_slide(prs.slide_layouts[layout_index])
            except:
                # 如果布局不存在，使用第一个可用布局
                slide = prs.slides.add_slide(prs.slide_layouts[0])
            
            # 填充标题
            title_added = False
            try:
                # 尝试使用标题占位符
                if hasattr(slide, 'shapes') and slide.shapes.title:
                    title_shape = slide.shapes.title
                    if title_shape.has_text_frame:
                        title_shape.text = slide_data['title']
                        title_added = True
            except:
                pass
            
            # 如果没有标题占位符，尝试查找其他文本框
            if not title_added:
                for shape in slide.shapes:
                    if hasattr(shape, 'text_frame') and shape.text_frame:
                        try:
                            # 检查是否是标题位置（通常在顶部）
                            if shape.top < slide.height * 0.2:  # 在顶部20%区域内
                                shape.text_frame.text = slide_data['title']
                                title_added = True
                                break
                        except:
                            pass
            
            # 填充内容
            if slide_data['points']:
                content_added = False
                
                # 方法1: 尝试使用内容占位符（索引1）
                try:
                    if len(slide.placeholders) > 1:
                        content_placeholder = slide.placeholders[1]
                        if content_placeholder != slide.shapes.title and hasattr(content_placeholder, 'text_frame'):
                            text_frame = content_placeholder.text_frame
                            text_frame.clear()
                            
                            # 设置第一个段落
                            if len(text_frame.paragraphs) > 0:
                                p = text_frame.paragraphs[0]
                            else:
                                p = text_frame.add_paragraph()
                            
                            p.text = slide_data['points'][0]
                            p.level = 0
                            
                            # 添加其他要点
                            for point in slide_data['points'][1:]:
                                p = text_frame.add_paragraph()
                                p.text = point
                                p.level = 0
                            
                            content_added = True
                except:
                    pass
                
                # 方法2: 如果没有找到占位符，查找内容区域的文本框
                if not content_added:
                    for shape in slide.shapes:
                        if shape != slide.shapes.title and hasattr(shape, 'text_frame'):
                            text_frame = shape.text_frame
                            if text_frame:
                                try:
                                    # 检查是否是内容位置（不在顶部）
                                    if shape.top > slide.height * 0.15:  # 在顶部15%以下
                                        text_frame.clear()
                                        
                                        # 设置第一个段落
                                        if len(text_frame.paragraphs) > 0:
                                            p = text_frame.paragraphs[0]
                                        else:
                                            p = text_frame.add_paragraph()
                                        
                                        p.text = slide_data['points'][0]
                                        p.level = 0
                                        
                                        # 添加其他要点
                                        for point in slide_data['points'][1:]:
                                            p = text_frame.add_paragraph()
                                            p.text = point
                                            p.level = 0
                                        
                                        content_added = True
                                        break
                                except:
                                    pass
        
        # 保存到内存
        ppt_io = BytesIO()
        prs.save(ppt_io)
        ppt_io.seek(0)
        
        return send_file(
            ppt_io,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name='presentation.pptx'
        )
    except ImportError:
        return jsonify({
            'success': False,
            'message': 'PPT生成功能需要安装python-pptx库，请运行: pip install python-pptx'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成PPT失败: {str(e)}'
        })

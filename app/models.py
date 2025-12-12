from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(255))
    
    # 关系
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    forum_posts = db.relationship('ForumPost', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Article(db.Model):
    """文章模型"""
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # 热门科普, 最新资讯, 核心概念等
    cover_image = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)  # 是否精选
    
    def __repr__(self):
        return f'<Article {self.title}>'


class Tool(db.Model):
    """AI工具模型"""
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    category = db.Column(db.String(50))  # 图像生成, 写作, 翻译, 编程等
    icon = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tool {self.name}>'


class Case(db.Model):
    """应用案例模型"""
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(50))  # AI+医疗, AI+教育, AI+科研等
    image = db.Column(db.String(255))
    external_link = db.Column(db.String(255))
    tags = db.Column(db.String(200))  # 逗号分隔的标签
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Case {self.title}>'


class ForumPost(db.Model):
    """论坛帖子模型"""
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50))  # 问答, 讨论等
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ForumPost {self.title}>'


class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    ethics_topic_id = db.Column(db.Integer, db.ForeignKey('ethics_topics.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class Term(db.Model):
    """AI术语模型"""
    __tablename__ = 'terms'
    
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False, index=True)
    definition = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # LLM, Transformer, 扩散模型等
    related_terms = db.Column(db.String(200))  # 相关术语ID，逗号分隔
    examples = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Term {self.term}>'


class Resource(db.Model):
    """推荐阅读资源模型"""
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    type = db.Column(db.String(50))  # 书籍, 论文, 期刊, 课程
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource {self.title}>'


class EthicsTopic(db.Model):
    """伦理与未来专题模型"""
    __tablename__ = 'ethics_topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, index=True)  # ai-safety, ai-bias等
    description = db.Column(db.Text)
    background = db.Column(db.Text)  # 背景介绍
    key_issues = db.Column(db.Text)  # 关键问题
    expert_views = db.Column(db.Text)  # 专家观点摘要
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    comments = db.relationship('Comment', backref='ethics_topic', lazy='dynamic')
    
    def __repr__(self):
        return f'<EthicsTopic {self.title}>'


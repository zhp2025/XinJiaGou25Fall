from flask import Flask
from flask_login import LoginManager
from config import Config

# 暂时不使用数据库，使用 session 进行用户管理
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'

class MockUser:
    """模拟用户类，用于 Flask-Login"""
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data.get('role', 'user')
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    from app.mock_data import get_user_by_id
    user_data = get_user_by_id(int(user_id))
    if user_data:
        return MockUser(user_data)
    return None

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化登录管理器
    login_manager.init_app(app)
    
    # 添加模板过滤器，安全访问字典
    @app.template_filter('get')
    def dict_get(value, key, default=None):
        """安全获取字典值"""
        if isinstance(value, dict):
            return value.get(key, default)
        return getattr(value, key, default)
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 添加静态文件路由（用于 logo）
    @app.route('/AICove.jpg')
    def serve_logo():
        from flask import send_from_directory, abort
        import os
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'AICove.jpg')
        if os.path.exists(logo_path):
            return send_from_directory(os.path.dirname(logo_path), 'AICove.jpg')
        else:
            # 如果 logo 不存在，返回 404（前端会通过 onerror 隐藏）
            abort(404)
    
    # 添加错误处理
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('500.html'), 500
    
    return app


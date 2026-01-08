from flask import Flask
from flask_login import LoginManager
from config import Config
from datetime import date

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'

class MockUser:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.nickname = user_data.get('nickname', user_data['username'])
        self.email = user_data.get('email')
        self.role = user_data.get('role', 'user')
        self.avatar = user_data.get('avatar')
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

def record_visit(user_id):
    """记录访问统计"""
    if user_id:
        from app.mock_data import MOCK_VISIT_STATS
        today_str = str(date.today())
        MOCK_VISIT_STATS[today_str] = MOCK_VISIT_STATS.get(today_str, 0) + 1

@login_manager.user_loader
def load_user(user_id):
    from app.mock_data import get_user_by_id
    user_data = get_user_by_id(int(user_id))
    if user_data:
        return MockUser(user_data)
    return None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login_manager.init_app(app)
    
    @app.template_filter('get')
    def dict_get(value, key, default=None):
        if isinstance(value, dict):
            return value.get(key, default)
        return getattr(value, key, default)
    
    from app.routes import main_bp, auth_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/AICove.jpg')
    def serve_logo():
        from flask import send_from_directory, abort
        import os
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'AICove.jpg')
        if os.path.exists(logo_path):
            return send_from_directory(os.path.dirname(logo_path), 'AICove.jpg')
        abort(404)
    
    @app.route('/default.jpg')
    def serve_default_avatar():
        from flask import send_from_directory, abort
        import os
        avatar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'default.jpg')
        if os.path.exists(avatar_path):
            return send_from_directory(os.path.dirname(avatar_path), 'default.jpg')
        abort(404)
    
    @app.route('/backgroud/bottom.jpg')
    def serve_bottom_background():
        from flask import send_from_directory, abort
        import os
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backgroud', 'bottom.jpg')
        if os.path.exists(bg_path):
            return send_from_directory(os.path.dirname(bg_path), 'bottom.jpg')
        abort(404)
    
    @app.route('/AIGCimages/<filename>')
    def serve_aigc_image(filename):
        from flask import send_from_directory, abort
        import os
        images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'AIGCimages')
        file_path = os.path.join(images_dir, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(images_dir, filename)
        abort(404)
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('500.html'), 500
    
    return app


# 在 app/__init__.py 中
def create_app():
    app = Flask(__name__)
    # ...其他配置代码...
    
    # 注册蓝图
    from app.blueprints.groups import groups_bp
    app.register_blueprint(groups_bp, url_prefix='/groups')
    
    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.practice import practice_bp
    app.register_blueprint(practice_bp, url_prefix='/practice')
    
    return app
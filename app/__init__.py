from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.main import main_bp
    from app.blueprints.groups import groups_bp
    from app.blueprints.practice import practice_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(practice_bp, url_prefix='/practice')

    return app
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions 
    db.init_app(app)

    # Register Blueprints
    from app.routes.main import main as main_blueprint
    from app.routes.chat_routes import chat_bp
    # from app.routes.auth import auth as auth_blueprint
    # from app.routes.student import student as student_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(chat_bp)
    # app.register_blueprint(auth_blueprint, url_prefix="/auth")
    # app.register_blueprint(student_blueprint, url_prefix="/student")

    return app
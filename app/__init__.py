from flask import Flask
from .database import engine, metadata


def create_app() -> Flask:
    app = Flask(__name__)
    
    from .blog import blog
    app.register_blueprint(blog)
    
    return app

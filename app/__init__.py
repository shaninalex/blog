from oauthlib.oauth2 import WebApplicationClient
from flask import Flask,render_template
from flask_login import LoginManager

from .database import init_db
from .userbp.user import User
from .userbp import GOOGLE_CLIENT_ID


def create_app() -> Flask:
    app = Flask(__name__)
    init_db()
    
    # app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    app.secret_key = "SECRET_KEY"

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.config["client"] = WebApplicationClient(GOOGLE_CLIENT_ID)
    # Flask-Login helper to retrieve a user from our db

    @login_manager.user_loader
    def load_user(email):
        return User.get(email)  

    # Blueprints
    from .userbp import userbp
    app.register_blueprint(userbp)

    from .blog import blog
    app.register_blueprint(blog)
    
    from .static_pages import static_pages
    app.register_blueprint(static_pages)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def error(e):
        return render_template("500.html")

    return app

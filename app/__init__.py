from flask import Flask,render_template
from .database import engine, metadata


def create_app() -> Flask:
    app = Flask(__name__)
    metadata.create_all(bind=engine)
    
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

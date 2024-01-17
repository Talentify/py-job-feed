from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import and register blueprints
    from feed_downloader.routes.main_routes import main_bp
    from feed_downloader.routes.feed_routes import feed_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(feed_bp, url_prefix='/feed')

    return app

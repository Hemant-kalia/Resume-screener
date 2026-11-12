from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.resume_routes import resume_bp
    app.register_blueprint(resume_bp)

    return app
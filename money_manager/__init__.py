import os
from flask import Flask
from .helpers import ARS, datetimeformat

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.environ.get("DATABASE_URL"),
        TEMPLATES_AUTO_RELOAD = True
    )

    if test_config == None:
        app.config.from_pyfile("config.py", silent = True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    from money_manager import db
    db.init_app(app)

    from money_manager import auth, mm
    app.register_blueprint(auth.bp)
    app.register_blueprint(mm.bp)
    app.add_url_rule('/', endpoint='index')

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    app.jinja_env.filters["ARS"] = ARS
    app.jinja_env.filters["datetimeformat"] = datetimeformat

    return app


import os

from flask import Flask


def create_app(test_config=None):
    """A simple flask application factory."""
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "joke_share.db")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from joke_share import db
    db.init_app(app)
    
    from joke_share.auth import bp as abp
    app.register_blueprint(abp)

    from joke_share.jokes import bp as jbp
    app.register_blueprint(jbp)
    
    @app.route("/dummy")
    def dummy():
        return "<h1 style='text-align: center; color: green'>Working</h1>"
    @app.route("/api")
    def api():
        return {
            "key1": 100,
            "key2": "Worked"
        }
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

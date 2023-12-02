import os

from flask import Flask
from flask import request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route("/")
    def hello_world():
        return "<h1>Hello, World!</h1>"

    @app.route("/oil_price", methods=['GET', 'POST', 'PUT', 'DELETE'])
    def oil_price():
        return "<h1>Oil Price</h1>"


    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route("/name", methods=['GET', 'POST'])
    def get_name():
        if request.method == 'POST':
            return "<p>Yiyun Lei from POST</p>"
        else:
            return "<p>Yiyun Lei from GET</p>"

    @app.route("/hometown", methods=['GET', 'POST'])
    def get_hometown():
        if request.method == 'GET':
            name = request.args.get('name')
            if name == 'yiyunlei':
                return dict(name="yiyunlei", hometown="China")
            else:
                return dict(name="unknown", hometown="unknown")
        elif request.method == 'POST':
            name = request.json.get('name')
            if name == 'yiyunlei':
                return dict(name="yiyunlei", hometown="China")
            else:
                return dict(name="unknown", hometown="unknown")

    return app
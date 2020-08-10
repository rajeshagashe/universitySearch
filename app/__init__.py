import os
import importlib

from flask import Flask
from flask_migrate import Migrate

from app.extensions import postgres_db
from app.views import blueprints


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load global environments, when not testing
        app.config.from_pyfile("../.env")
        #connect db
        postgres_db.init_app(app)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        try:
            # create folder for sqlite
            os.makedirs(app.instance_path)
        except OSError:
            pass
    
    for path, blueprint, url_prefix in blueprints:
        module = importlib.import_module(path)
        app.register_blueprint(getattr(module, blueprint), url_prefix=url_prefix)       
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

# migrations -->
# flask db init
# flask db migrate
# flask db upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate#, MigrateCommand
from app.models.universities import UniversityInfo 

app = create_app()
migrate = Migrate(app, postgres_db)


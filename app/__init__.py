import os

from flask import Flask
from app.extensions import postgres_db
from flask_migrate import Migrate

migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("../.env")
        postgres_db.init_app(app)
        migrate.init_app(app, postgres_db)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = create_app()
migrate = Migrate(app, postgres_db)
from app.models.universities import UniversityInfo 


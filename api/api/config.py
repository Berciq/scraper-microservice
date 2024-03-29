from os.path import abspath, dirname, join

import connexion
from flask_sqlalchemy import SQLAlchemy

from api.env import configmodule
from api.utils import FileSystemImageStore

basedir = abspath(dirname(dirname(__file__)))

# Create the connexion application instance
# TODO: Configure docExpansion to list
options = {
    'swagger_url': '/',
    'swagger_ui_config': {'docExpansion': 'full'}
}
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir, options=options)

# Get the underlying Flask app instance
app = connex_app.app

app.config.from_object(configmodule)

db = SQLAlchemy(app)

storage = FileSystemImageStore(app.config['IMAGES_STORE'])

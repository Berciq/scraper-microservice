from os.path import abspath, dirname, join
import connexion
from flask_sqlalchemy import SQLAlchemy

basedir = abspath(dirname(dirname(__file__)))

# Create the connexion application instance
# TODO: Configure docExpansion to list
options = {
    'swagger_url': '/',
    'swagger_ui_config': {'docExpansion': 'full'}
}
connex_app = connexion.FlaskApp(__name__, specification_dir='.', options=options)

# Get the underlying Flask app instance
app = connex_app.app

# Use Sqlite as a temporary solution
SQLITE_URL = "sqlite:////" + join(basedir, "scape_jobs.db")

app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Use file system as temporary storage
IMAGES_STORE = '/tmp/scraper/'
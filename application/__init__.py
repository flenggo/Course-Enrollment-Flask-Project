from flask import Flask
from config import Config
from application.extensions import db
from application.routes import routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Register blueprints (order matters — do this after app/db init)
from application.routes import routes
from application.api import api

app.register_blueprint(routes)
app.register_blueprint(api)

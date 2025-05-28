from flask import Flask
from config import Config
from application.extensions import db
from application.routes import routes
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Swagger for API documentation
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Course Enrollment API",
        "description": "API documentation for course and enrollment management",
        "version": "1.0.0"
    }
})


# Initialize extensions
db.init_app(app)

# Register blueprints (order matters — do this after app/db init)
from application.routes import routes
from application.api import api

app.register_blueprint(routes)
app.register_blueprint(api)

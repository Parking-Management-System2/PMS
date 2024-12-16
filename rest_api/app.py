from flask import Flask
from flasgger import Swagger
from rest_api.db.database import initialize_database
from rest_api.routes.car_routes import cars_blueprint
from rest_api.routes.parking_routes import parking_blueprint
from rest_api.routes.activity_routes import activity_blueprint

app = Flask(__name__)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "Parking Management REST API",
    "description": "This is the API documentation for the Parking Management System. It includes endpoints for managing cars, parking spots, and activities."
}

# Initialize Swagger
swagger = Swagger(app, config=swagger_config)

# Register blueprints
app.register_blueprint(cars_blueprint, url_prefix="/cars")
app.register_blueprint(parking_blueprint, url_prefix="/parking_spots")
app.register_blueprint(activity_blueprint, url_prefix="/activities")

if __name__ == "__main__":
    # Initialize database
    initialize_database()
    # Run the app
    app.run(debug=True)
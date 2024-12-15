from flask import Flask
from rest_api.db.database import initialize_database
from rest_api.routes.cars_routes import cars_blueprint
from rest_api.routes.parking_routes import parking_blueprint
from rest_api.routes.activity_routes import activity_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(cars_blueprint, url_prefix="/cars")
app.register_blueprint(parking_blueprint, url_prefix="/parking")
app.register_blueprint(activity_blueprint, url_prefix="/activity")

if __name__ == "__main__":
    # Initialize database
    initialize_database()
    # Run the app
    app.run(debug=True)

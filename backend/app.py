from flasgger import Swagger
from flask import Flask

from backend.db.database import initialize_database
from routes.activity import activity_bp
from routes.spot import spot_bp  # Import the spot blueprint

app = Flask(__name__)
app.register_blueprint(activity_bp, url_prefix='/activities')
app.register_blueprint(spot_bp, url_prefix='/spots')  # Register the spot blueprint

swagger = Swagger(app)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)

from flasgger import Swagger
from flask import Flask

from backend.db.database import initialize_database
from routes.activity import activity_bp

app = Flask(__name__)
app.register_blueprint(activity_bp, url_prefix='/activities')

swagger = Swagger(app)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)

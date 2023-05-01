from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from src.routes import auth, gpu
import os

app = Flask(__name__)
app.testing = True
load_dotenv()

# JWT configuration with secret key
secret = os.getenv("JWT_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = secret
jwt = JWTManager(app)

# Blueprints declaration
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(gpu, url_prefix="/api/gpu")


@app.route("/api/status")
def status():
    return jsonify({"status": "online", "version": 0.1})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT"))

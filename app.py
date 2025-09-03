from flask import Flask
from config import Config
from sqlalchemy.sql import text
from flask_cors import CORS
from extensions import db, jwt
from routes.movies_bp import movies_bp
from routes.users_bp import users_bp
from os import environ

app = Flask(__name__)
app.config.from_object(Config)  # URL


db.init_app(app)  # Call
jwt.init_app(app)
CORS(app)


@jwt.unauthorized_loader
def _unauth(e):
    return {"error": "missing/invalid token"}, 401


@jwt.expired_token_loader
def _expired(h, p):
    return ({"error": "token expired"}), 401


with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
    except Exception as e:
        print("Error connecting to the database:", e)


@app.get("/")
def hello_world():
    print("Super")
    return "<h1>Hello, World! 🎊🍊 🌽</h1>"


app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(users_bp, url_prefix="/api/users")


if __name__ == "__main__":
    port = environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True)

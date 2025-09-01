from flask import Flask
from config import Config
from sqlalchemy.sql import text
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)  # URL


db.init_app(app)  # Call


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


from routes.movies_bp import movies_bp

app.register_blueprint(movies_bp, url_prefix="/api/movies")

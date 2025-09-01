from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config.from_object(Config)  # URL

db = SQLAlchemy()
db.init_app(app)  # Call


with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
    except Exception as e:
        print("Error connecting to the database:", e)

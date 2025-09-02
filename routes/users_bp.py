from flask import Blueprint, request
from models.user import User
from extensions import db


users_bp = Blueprint("users_bp", __name__)

HTTP_NOT_FOUND = 404
HTTP_CREATED = 201
HTTP_ERROR = 500


@users_bp.post("/signup")
def create_user():
    data = request.get_json()
    new_user = User(**data)
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Sign Up Successful"}, HTTP_CREATED
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR


@users_bp.post("/login")
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username / password required"}, 400
    db_user = User.query.filter_by(username=username).first()
    if not db_user:
        return {"error": "username or password is incorrect"}, 401

    # User ✅ but Password?
    db_user = db_user.to_dict()

    # Password Check
    if db_user.get("password") != password:
        return {"error": "username or password is incorrect"}, 401

    print("login ✨✨✨✨")
    return {"message": "Login Up Successful"}

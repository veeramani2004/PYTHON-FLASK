from flask import Blueprint, request
from models.movie import Movie
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt


HTTP_NOT_FOUND = 404
HTTP_CREATED = 201
HTTP_ERROR = 500


movies_bp = Blueprint("movies_bp", __name__)


@movies_bp.get("/")
@jwt_required()
def get_movies():
    movies = [movie.to_dict() for movie in Movie.query.all()]
    return movies


@movies_bp.get("/<id>")
def get_movie_by_id(id):
    print(id, type(id))

    data = Movie.query.get(id)

    if not data:
        return {"message": "Movie not found"}, HTTP_NOT_FOUND

    movie = data.to_dict()
    return movie


@movies_bp.delete("/<id>")
def delete_movie_by_id(id):
    data = Movie.query.get(id)

    if not data:
        return {"message": "Movie not found"}, HTTP_NOT_FOUND

    movie = data.to_dict()
    try:
        # Row lock
        db.session.delete(data)
        # raise Exception("Oh no")
        db.session.commit()
        # Row release

        return movie
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR


@movies_bp.post("/")
def create_movie():
    # List (Dict) -> JSON
    data = request.get_json()  # JSON -> Dict, List(Dict)
    # Movie(name=new_movie['name'], rating=new_movie['rating'])

    new_movie = Movie(**data)  # id
    try:
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.to_dict(), HTTP_CREATED
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR


@movies_bp.put("/<id>")
def update_movie(id):
    body = request.get_json()  # body

    print(id)

    try:
        updated = Movie.query.filter_by(id=id).update(body)

        if not updated:
            return {"message": "Movie not found"}, HTTP_NOT_FOUND

        db.session.commit()
        data = Movie.query.get(id)
        return data.to_dict()

    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR

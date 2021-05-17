import os
import sys
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, db_drop_and_create_all, setup_db, db
from auth import AuthError, requires_auth


class Already_Exists_Error(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

ITEMS_PER_PAGE = 10


# defining a function to paginate items for a page
def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    items = [item.format() for item in selection]
    return items[start:end]


# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    uncomment the following line to initialize the database
    !! NOTE drops all tables and start the database from scratch
    should be run the first time running the app
    '''
    # db_drop_and_create_all(db)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # login
    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login_results")
    def login_results():
        return render_template("login_results.html")

    # get all actors
    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(payload):
        # get all actors and return them formatted
        selection = Actor.query.order_by(Actor.id).all()
        actors = paginate_items(request, selection)
        actors_count = Actor.query.count()
        return jsonify({
            "success": True,
            "actors": actors,
            "actors_count": actors_count
        })

    # get all movies
    @app.route("/movies")
    @requires_auth("get:movies")
    def get_movies(payload):
        # get all movies and return them formatted
        selection = Movie.query.order_by(Movie.id).all()
        movies = paginate_items(request, selection)
        movies_count = Movie.query.count()
        return jsonify({
            "success": True,
            "movies": movies,
            "movies_count": movies_count
        })

    # post a new actor
    @app.route("/actors", methods=['POST'])
    @requires_auth("post:actors")
    def add_actor(payload):
        # get the request data
        data = request.get_json()
        if data is None:
            abort(400)
        try:
            name = data['name']
            age = data.get('age')
            gender = data.get('gender')
            # check if actor already exists in database
            the_actor = Actor.query.filter(Actor.name == name).one_or_none()
            if the_actor is not None:
                raise Already_Exists_Error({
                    "code": "Conflict",
                    "description": "actor already exists in database"
                }, 409)
            # insert the actor to the database
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            # return success with the added actor data
            the_actor = Actor.query.filter(
                Actor.name == actor.name).one_or_none()
            actor_id = the_actor.id
            return jsonify({
                "success": True,
                "created": actor_id
            })

        except Exception as e:
            print(e)
            if isinstance(e, Already_Exists_Error):
                raise Already_Exists_Error({
                    "code": "Conflict",
                    "description": "actor already exists in database"
                }, 409)
            else:
                abort(422)

    # post a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def add_movie(payload):
        # get the request data
        data = request.get_json()
        if data is None:
            abort(400)
        try:
            title = data['title']
            release_date = data.get('release_date')
            the_movie = Movie.query.filter(Movie.title == title).one_or_none()
            # check if movie already exists in database
            if the_movie is not None:
                raise Already_Exists_Error({
                    "code": "Conflict",
                    "description": "movie already exists in database"
                }, 409)
            # insert the movie to the database
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            # return success with the added movie data
            the_movie = Movie.query.filter(Movie.title == title).one_or_none()
            movie_id = the_movie.id
            return jsonify({
                "success": True,
                "created": movie_id
            })

        except Exception as e:
            print(e)
            if isinstance(e, Already_Exists_Error):
                raise Already_Exists_Error({
                    "code": "Conflict",
                    "description": "movie already exists in database"
                }, 409)
            else:
                abort(422)

    # update an existing actor data
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor(payload, actor_id):
        # check if the requested actor exists
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        # get the request data
        data = request.get_json()
        if data is None:
            abort(400)
        try:
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            # update the actor information
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            actor.update()
            updated_actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()
            return jsonify({
                "success": True,
                "actor": updated_actor.format()
            })
        except Exception as e:
            print(e)
            abort(422)

    # update an existing movie data
    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie(payload, movie_id):
        # get the request data
        data = request.get_json()
        if data is None:
            abort(400)
        # check if the requested movie exists
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            title = data.get('title')
            release_date = data.get('release_date')
            # update the movie information
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date
            movie.update()
            updated_movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()
            return jsonify({
                "success": True,
                "movie": updated_movie.format()
            })
        except Exception as e:
            print(e)
            abort(422)

    # delete an actor
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        # check if the actor exists in the database
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            # delete actor from database
            actor.delete()
            return jsonify({
                "success": True,
                "deleted": actor.id
            })
        except Exception as e:
            print(e)
            abort(e)

    # delete a movie
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        # check if the movie exists in the database
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            # delete movie from database
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception as e:
            print(e)
            abort(e)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def Auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    @app.errorhandler(Already_Exists_Error)
    def Already_Exists_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

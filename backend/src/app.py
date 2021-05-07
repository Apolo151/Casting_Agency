import os
import sys
sys.path.append(".")
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import Actor, Movie, Casting, db_drop_and_create_all, setup_db, db


def format_model(model_list):
    formatted = [item.format() for item in model_list]
    return formatted


#main_view_func = Main.as_view('main')


#create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    uncomment the following line to initialize the database 
    !! NOTE drops all tables and start the database from scratch
    '''
    #db_drop_and_create_all(db)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # get all actors
    @app.route("/actors")
    def get_actors():
        # get all actors and return them formatted
        actors = Actor.query.all()
        actors_count =  Actor.query.count()
        actors_list = format_model(actors)
        return jsonify({
            "success": True,
            "actors": actors_list,
            "actors_count": actors_count
        })

    # get all movies
    @app.route("/movies")
    def get_movies():
        # get all movies and return them formatted
        movies = Movie.query.all()
        movies_count = Movie.query.count()
        movies_list = format_model(movies)
        return jsonify({
            "success": True,
            "movies": movies_list,
            "movies_count": movies_count
        })

    # post a new actor
    @app.route("/actors", methods=['POST'])
    def add_actor():
        try:
            # get the request data
            data = request.get_json()
            if data == None:
                abort(400)
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            # insert the actor to the database
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            # return success with the added actor data
            the_actor = Actor.query.filter(Actor.name == actor.name).one_or_none()
            formatted_actor = the_actor.format()
            return jsonify({
                "success": True,
                "actor": formatted_actor
            })

        except Exception as e:
            print(e)
            abort(422)

    # post a new movie
    @app.route('/movies', methods=['POST'])
    def add_movie():
        try:
            # get the request data
            data = request.get_json()
            if data == None:
                abort(400)
            title = data.get('title')
            release_date = data.get('release_date')
            # insert the movie to the database
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            # return success with the added movie data
            the_movie = Movie.query.filter(Movie.title == title).one_or_none()
            formatted_movie = the_movie.format()
            return jsonify({
                "success": True,
                "movie": formatted_movie
            })

        except Exception as e:
            print(e)
            abort(422)

    # update an existing actor data
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        try:
            # get the request data
            data = request.get_json()
            if data is None:
                abort(400)
            # check if the requested actor exists
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
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
            updated_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            return jsonify({
                "success": True,
                "actor": updated_actor.format()
            })
        except Exception as e:
            print("the update actor exception:")
            print(e)
            abort(422)

    # update an existing movie data
    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    def update_movie(movie_id):
        try:
            # get the request data
            data = request.get_json()
            if data is None:
                abort(400)
            # check if the requested movie exists
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            title = data.get('title')
            release_date = data.get('release_date')
            # update the movie information
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date
            movie.update()
            updated_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            return jsonify({
                "success": True,
                "actor": updated_movie.format()
            })
        except Exception as e:
            print(e)
            abort(422)

    # delete an actor
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            # check if the actor exists in the database
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            # delete actor from database
            actor.delete()
            return jsonify({
                "success": True,
                "deleted": actor.id
            })
        except Exception as e:

            print(e)
            abort(404)

    # delete a movie
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            # check if the movie exists in the database
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            # delete movie from database
            movie.delete()
            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception as e:
            print(e)
            abort(404)


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
        }), 404


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


    #@app.errorhandler(AuthError)
    #def Auth_error(error):
        #return jsonify({
        #    "success": False,
        #    "error": error.status_code,
        #    "message": error.error
        #}), error.status_code

    return app

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

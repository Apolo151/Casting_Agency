import os
import sys
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db


class CastingAgencyTestCase(unittest.TestCase):
    """ The Casting Agency test case """

    def setUp(self):
        """ initialize app and define teset variables """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)
        db.create_all()

        self.casting_assistant_header = {
            'Authorization': "Bearer {}".format(
                os.environ['CASTING_ASSISTANT_TOKEN'])
        }

        self.casting_director_header = {
            'Authorization': "Bearer {}".format(
                os.environ['CASTING_DIRECTOR_TOKEN'])
        }

        self.executive_producer_header = {
            "Authorization": "Bearer {}".format(
                os.environ['EXECUTIVE_PRODUCER_TOKEN'])
        }

        self.all_perms_header = self.executive_producer_header

        self.unvalid_token_header = {
            "Authorization": "invalid_token"
        }

        self.new_actor = {
            "name": "Tom Cruise",
            "age": 58,
            "gender": "male"
        }

        self.new_movie = {
            "title": "Tenet",
            "release_date": "2020-8-12"
        }

        self.invalid_actor_json = {
            "name": "unknown",
            "agw": 33,
            "gendr": "male"
        }

        self.invalid_movie_json = {
            "title": "new_movie",
            "relse_dat": "2022-3-6"
        }

        self.update_actor_json = {
            "name": "Scarlett Johansson",
            "gender": "female"
        }

        self.update_movie_json = {
            "release_date": "2025-6-9"
        }

        self.update_movie_date = (2025, 6, 9)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """ Executed after each test """
        pass

    '''
    Tests for Auth
    '''

    # casting assistant tests

    def test_get_actors_CA(self):
        res = self.client().get(
            "/actors", headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data["actors_count"])

    def test_cannot_post_actors_CA(self):
        res = self.client().post(
            "/actors", headers=self.casting_assistant_header,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], "Forbidden")
        self.assertEqual(
            data['message']['description'],
            "permission not found")

    # casting director tests

    def test_patch_actor_CD(self):
        res = self.client().patch(
            '/actors/3', json=self.update_actor_json,
            headers=self.casting_director_header)
        data = json.loads(res.data)
        actor = Actor.query.get(3)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 3)
        self.assertEqual(actor.name, self.update_actor_json['name'])
        self.assertEqual(actor.gender, self.update_actor_json['gender'])

    def test_cannot_delete_movie_no_auth_header_CD(self):
        res = self.client().delete("/movies/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message']['code'],
            'authorization_header_missing')
        self.assertEqual(
            data['message']['description'],
            'Authorization header is expected')

    # executive producer tests

    def test_delete_movie_EP(self):
        res = self.client().delete(
            "/movies/3", headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    def test_post_movie_unvalid_token_EP(self):
        res = self.client().post(
            "/movies", headers=self.unvalid_token_header,
            json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], "invalid_header")
        self.assertEqual(
            data['message']['description'],
            "Authorization must start with 'Bearer'.")
    '''
    Tests for GET endpoints
    '''

    def test_get_actors(self):
        res = self.client().get("/actors", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertTrue(data["actors_count"])

    def test_get_actors_bad_url(self):
        res = self.client().get('/actors/2', headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertTrue(data["movies_count"])

    def test_get_movies_bad_url(self):
        res = self.client().get("/movies/3", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    '''
    Tests for POST endpoints
    '''

    def test_post_actor(self):
        res = self.client().post(
            "/actors", json=self.new_actor,
            headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_post_actor_bad_json(self):
        res = self.client().post(
            "/actors", json=self.invalid_actor_json,
            headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_movie(self):
        res = self.client().post(
            "/movies", json=self.new_movie,
            headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_post_movie_no_data(self):
        res = self.client().post(
            '/movies', headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    '''
    Tests for PATCH endpoints
    '''

    def test_update_actor_info(self):
        res = self.client().patch(
            '/actors/1', json=self.update_actor_json,
            headers=self.all_perms_header)
        data = json.loads(res.data)
        actor = Actor.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 1)
        self.assertEqual(actor.name, self.update_actor_json['name'])
        self.assertEqual(actor.gender, self.update_actor_json['gender'])

    def test_update_actor_info_no_data(self):
        res = self.client().patch(
            '/actors/1', headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_movie_info(self):
        res = self.client().patch(
            '/movies/1', json=self.update_movie_json,
            headers=self.all_perms_header)
        data = json.loads(res.data)
        movie = Movie.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 1)
        self.assertEqual(
            movie.release_date, datetime.date(*self.update_movie_date))

    def test_update_movie_info_no_movie(self):
        res = self.client().patch(
            '/movies/77', json=self.update_movie_json,
            headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests for DELETE endpoints
    '''

    def test_delete_actor(self):
        res = self.client().delete(
            "/actors/2", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_actor_does_not_exist(self):
        res = self.client().delete(
            "/actors/33", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete(
            "/movies/2", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_movie_does_not_exist(self):
        res = self.client().delete(
            "/movies/99", headers=self.all_perms_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

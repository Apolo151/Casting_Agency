# Casting agency backend

## Motivation
This is the last project in the Udacity Fullstack Nanodegree
It is an api of a casting agency.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

Running the project locally means that it can´t access Herokus env variables. To fix this, you need to edit a few informations in setup.py, so it can connect to a local database

- open setup.sh and change the DATABASE_PATH and TEST_DATABASE_PATH to your database path.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the postgres database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

first, to export the environment variables, run:
```bash
. setup.sh
```


Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Api documentation
### Api Base URL
https://herokuab

### Endpoints

### get /login
returns the html template for login page

### get /login-results
returns the html template for the login-results page (the callback URL after login)

### Get /actors
query paginated actors
```bash
curl https://afhsaf/actors
```
- Fetches a list of dictionaries of actors
- Requires permission: `get:actors`
- Request Arguments: integer `page` (defaults to 1 if not provided)
- Request Headers: None
- Returns:
  - A list of actors objects with the fields:
    - integer `id`
    - string `name`
    - integer `age`
    - string `gender`
  - An integer `actors_count` (total number of actors)
  - A boolean `success`
#### Example response
```python
{
    "actors": [
        {
            "age": 54,
            "gender": "female",
            "id": 3,
            "name": "Salma Hayek"
        },
        {
            "age": 64,
            "gender": "male",
            "id": 2,
            "name": "Tom Hanks"
        },
        {
            "age": 58,
            "gender": "male",
            "id": 4,
            "name": "Tom Cruise"
        }
    ],
    "actors_count": 3,
    "success": true
}
```

### Get /movies
query paginated movies
```bash
curl https://hafda/movies
```
- Fetches a list of dictionaries of movies
- Requires permission: `get:movies`
- Request Arguments: integer `page` (defaults to 1 if not provided)
- Request Headers: None
- Returns:
  - A list of movies objects with the fields:
    - integer `id`
    - string `title`
    - date `release_date`
  - An integer `movies_count` (total number of movies)
  - A boolean `success`
  #### Example response
```python
{
    "movies": [
        {
            "id": 2,
            "release_date": "Tue, 05 Dec 2017 00:00:00 GMT",
            "title": "Jumanji"
        },
        {
            "id": 3,
            "release_date": "Thu, 10 Jan 2019 00:00:00 GMT",
            "title": "The Upside"
        },
        {
            "id": 1,
            "release_date": "Mon, 09 Jun 2025 00:00:00 GMT",
            "title": "Whiplash"
        }
    ],
    "movies_count": 3,
    "success": true
}
```

### POST /actors
add an actor to the database
```bash
curl -X POST https://afsgga/actors
```
- Requires permission: `post:actors`
- Request Arguments: None
- Request Headers: `Content-Type: application/json`
- Request body (all fields are required):
  - string `name`: actor name
  - integer `age`: actor age
  - string `gender`: actor gender

  #### Example Request body
  ```python
  {
      "name": "Tom Cruise",
      "age": 58,
      "gender": "male"
    }
  ```
- Returns:
  - Integer `created` (created actor id)
  - boolean `success`

  #### Example Response
  ```python
  {
    "created": 4,
    "success": true
  }
  ```

### POST /movies
add a movie to the database
```bash
curl -X POST https://htsgsa/movies
```
- Requires permission: `post:movies`
- Request Arguments: None
- Request Headers: `Content-Type: application/json`
- Request body (all fields are required):
  - string `title`: movie title
  - date `release_date`: movie release date 
  #### Example Request Body
  ```python
  {

      "title": "Tenet",
      "release_date": "2020-8-12"

  }
  ```
- Returns:
  - Integer `created` (created movie id)
  - boolean `success`

  #### Example Response
  ```python
  {
    "created": 4,
    "success": true
  }
  ```

### PATCH /actors
update an existing actor
```bash
curl -X PATCH https://faadsfa/actors/1
```
- Requires permission: `patch:actors`
- Request Arguments: integer `actor_id` (the id of the actor you want to modify)
- Request Headers: `Content-Type: application/json`
- Request body (all fields are optional):
  - string `name`
  - integer `age`
  - string `gender`
  #### Example Request Body
  ```python
  {
      "name": "Scarlett Johansson",
      "age": 32,
  }
  ```
- Returns:
  - object `actor` (the updated actor)
  - boolean `success`
  #### Example Response
  ```python
  {
    "actor": {
        "age": 32,
        "gender": "female",
        "id": 1,
        "name": "Scarlett Johansson"
    },
    "success": true
  }
  ```

### PATCH /movies
update an existing movie
```bash
curl -X PATCH https://faadsfa/movies/1
```
- Requires permission: `patch:movies`
- Request Arguments: integer `movie_id` (the id of the movie you want to modify)
- Request Headers: `Content-Type: application/json`
- Request body (all fields are optional):
  - string `title`
  - date `release_date`
  #### Example Request Body
  ```python
  {
      "title": "Django Unchained"
  }
  ```
- Returns:
  - object `movie` (the updated movie)
  - boolean `success`
  #### Example Response
  ```python
  {
    "movie": {
        "id": 1,
        "release_date": "Mon, 09 Jun 2025 00:00:00 GMT",
        "title": "Django Unchained"
    },
    "success": true
  }
  ```

### DELETE /actors
delete an actor from database
```bash
curl -X DELETE https://faadsfa/actors/1
```
- Requires permission: `delete:actors`
- Request Arguments: integer `actor_id` (the id of the actor you want to delete)
- Request Headers: None
- Returns:
  - integer `deleted` (the deleted actor id)
  - boolean `success`
  #### Example Response
  ```python
  {
    "deleted": 1,
    "success": true
  }
  ```

### DELETE /movies
delete a movie from database
```bash
curl -X DELETE https://faadsfa/movies/1
```
- Requires permission: `delete:movies`
- Request Arguments: integer `movie_id` (the id of the movie you want to delete)
- Request Headers: None
- Returns:
  - integer `deleted` (the deleted movie id)
  - boolean `success`
  #### Example Response
  ```python
  {
    "deleted": 1,
    "success": true
  }
  ```


   




## Error Handling
- Errors are returned as a JSON object in the following format:
```python
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}
```

### Error codes the API returns:
- 401 : `unauthorized`
- 403 : `Forbidden`
- 409 : `Conflict`
- 400 : `bad request`
- 404 : `resource not found`
- 422 : `unprocessable`
- 405 : `method not allowed`
- 500 : `internal server error`

## Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
python test_app.py
```
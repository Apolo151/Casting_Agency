# Casting agency backend

## Motivation
This is a project to showcase learnt backend skills, where I built a Casting Agency API from scratch.
This is the project I submitted as a Capstone project in the Udacity Fullstack Nanodegree.

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

For the project to be able to connect to your local database you will have to:
- open setup.sh and change the DATABASE_URL and TEST_DATABASE_URL to your database URL and test databse URL.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the postgres database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

to export the environment variables, run:
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

### Api Base URL (currently not working)
https://fsnd-ca.herokuapp.com/

### Endpoints

### get /login
returns the html template for login page

### get /login-results
returns the html template for the login-results page (the callback URL after login)

### Get /actors
query paginated actors
```bash
curl https://fsnd-ca.herokuapp.com/actors
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
curl https://fsnd-ca.herokuapp.com/movies
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
curl -X POST https://fsnd-ca.herokuapp.com/actors
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
curl -X POST https://fsnd-ca.herokuapp.com/movies
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
curl -X PATCH https://fsnd-ca.herokuapp.com/actors/1
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
curl -X PATCH https://fsnd-ca.herokuapp.com/movies/1
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
curl -X DELETE https://fsnd-ca.herokuapp.com//actors/1
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
curl -X DELETE https://fsnd-ca.herokuapp.com/movies/1
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
- Errors are returned as a JSON object with keys:
  - boolean `success`
  - integer `error`
  - string `message`

  ### Example Error 
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


## AUTH
Auth0 is setup with RBAC
and the bearer tokens for all roles are in setup.sh, 
you can use them with the `Authorization` header for your API calls to the running api at the BASE URl.
  ### EXAMPLE
  ```bash
   curl https://fsnd-ca.herokuapp.com/actors -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikt6dEE0ZHY4UVJCT0kyTXkxbTlFNiJ9.eyJpc3MiOiJodHRwczovL2Fwb2xsbzE1MS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA5NmFlMTM2OWI2MjgwMDY4NjJkMWFkIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2MjEyMTEyNDIsImV4cCI6MTYyMTI5NzY0MiwiYXpwIjoiZldUazhMZjZLOGI3T1d0WDJobkYxenZGcU44djVVcDIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Ou3BguKxjU32gfeXnMYPFqEYsOjX1cGEGcrtnVMl3CGtPDn-w7vqrlYfr0Spjaj6eo-UDYFyUiu0ungrY0DdzRGcgAc9d9YZdont6foVCLFWcG356BTq1BZnAqtImnF5AbkYeKd7pC7W-7-Vcf49Ng4V_W4O-oI4FiVDLKlDZgAjqRpZNZ0PWK8e7T4BqvQ2CQUfyO6qNhygEI3y5q4ZfF0h8JrIXqAwYqi4ftcZjTQB71piQW0z6U_Yqcq0zx30KEpWY8EVi7vbCXSJV2RnZ8bdKXaAnJE7heWIAVlwakH-Dl-hKcBCXgZH8EX7bUrqtNeejLciwq9F7q8kO5Ip6w'
  ```

if you want to setup Auth0 for local use:
1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, regular web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. change the AUTH0_DOMAIN and API_AUDIENCE environment variables in the setup.sh to yours.
6. Create new API permissions:
    - `get:actors`: get actors from the database
    - `get:movies`: get movies from the database
    - `post:actors`: add actors to the database
    - `post:movies`: add movies to the database
    - `patch:actors`: modify existing actors in the database
    - `patch:movies`: modify existing movies in the database
    - `delete:actors`: delete actors form the database
    - `delete:movies`: delete movies from the database
7. Create new roles and assign each it's permissions as following:
    - Casting assistant
        - can `get:actors`
        - can `get:movies`
    - Casting director, has same permissions as casting assistant plus
        - can `post:actors`
        - can `patch:actors`
        - can `patch:movies`
        - can `delete:actors`
    - Executive producer
        - can perform all actions
Test the endpoints with [Postman](https://getpostman.com) or using curl
    - Register 3 users - assign each user a unique role.
    - Sign into each account and make note of the JWT.
    - use the JWT tokens for your local api calls
    - go to the login.html file in the templates directory and change the herf on the button to your url in the format
    ```bash
    https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
    ```


## Testing
before running the tests, run
```bash
dropdb CA_test && createdb CA_test
psql CA_test < CA.psql
```
to run the unittest tests, run
```bash
python test_app.py
```
- if everything went well it should return
```bash
........
----------------------------------------------------------------------
Ran 22 tests in 9.989s

OK
```

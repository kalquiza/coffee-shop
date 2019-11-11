# Coffee Shop Backend

## Setting up the Backend

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

**db_drop_and_create_all()** in **api.py** must be uncommented on the first run to initialize the database. This line is left uncommented by default. When the server is reloaded all records will be dropped and the database will start from scratch. Uncomment or remove this line if running a server where the data should persist.
>_tip_: the postman collection tests on a newly initialized database, ensure this line is uncommented when testing.

```py
"""
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()
```
Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Setting up Auth0
Use the third-party application [Auth0](https://auth0.com/) to implement authentication and role-based access control (**RBAC**).

- Create a new [Auth0](https://auth0.com/) Account
- Select a unique tenant domain
- Create a new, single page web application
- Create a new API
    - in API Settings:
      - Enable RBAC
      - Enable Add Permissions in the Access Token
- Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
  
- Create new roles for:
    - Barista
      - can `get:drinks-detail`
    - Manager
        - can perform all actions

- Configure the application variables in `./src/auth/auth.py`:
```py
    AUTH0_DOMAIN = {AUTH0 DOMAIN PREFIX}
    ALGORITHMS = ['RS256']
    API_AUDIENCE = {AUTH0 APP API AUDIENCE}
``` 

## Testing
Test your endpoints with [Postman](https://getpostman.com). 

- Register 2 users - assign the Barista role to one and Manager role to the other.
- Sign into each account and make note of the JWT. We will provide these JWTs in our tests.
- Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
- Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and include the JWT in the token field you made note of previusly.
- Run the collection

>_tip_: ensure you are providing a recent JWT to ensure it is not expired and the user has not logged out of the account.

## API Reference

### Endpoints

#### GET /drinks
- A public endpoint that retrieves the list of drinks.
- Returns a success value and list of drinks in the drink.short() representation.
> Example : `curl --location --request GET "localhost:5000/drinks"`
```
{
   "drinks": [{
         "id": 1,
         "recipe": [{
               "color": "blue",
               "parts": 1
        }],
        "title":"Water"
    }],
   "success":true
}
```

#### GET /drinks-detail
- An endpoint that retrieves a detailed list of drinks. Requires the 'get:drinks-detail' permission.
- Returns a success value and list of drinks in the drink.long() representation.
> Example : `curl --location --request GET "localhost:5000/drinks-detail`
```
{
    "drinks": [{
        "id": 1,
        "recipe": {
            "color": "blue",
            "name": "Water",
            "parts": 1
        },
        "title": "Water"
    }],
    "success": true
}
```

#### POST /drinks
- An endpoint that creates a new row in the drinks table. Requires the 'post:drinks' permission.
- Returns a success value and list containing only the newly created drink in the drink.long() representation.
> Example: `curl http://127.0.0.1:5000/drinks -X POST -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "Water", "recipe": {"name": "Water", "color": "blue", "parts": 1}}'`
```
{
    "drink": {
        "id": 1,
        "recipe": {
            "color": "blue",
            "name": "Water",
            "parts": 1
        },
        "title": "Water"
    },
    "success": true
}
```
#### PATCH /drinks/\<id>
-   An endpoint that updates the corresponding row for \<id>. Requires the 'patch:drinks' permission. Returns a success value and list containing only the updated drink in the drink.long() representation.
> Example: `curl http://127.0.0.1:5000/drinks/1 -X PATCH -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "Dihydrogen monoxide"}'`
```
{
    "drink": {
        "id": 1,
        "recipe": {
            "color": "blue",
            "name": "Dihydrogen monoxide",
            "parts": 1
        },
        "title": "Water"
    },
    "success": true
}
```

#### DELETE /drinks/\<id>
- An endpoint that deletes the corresponding row for \<id>. Requires the 'delete:drinks' permission.
- Returns a success value and the id of the deleted record.
> Example : `curl -X DELETE -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/drinks/1`
```
{
    "delete": 1,
    "success": true
}
```


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 401,
    "message": "Unauthorized"
}
```
The API will return three error types when requests fail:
- 401: Unauthorized
- 404: Resource Not Found
- 422: Unprocessable

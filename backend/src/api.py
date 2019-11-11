import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()


""" ROUTES """
@app.route('/drinks', methods=['GET'])
def get_drinks():
    """GET /drinks

    A public endpoint that retrieves the list of drinks.

    Returns:
        A status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks in the drink.short() representation or
        appropriate status code indicating reason for failure.
    """
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    """GET /drinks-detail

    An endpoint that retrieves a detailed list of drinks. Requires the
    'get:drinks-detail' permission.

    Args:
        jwt: a json web token (string).

    Returns:
        A status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks in the drink.long() representation or
        appropriate status code indicating reason for failure.
    """
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.long() for drink in selection]

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    """POST /drinks

    An endpoint that creates a new row in the drinks table. Requires the
    'post:drinks' permission.

    Args:
        jwt: a json web token (string).

    Returns:
        A status code 200 and json {"success": True, "drinks": drink} where
        drink is an array containing only the newly created drink in the
        drink.long() representation or appropriate status code indicating
        reason for failure.
    """
    try:
        body = request.get_json()
        req_title = body.get('title', None)
        req_recipe = json.dumps(body.get('recipe', None))

        drink = Drink(title=req_title, recipe=req_recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drink': [drink.long()]
        }), 200

    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    """PATCH /drinks/<id>

    An endpoint that updates the corresponding row for <id>. Requires the
    'patch:drinks' permission.

    Args:
        jwt: a json web token (string).
        drink_id: where <drink_id> is the existing model id (int).

    Returns:
        A status code 200 and json {"success": True, "drinks": drink} where
        drink is an array containing only the updated drink in the drink.long()
        representation or appropriate status code indicating reason for
        failure.
    """
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        body = request.get_json()
        req_title = body.get('title', None)

        drink.title = req_title

        print(drink.long())

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    """
        DELETE /drinks/<id>:
            An endpoint that deletes the corresponding row for <id>. Requires
            the 'delete:drinks' permission.

        Args:
            jwt: a json web token (string).
            drink_id: where <drink_id> is the existing model id (int).

        Returns:
            A status code 200 and json {"success": True, "delete": id} where id
            is the id of the deleted record or appropriate status code
            indicating reason for failure.
    """
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        id = drink.id
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    except Exception as e:
        abort(422)


""" Error Handling """

"""
Error handling for unprocessable entity
"""
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


"""
Error handler for the requested resource could not be found
"""
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


"""
Error handler for when authentication is required and has failed or has not
yet been provided
"""
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

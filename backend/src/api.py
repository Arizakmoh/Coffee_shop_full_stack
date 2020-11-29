#----------------------------------------------------------------------------#
#                           Coder  / student Info
#                   ABDIRIZAK MOHAMED ABDULLAHI
#                      Udacity Course Project 
#                            Class 2020
#              https://www.linkedin.com/in/arizakmoh/
#                  https://github.com/Arizakmoh
#                   +252615591064/+25377145259 
#                     arizakprime@gmail.com
#----------------------------------------------------------------------------#
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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# GET /drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True, 
            'drinks': [drink.long() for drink in drinks]
        }), 200 # returns status code 200 and json {"success": True, "drinks": drinks}
    # or appropriate status code indicating reason for failure
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': repr(e)
        }), 400
'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail') #  it should require the 'get:drinks-detail' permission
def get_drink_details(jwt):
    try:
        drinks = Drink.query.all()
        # it should contain the drink.long() data representation
        drinks = [drink.long() for drink in drinks] 

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200 # returns status code 200 and json {"success": True, "drinks": drinks}
    # or appropriate status code indicating reason for failure
    except Exception as error:
        return jsonify({
            'success': False,
            'drinks': "",
            'error' :   repr(e) 
        }),400


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
 # it should require the 'post:drinks' permission
@requires_auth('post:drinks')
def add_drink(token):
    try:
        if request.data:
            body = request.get_json()
            title = body.get('title', None)
            recipe = body.get('recipe', None)
             
            drink = Drink(title=title, recipe=json.dumps(recipe))
            Drink.insert(drink)

            new_drink = Drink.query.filter_by(id=drink.id).first()

            return jsonify({
                'success': True,
                'drinks': [new_drink.long()] # it should contain the drink.long() data representation
            })
        else:
            return jsonify({
            'success': False,
            'drinks': "",
            'error' :   repr(e) 
        }),400
    # or appropriate status code indicating reason for failure
    except Exception as e: # prevent UNIQUE constraint failed 
        return jsonify({
            'success': False,
            'drinks': "",
            'error' :   repr(e) 
        }),400


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks') # it should require the 'patch:drinks' permission
def edit_drink(payload, id):
    data = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()


    if not drink: 
        abort(404) #it should respond with a 404 error if <id> is not found

    try:
        title = data.get('title')

        if title:
            drink.title = title

        recipe = data.get('recipe', None)
        if recipe:
            drink.recipe = json.dumps(recipe)
        
        drink.update()
    except Exception as e: # prevent UNIQUE constraint failed 
        return jsonify({
            'success': False,
            'drinks': "",
            'error' :   repr(e) 
        })

    return jsonify({
        'success': True, 
        'drinks': [drink.long()]} # it should contain the drink.long() data representation
        ), 200 #returns status code 200 and json {"success": True, "drinks": drink}


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    

    

    try:
        drink = Drink.query.filter_by(id=Drink.id).one_or_none()
        if not drink:
            abort(404)
        drink.delete()
    except BaseException:
        return jsonify({
        'success': True, 
        'delete': id}
        ), 400

    return jsonify({
        'success': True, 
        'delete': id}
        ), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405

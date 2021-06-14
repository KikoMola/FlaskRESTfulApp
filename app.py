# FLASK
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

# RESOURCES
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList

# LIBRARIES
from datetime import timedelta
from secutiry import authenticate, identity
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kiko'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access token': access_token.decode('utf-8'),
        'user.id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)

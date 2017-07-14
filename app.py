from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from security import get_access_token

from resources.account_authentication import AccountAuthentication
from resources.oauth_authentication import OAuthAuthentication
from resources.protected import Protected

APP = Flask(__name__)
API = Api(APP)
APP.secret_key = 'SECRET'

# Setup the Flask-JWT-Extended extension
JWTManager(APP)

# Add API resources.
API.add_resource(AccountAuthentication, '/auth')
API.add_resource(OAuthAuthentication, '/oauth')
API.add_resource(Protected, '/protected')

if __name__ == '__main__':
    APP.run(debug=True)

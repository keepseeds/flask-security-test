from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from security import get_access_token

app = Flask(__name__)
api = Api(app)
app.secret_key = 'SECRET'

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

class AccountAuthentication(Resource):
    """
    This Resource represents a classic email and password
    login authentication route.
    """
    account_parser = reqparse.RequestParser()
    account_parser.add_argument('email', type=str, required=True, help='Username is required.')
    account_parser.add_argument('password', type=str, required=True, help='Password is required.')

    def post(self):
        """
        We POST our authentication request to /auth, with an email and password defined.
        """
        args = self.account_parser.parse_args()

        if args['email'] != 'test' or args['password'] != 'test':
            return {'message': 'Bad username or password'}, 401

        return get_access_token('account', args['email'])

class OAuthAuthentication(Resource):
    """
    This Resource represents authentication provided via a third party application
    such as Facebook or Google; in this instance we are only provided with a token issued
    by the third party and the provider the have authenticated with.

    We will need to check that the user has been registered before, and if not should be
    registered here; so this ultimately becomes both a registration and log in end point.
    """
    VALID_GRANT_TYPES = ('facebook',)

    oauth_parser = reqparse.RequestParser()
    oauth_parser.add_argument('grantType', type=str, required=True, help='Grant Type is required.')
    oauth_parser.add_argument('identifier', type=str, required=True, help='Identifier is required.')
    # maybe user id is required too?

    def post(self):
        """
        We POST our authentication request to /oauth, with a grant type and identifier defined.
        """
        args = self.oauth_parser.parse_args()
        is_valid_grant = args['grantType'] in self.VALID_GRANT_TYPES

        if not is_valid_grant or args['identifier'] != '11d5a981-e218-4b98-aec6-82c0732e5481':
            return {'message': 'Bad values passed through.'}, 401

        return get_access_token(args['grantType'], args['identifier']), 200

class Protected(Resource):
    """
    Demo Resource to test against, this simply shows how to protect a Flask-RESTful endpoint with
    Flask-JWT-Extended.
    """
    @jwt_required
    def get(self):
        """
        Get details about the currently authenticated user.

        This will show details based on the JWT token provided.
        """
        current_user = get_jwt_identity()
        return {'helloFrom': current_user}

# Add API resources.
api.add_resource(AccountAuthentication, '/auth')
api.add_resource(OAuthAuthentication, '/oauth')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)

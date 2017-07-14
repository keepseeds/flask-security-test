from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from security import get_access_token

app = Flask(__name__)
api = Api(app)
app.secret_key = 'SECRET'

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token

class AccountAuthentication(Resource):
    account_parser = reqparse.RequestParser()
    account_parser.add_argument('email', type=str, required=True, help='Username is required.')
    account_parser.add_argument('password', type=str, required=True, help='Password is required.')

    def post(self):
        args = self.account_parser.parse_args()

        if args['email'] != 'test' or args['password'] != 'test':
            return {'message': 'Bad username or password'}, 401

        return get_access_token('account', args['email'])

class OAuthAuthentication(Resource):
    VALID_GRANT_TYPES = ('facebook',)

    oauth_parser = reqparse.RequestParser()
    oauth_parser.add_argument('grantType', type=str, required=True, help='Grant Type is required.')
    oauth_parser.add_argument('identifier', type=str, required=True, help='Identifier is required.')
    # maybe user id is required too?

    def post(self):
        args = self.oauth_parser.parse_args()
        is_valid_grant = args['grantType'] in self.VALID_GRANT_TYPES

        if not is_valid_grant or args['identifier'] != '11d5a981-e218-4b98-aec6-82c0732e5481':
            return {'message': 'Bad values passed through.'}, 401

        return get_access_token(args['grantType'], args['identifier']), 200

class Protected(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'helloFrom': current_user}

# Add API resources.
api.add_resource(AccountAuthentication, '/auth')
api.add_resource(OAuthAuthentication, '/oauth')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)

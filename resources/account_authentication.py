"""
Module for AccountAuthentication Resource
"""
from flask_restful import Resource, reqparse
from security import get_access_token

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

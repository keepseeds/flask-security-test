"""
Module for OAuthAuthentication Resource
"""
from flask_restful import Resource, reqparse
from security import get_access_token

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

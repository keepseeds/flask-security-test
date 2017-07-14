"""
Module for Protected Resource
"""
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

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

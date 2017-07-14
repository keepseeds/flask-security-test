from flask import jsonify
from flask_jwt_extended import create_access_token

def get_access_token(grantType, identifier):
    identity = {'grantType': grantType, 'identifier': identifier}
    token = create_access_token(identity=identity)

    return jsonify({'accessToken': token})

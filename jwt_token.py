""" JWT configuration """
from flask_jwt_extended import JWTManager

jwt = JWTManager()

# Blocklist para almacenar tokens revocados
blocklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    """ Check if token in blocklist """
    jti = jwt_payload['jti']
    return jti in blocklist

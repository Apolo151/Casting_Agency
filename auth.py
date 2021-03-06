import json
import os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
get_token_auth_header() method
    it attempts to get the header from the request
        it raises an AuthError if no header is present
    it attempts to split bearer and the token
        it raises an AuthError if the header is malformed
    returns the token part of the header
'''


def get_token_auth_header():
    # getting the request authorization header
    header = request.headers.get('Authorization', None)
    if not header:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)
    # spilting and checking that the token is a bearer token
    parts = header.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization must start with 'Bearer'."
        }, 401)
    elif len(parts) != 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be a bearer token"
        }, 401)
    return parts[1]


'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it raises an AuthError if permissions are not included in the payload
    it raises an AuthError if the requested permission
    string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    # checking that the permissions key is in the decoded jwt payload
    if "permissions" not in payload:
        raise AuthError({
            "code": "invaild_claim",
            "description": "permissions not in JWT"
        }, 400)
    # checking that the required permission is in the decoded jwt payload
    if permission not in payload['permissions']:
        print(payload['permissions'])
        raise AuthError({
            "code": "Forbidden",
            "description": "permission not found"
        }, 403)

    return True


'''
    verify_decode_jwt method(token)
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it verifys the token using Auth0 /.well-known/jwks.json
    it decodes the payload from the token
    it validates the claims
    returns the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it uses the get_token_auth_header method to get the token
    it uses the verify_decode_jwt method to decode the jwt

    it uses the check_permissions method validate
    claims and check the requested permission

    returns the decorator which passes the decoded
    payload to the decorated method
'''

# defining the rquires_auth decorator method to use on api routes


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

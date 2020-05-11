from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import jwt_decode_handler, jwt_get_username_from_payload
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import jwt

class JWTAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        try:
            user = self.authenticate_credentials(token)
            scope['user'] = user
        except Exception as err:
            print(err)
            scope['user'] = AnonymousUser()
        return self.inner(scope)

    def authenticate_credentials(self, token):
        User = get_user_model()
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise Exception(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise Exception(msg)
        except jwt.InvalidTokenError:
            raise Exception(msg)

        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user

JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))

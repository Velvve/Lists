import sys

from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    """беспарольный серверный процессор аунтентификации"""

    def authenticate(self, request, uid):
        """аутентифицировать"""
        try:
            print('uid', file=sys.stderr)
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            print('user', file=sys.stderr)
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            print('token', file=sys.stderr)
            return None

    def get_user(self, email):
        """получить пользователя"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import User


class UserBackend(ModelBackend):
    """
    This overrides the authenticate method of the ModelBackend class and helps us
    modify the authentication process that allows a user login with either their username or email.
    """

    def authenticate(self, request, **kwargs):
        email = kwargs["username"]
        password = kwargs["password"]
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) is True:
                # this checks if the password provided corresponds with an existing user
                return user
        except User.DoesNotExist:
            pass
            # this checks the user input against the database. if a user does not exist, the views.py will handle the error message.


# The form and view can remain unchanged and keep the fields name as username and password. We need to add CustomerBackend to AUTHENTICATION_BACKENDS.

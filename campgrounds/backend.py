# backend.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Retrieve the custom user model
UserModel = get_user_model()

# Custom authentication backend for handling email or username login
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Initialize user to None
        user = None

        # Check if username is an email address
        if username:
            try:
                # Attempt to retrieve user by email
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                # If user not found by email, continue to next check
                pass

        # If user not found by email or username is not provided, or if username is not an email
        if user is None and username:
            try:
                # Attempt to retrieve user by username
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # If user not found by username, continue to password check
                pass

        # If user found and password is correct
        if user and user.check_password(password):
            # Return the authenticated user
            return user

        # If no user found or password is incorrect, return None
        return None

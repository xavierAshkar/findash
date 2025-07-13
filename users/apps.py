"""
users/apps.py

Handles the configuration of the users application.
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

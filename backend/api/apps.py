import os

from django.apps import AppConfig
from django.db.utils import DatabaseError
from django.db.models.signals import post_migrate


def create_default_admin(sender, **kwargs):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = os.getenv('DEFAULT_ADMIN_USERNAME', 'ifugao_admin')
    password = os.getenv('DEFAULT_ADMIN_PASSWORD', 'Admin1234')
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                password=password,
                first_name='Ifugao',
                last_name='Admin',
                is_staff=True,
                is_personnel=False,
                must_change_password=True,
            )
    except DatabaseError:
        pass


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)

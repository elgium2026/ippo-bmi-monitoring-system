from django.apps import AppConfig
from django.db.utils import OperationalError

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            if not User.objects.filter(username='ifugao_admin').exists():
                admin = User.objects.create_user(
                    username='ifugao_admin',
                    password='Admin1234',
                    first_name='Ifugao',
                    last_name='Admin',
                    is_staff=True,
                    is_personnel=False,
                    must_change_password=True,
                )
                admin.save()
        except OperationalError:
            pass

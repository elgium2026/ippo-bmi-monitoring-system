from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginHistory

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Personnel data', {
            'fields': (
                'rank', 'rank_classification', 'qualifier', 'birthdate', 'unit', 'unit_other',
                'sex', 'weight_kg', 'height_cm', 'waist_cm', 'hip_cm', 'wrist_cm',
                'must_change_password', 'admin_totp_secret', 'is_personnel',
            )
        }),
    )

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('username', 'action', 'timestamp', 'success')
    list_filter = ('success',)
    search_fields = ('username', 'action')

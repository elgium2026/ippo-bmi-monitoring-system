import re
from django.core.exceptions import ValidationError

PASSWORD_PATTERN = re.compile(r'^[A-Za-z0-9]+$')

def validate_personnel_password(password: str):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not PASSWORD_PATTERN.match(password):
        raise ValidationError('Password can only contain letters and numbers. No special characters allowed.')
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if sum(char.islower() for char in password) < 2:
        raise ValidationError('Password must contain at least two lowercase letters.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit.')

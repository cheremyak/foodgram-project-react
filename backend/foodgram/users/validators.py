from django.core.exceptions import ValidationError


def validate_username(data):
    if data.lower() == "me":
        raise ValidationError(
            'Использовать имя me запрещено'
        )

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(data):
    if data.lower() == "me":
        raise ValidationError(
            'Использовать имя me запрещено'
        )


class NamesValidator(RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z -]+$'
    message = (
        'Введите правильное имя. Оно должно включать только буквы, '
        'пробел и дефис.'
    )
    flags = 0

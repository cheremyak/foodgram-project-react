from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


EN_RU_LETTERS_ONLY = RegexValidator(
    '[A-zА-яЁё]',
    'Допустимы только буквы кириллицы и латиницы'
)


def validate_username(data):
    if data.lower() == "me":
        raise ValidationError(
            'Использовать имя me запрещено'
        )

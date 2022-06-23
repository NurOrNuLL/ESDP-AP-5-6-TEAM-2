from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class OwnValidator(BaseValidator):
    def int_latin_letter_validator(value):
        allowed_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
        for symbol in value:
            if symbol.upper() not in allowed_symbols:
                raise ValidationError("Для ввода госномера доступны только цифры и латинские буквы")
        return value

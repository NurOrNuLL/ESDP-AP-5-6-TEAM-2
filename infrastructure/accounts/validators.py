import re

from django.core.exceptions import ValidationError


def number_validate(password):
    if not re.findall('\d', password):
        raise ValidationError("Пароль должен содержать не менее 1 цифры от 0 до 9.")


def uppercase_validate(password):
    if not re.findall('[A-Z]', password):
        raise ValidationError("Пароль должен содержать как минимум 1 заглавную букву, A-Z.")


def symbol_validate(password):
    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        raise ValidationError("Пароль должен содержать не менее 1 символа: " + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")


def len_validate(password):
    if len(password) < 10:
        raise ValidationError('Пароль должен содержать не менее 12 символов')

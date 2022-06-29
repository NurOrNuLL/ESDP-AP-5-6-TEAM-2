import datetime
from django.core.exceptions import ValidationError
import re
from operator import add, mul
from functools import reduce
from typing import List


def birthdate_validator(date: datetime.date) -> None:

    if date > datetime.date.today() or datetime.date.today().year - date.year > 99:
        raise ValidationError(f'Укажите дату в диапазоне от {datetime.date.today().year - 99} до \
        текущего дня {datetime.date.today().year} года!')


def multiply(iin: str, weights: List[int]) -> int:
    result = reduce(
        add,
        map(lambda i: mul(*i), zip(map(int, iin), weights))
    )
    return result


def validate_iin(iin: str) -> bool:
    if not re.match(r'[0-9]{12}', iin):
        return False
    w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    w2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
    check_sum = multiply(iin, w1) % 11
    print(multiply(iin, w1) % 11)
    if check_sum == 10:
        check_sum = multiply(iin, w2) % 11
    if check_sum != int(iin[-1]):
        raise ValidationError("Введите корректный ИИН. ")
    return True


def latin_validate(name):
    if re.search('[a-zA-Z]', name):
        raise ValidationError("Имя должен содержать только кирилицу. ")


def latin_surname_validate(surname):
    if re.search('[a-zA-Z]', surname):
        raise ValidationError("Фамилия должна содержать только кирилицу. ")


def number_validate(name):
    if re.match(r'[0-9]{11}', name):
        raise ValidationError("В это поле нельзя вводить цифру. ")


def number_surname_validate(surname):
    if re.match(r'[0-9]{11}', surname):
        raise ValidationError("В это поле нельзя вводить цифру. ")


def len_phone_validate(phone):
    if len(phone) < 11:
        raise ValidationError(f'Телефон должен содержать 11 символов. Вы ввели {len(phone)}. ')

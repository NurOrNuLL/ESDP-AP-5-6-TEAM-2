import django
from django.core.validators import BaseValidator
import jsonschema
from django.core.exceptions import ValidationError
import re
from operator import add, mul
from functools import reduce
from typing import List


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError:
            raise django.core.exceptions.ValidationError(
                '%(value)s не более 100 символов для Имени и не более 150 символов для Комментария для доверенного лица', params={'value': value}
            )


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
        raise ValidationError("Введите корректный ИИН")
    return True

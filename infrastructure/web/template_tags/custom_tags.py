from django.template.defaulttags import register
from typing import Any


@register.filter
def get_item(dictionary: str, key: str) -> Any:
    return dictionary.get(key)

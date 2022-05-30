from django.template.defaulttags import register
from typing import Any
import json

@register.filter
def get_item(dictionary:str, key:str) -> Any:
    return dictionary.get(key)

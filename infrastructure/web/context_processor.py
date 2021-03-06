import os
from typing import Dict
from django.http import HttpRequest


def env_debug_context(request: HttpRequest) -> Dict[str, bool]:
    return {'DEBUG': os.environ.get('DEBUG')}

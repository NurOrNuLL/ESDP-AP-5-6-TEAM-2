import datetime
from django.core.exceptions import ValidationError

def birthdate_validator(date: datetime.date) -> None:

    if date > datetime.date.today() or datetime.date.today().year - date.year > 99:
        raise ValidationError(f'Укажите дату в диапазоне от {datetime.date.today().year - 99} до текущего дня {datetime.date.today().year} года!')

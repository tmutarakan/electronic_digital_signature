from datetime import date
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


def validate_birthdate(value):
    if value > date.today() - relativedelta(years=14):
        raise ValidationError("Паспорт выдаётся с 14 лет.")

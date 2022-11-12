from django.utils import timezone
from django.core import exceptions


class DateValidator:

    @staticmethod
    def date_validator(date: str) -> str:
        now_date = timezone.now().date()
        if date > now_date:
            raise exceptions.ValidationError('Date must not be in the future')
        return date
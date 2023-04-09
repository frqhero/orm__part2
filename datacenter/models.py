import re

from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_entered_at(self):
        entered_at = self.entered_at.strftime('%d <%m> %Y г. %H:%M')
        pattern = r'<([^<>]+)>'
        match = re.search(pattern, entered_at)
        month_number = match.group(1)
        months_list = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]
        newvalue = months_list[int(month_number) - 1]
        oldvalue = f'<{month_number}>'
        return entered_at.replace(oldvalue, newvalue)

    def format_duration(self, timedelta):
        return str(timedelta)[:5]

    def get_duration(self):
        now = timezone.localtime()
        then = self.entered_at
        return self.format_duration(now - then)

import datetime
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
                if self.leaved_at
                else 'not leaved'
            ),
        )

    def get_entered_at(self):
        entered_at = timezone.localtime(self.entered_at).strftime(
            '%d <%m> %Y г. %H:%M'
        )
        pattern = r'<([^<>]+)>'
        match = re.search(pattern, entered_at)
        month_number = match.group(1)
        months_names = [
            'января',
            'февраля',
            'марта',
            'апреля',
            'мая',
            'июня',
            'июля',
            'августа',
            'сентября',
            'октября',
            'ноября',
            'декабря',
        ]
        month_name = months_names[int(month_number) - 1]
        month_number_with_brackets = f'<{month_number}>'
        return entered_at.replace(month_number_with_brackets, month_name)

    def get_time_spent(self):
        entered_at = timezone.localtime(self.entered_at)
        leaved_at_or_now = (
            timezone.localtime(self.leaved_at)
            if self.leaved_at
            else timezone.localtime()
        )
        return leaved_at_or_now - entered_at

    def format_duration(self, timedelta):
        hours, minutes = divmod(timedelta.total_seconds(), 3600)
        minutes //= 60
        hours, minutes = int(hours), int(minutes)
        return f'{hours:02d}:{minutes:02d}'

    def get_duration(self):
        time_spent = self.get_time_spent()
        return self.format_duration(time_spent)

    def is_long(self, minutes=60):
        time_spent = self.get_time_spent()
        return time_spent.total_seconds() > minutes * 60

import datetime
import pytz
import re

from django.db import models
from django.utils import timezone

from project.settings import TIME_ZONE


def convert_datetime_tz_plus_3(datetime_to_convert):
    msc_tz = pytz.timezone(TIME_ZONE)
    return datetime_to_convert.astimezone(msc_tz)


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
        timezone = pytz.timezone(TIME_ZONE)
        entered_at = self.entered_at.astimezone(timezone).strftime(
            '%d <%m> %Y г. %H:%M'
        )
        pattern = r'<([^<>]+)>'
        match = re.search(pattern, entered_at)
        month_number = match.group(1)
        months_list = [
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
        newvalue = months_list[int(month_number) - 1]
        oldvalue = f'<{month_number}>'
        return entered_at.replace(oldvalue, newvalue)

    def format_duration(self, timedelta):
        random_day = datetime.datetime(1970, 1, 1) + timedelta
        return random_day.strftime('%H:%M')

    def get_duration(self):
        entered_at = convert_datetime_tz_plus_3(self.entered_at)
        leaved_at = (
            convert_datetime_tz_plus_3(self.leaved_at)
            if self.leaved_at
            else timezone.localtime()
        )
        return self.format_duration(leaved_at - entered_at)

    def is_long(self, minutes=60):
        entered_at = convert_datetime_tz_plus_3(self.entered_at)
        leaved_at = (
            convert_datetime_tz_plus_3(self.leaved_at)
            if self.leaved_at
            else timezone.localtime()
        )
        timedelta = leaved_at - entered_at
        return timedelta.total_seconds() > minutes * 60

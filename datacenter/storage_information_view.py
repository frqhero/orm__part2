from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
import re


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []
    for visit in visits:
        non_closed_visit = {
            'who_entered': visit.passcard,
            'entered_at': visit.get_entered_at(),
            'duration': visit.get_duration()
        }
        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)

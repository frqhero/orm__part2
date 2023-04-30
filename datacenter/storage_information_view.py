from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []
    for visit in visits:
        non_closed_visit = {
            'who_entered': visit.passcard,
            'entered_at': visit.get_entered_at(),
            'duration': visit.get_duration(),
            'is_strange': visit.is_long(),
        }
        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)

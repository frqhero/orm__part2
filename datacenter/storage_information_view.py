from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    active_visits = Visit.objects.filter(leaved_at=None)
    active_visits_for_rendering = []
    for visit in active_visits:
        non_closed_visit = {
            'who_entered': visit.passcard,
            'entered_at': visit.get_entered_at(),
            'duration': visit.get_duration(),
            'is_strange': visit.is_long(),
        }
        active_visits_for_rendering.append(non_closed_visit)

    context = {
        'non_closed_visits': active_visits_for_rendering,
    }
    return render(request, 'storage_information.html', context)

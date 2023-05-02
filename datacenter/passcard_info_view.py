from django.shortcuts import get_object_or_404, render

from datacenter.models import Passcard


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = passcard.visit_set.all()
    passcard_visits_serialized = []
    for visit in passcard_visits:
        passcard_visits_serialized.append(
            {
                'entered_at': visit.get_entered_at(),
                'duration': visit.get_duration(),
                'is_strange': visit.is_long()
            },
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits_serialized
    }
    return render(request, 'passcard_info.html', context)

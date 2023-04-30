from django.shortcuts import get_object_or_404, render

from datacenter.models import Passcard


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = passcard.visit_set.all()
    this_passcard_visits = []
    for visit in visits:
        this_passcard_visits.append(
            {
                'entered_at': visit.get_entered_at(),
                'duration': visit.get_duration(),
                'is_strange': visit.is_long()
            },
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)

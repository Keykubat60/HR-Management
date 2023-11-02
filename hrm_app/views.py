from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect_to_admin(request):
    return HttpResponseRedirect(reverse('admin:index'))

from django.http import JsonResponse
from .models import Personal

def get_personal_details(request, personal_id):
    try:
        personal = Personal.objects.get(id=personal_id)
        data = {'iban': personal.iban, 'vertragsart': personal.vertragsart}
        return JsonResponse(data)
    except Personal.DoesNotExist:
        return JsonResponse({'error': 'Personal not found'}, status=404)



from rest_framework import viewsets
from .models import Personal, Abrechnung
from .serializers import PersonalSerializer

class PersonalViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer

def get_persons_not_in_month(request, month_id):
    persons_with_abrechnung = Abrechnung.objects.filter(monatsabrechnung_id=month_id).values_list('personal', flat=True)
    persons_without_abrechnung = Personal.objects.exclude(id__in=persons_with_abrechnung).filter(status='aktiv').values(
        'name', 'nachname', 'personalnummer')
    return JsonResponse({'persons': list(persons_without_abrechnung)})



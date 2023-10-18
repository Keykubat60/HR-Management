from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect_to_admin(request):
    return HttpResponseRedirect(reverse('admin:index'))
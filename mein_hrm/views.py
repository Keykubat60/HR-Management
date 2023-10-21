from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect_to_admin(request):
    if 'media' not in request.path:
        return HttpResponseRedirect(reverse('admin:index'))
    return HttpResponseRedirect(request.path)


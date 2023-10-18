from django.contrib import admin
from django.urls import path
from django.conf import settings  # <--- Hinzufügen
from django.conf.urls.static import static  # <--- Hinzufügen
from . import views  # Stellen Sie sicher, dass Ihre views importiert sind

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_admin),  # Weiterleitung von der Hauptseite zur Admin-Seite
]

if settings.DEBUG is False:  # Wenn DEBUG ist False, dienen Sie statische Dateien durch Django
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

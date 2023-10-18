from django.contrib import admin
from django.urls import path
from . import views  # Stellen Sie sicher, dass Ihre views importiert sind

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_admin),  # Weiterleitung von der Hauptseite zur Admin-Seite
]
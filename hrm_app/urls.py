from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <--- Hinzufügen
from django.conf.urls.static import static  # <--- Hinzufügen
from . import views  # Stellen Sie sicher, dass Ihre views importiert sind
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'personal', views.PersonalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_admin),  # Weiterleitung von der Hauptseite zur Admin-Seite
    path('api/get_personal_details/<int:personal_id>/', views.get_personal_details, name='get_personal_details'),
    path('api/', include(router.urls)),

]

if settings.DEBUG is False:  # Wenn DEBUG ist False, dienen Sie statische Dateien durch Django
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
URL configuration for mein_hrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <--- Hinzufügen
from django.conf.urls.static import static  # <--- Hinzufügen
import hrm_app.views  # Stellen Sie sicher, dass Ihre views importiert sind
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'personal', hrm_app.views.PersonalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hrm_app.views.redirect_to_admin),  # Weiterleitung von der Hauptseite zur Admin-Seite
    path('api/get_personal_details/<int:personal_id>/', hrm_app.views.get_personal_details, name='get_personal_details'),
    path('api/', include(router.urls)),
    path('api/get_persons_not_in_month/<int:month_id>/', hrm_app.views.get_persons_not_in_month,
         name='get_persons_not_in_month'),

]

if settings.DEBUG is False:  # Wenn DEBUG ist False, dienen Sie statische Dateien durch Django
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
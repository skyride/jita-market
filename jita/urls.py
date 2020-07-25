from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.api import views as api_views


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


# Register API endpoints
router.register(r"v1/types", api_views.TypeV1ViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
]

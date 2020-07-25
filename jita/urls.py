from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
]

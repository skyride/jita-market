from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers

from apps.api import views as api_views
from apps.core.views import schema_view


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()


# Register API endpoints
router.register(r"v1/types", api_views.TypeV1ViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls)
]

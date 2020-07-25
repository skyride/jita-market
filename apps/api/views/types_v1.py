"""
Types v1 endpint.

This endpoint returns a wide set of information about a type. Ideal for
providing a details page about a type.
"""

from rest_framework import serializers, viewsets

from apps.sde.models import Type
from apps.pricing.models import RegionPrice


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class TypeV1ViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin):
    queryset = Type.objects.filter(market_group_id__isnull=False)
    serializer_class = TypeSerializer

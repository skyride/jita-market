"""
Types v1 endpint.

This endpoint returns a wide set of information about a type. Ideal for
providing a details page about a type.
"""
from typing import Dict

from rest_framework import serializers, viewsets

from apps.sde.models import Type
from apps.pricing.models import RegionPrice


class RegionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionPrice
        exclude = ["id", "region", "type", "created"]


class TypeListSerializer(serializers.ModelSerializer):
    """
    Basic serializer for list view.
    """
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = ["id", "name", "volume", "group_id", "market_group_id", "icon_url", "prices"]

    def get_prices(self, obj: Type) -> Dict[int, Dict[str, int]]:
        """
        Return a dict of prices that only has the forge in it.
        """
        # Our query already prefetches the region pricing data. Iterating over
        # it here manually keeps our list endpoint to 2 queries instead of n+1
        # on the list endpoint.
        region_id = 10000002
        for region_price in obj.prices.all():
            if region_price.region_id == region_id:
                return {
                    region_id: RegionPriceSerializer(region_price).data}


class TypeV1ViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin):
    queryset = (Type.objects
        .filter(
            market_group_id__isnull=False)
        .prefetch_related("prices")
        .order_by("id"))

    def get_serializer_class(self):
        if self.action == "list":
            return TypeListSerializer

"""
Types v1 endpint.

This endpoint returns a wide set of information about a type. Ideal for
providing a details page about a type.
"""
from typing import Dict

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import serializers, viewsets

from apps.sde.models import Type, MarketGroup, Category, Group
from apps.pricing.models import RegionPrice


class RegionPriceSerializer(serializers.ModelSerializer):
    total_buy = serializers.SerializerMethodField()
    total_sell = serializers.SerializerMethodField()

    class Meta:
        model = RegionPrice
        exclude = ["id", "region", "type", "created"]

    def get_total_buy(self, obj: Type) -> float:
        return round(obj.average_buy * obj.buy_volume, 2)

    def get_total_sell(self, obj: Type) -> float:
        return round(obj.average_sell * obj.sell_volume, 2)


# List serializers
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


# Detail serializers
class MarketGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketGroup
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Group
        fields = "__all__"


class TypeDetailSerializer(serializers.ModelSerializer):
    """
    More detailed serializer for retrieve/detail call.
    """
    market_group = MarketGroupSerializer()
    group = GroupSerializer()
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = "__all__"

    def get_prices(self, obj: Type) -> Dict[int, Dict[str, int]]:
        """
        Return a dict of prices for every region we have data on.
        """
        return {
            region_price.region_id: RegionPriceSerializer(region_price).data
            for region_price in obj.prices.all()}


class TypeV1ViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin):
    queryset = (Type.objects
        .filter(
            market_group_id__isnull=False)
        .prefetch_related("prices")
        .order_by("id"))

    @method_decorator(cache_page(30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(30))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """Add select related for retrieve"""
        query = super().get_queryset()
        if self.action == "retrieve":
            query = query.select_related(
                "market_group",
                "group",
                "group__category")
        return query

    def get_serializer_class(self):
        if self.action == "list":
            return TypeListSerializer
        elif self.action == "retrieve":
            return TypeDetailSerializer

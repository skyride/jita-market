"""
Types v1 endpint.

This endpoint returns a wide set of information about a type. Ideal for
providing a details page about a type.
"""
from typing import Dict

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import serializers, viewsets
from drf_yasg.utils import swagger_auto_schema

from apps.sde.models import Type, MarketGroup, Category, Group
from apps.pricing.models import RegionPrice


class RegionPriceSerializer(serializers.ModelSerializer):
    total_buy = serializers.SerializerMethodField()
    total_sell = serializers.SerializerMethodField()

    class Meta:
        model = RegionPrice
        exclude = ["id", "type", "created"]

    def get_total_buy(self, obj: Type) -> float:
        return round(obj.average_buy * obj.buy_volume, 2)

    def get_total_sell(self, obj: Type) -> float:
        return round(obj.average_sell * obj.sell_volume, 2)


class RegionPriceListSerializer(serializers.ListSerializer):
    def to_representation(self, related_manager):
        objects = [
            region_price for region_price in related_manager.all()
            if region_price.region_id == 10000002]
        return super().to_representation(objects)


# List serializers
class TypeListSerializer(serializers.ModelSerializer):
    """
    Basic serializer for list view.
    """
    prices = RegionPriceListSerializer(child=RegionPriceSerializer())

    class Meta:
        model = Type
        fields = ["id", "name", "volume", "group_id", "market_group_id", "icon_url", "prices"]


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
    prices = RegionPriceSerializer(many=True)

    class Meta:
        model = Type
        fields = "__all__"


class TypeV1ViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin):
    queryset = (Type.objects
        .filter(
            market_group_id__isnull=False)
        .prefetch_related("prices")
        .order_by("id"))

    @swagger_auto_schema(
        tags=["Current Prices"],
        operation_summary="List Item types, some basic information and pricing data "
                          "for The Forge regional market")
    @method_decorator(cache_page(settings.CACHE_PERIOD))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Current Prices"],
        operation_summary="Provides more detailed information and pricing data for "
                          "every region for a single type")
    @method_decorator(cache_page(settings.CACHE_PERIOD))
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

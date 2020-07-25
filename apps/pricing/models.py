from django.db import models

from apps.sde.models import Region, Type


class RegionPrice(models.Model):
    """
    A summary of current pricing information for a type in a region.
    """
    region = models.ForeignKey(Region,
        related_name="prices", on_delete=models.CASCADE)
    type = models.ForeignKey(Type,
        related_name="prices", on_delete=models.CASCADE)

    max_buy = models.FloatField(default=0)
    max_sell = models.FloatField(default=0)
    min_buy = models.FloatField(default=0)
    min_sell = models.FloatField(default=0)
    average_buy = models.FloatField(default=0)
    average_sell = models.FloatField(default=0)
    percentile_buy = models.FloatField(default=0)
    percentile_sell = models.FloatField(default=0)
    buy_volume = models.BigIntegerField(default=0)
    sell_volume = models.BigIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("region", "type")
        ordering = ["id"]

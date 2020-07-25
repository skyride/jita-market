import requests
import ujson

from django.apps import AppConfig


class EsiConfig(AppConfig):
    name = 'esi'

    def ready(self):
        requests.models.json = ujson

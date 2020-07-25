import ujson

from rest_framework.renderers import BaseRenderer


class UJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.
    Uses the blazing-fast ujson library for serialization.
    """

    media_type = 'application/json'
    format = 'json'
    charset = "utf-8"

    def render(self, data, *args, **kwargs):

        if data is None:
            return ""

        return ujson.dumps(data)

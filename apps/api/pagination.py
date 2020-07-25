from rest_framework import pagination


class LimitedLimitOffsetPagination(pagination.LimitOffsetPagination):
    max_limit = 100

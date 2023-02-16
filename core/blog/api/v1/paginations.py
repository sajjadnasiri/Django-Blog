from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class PostPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total posts', self.page.paginator.count),
            ("total pages", self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('prev', self.get_previous_link()),
            ('results', data),
        ]))


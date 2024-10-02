from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class LearningNotePagination(PageNumberPagination):
    page_size = 5  # Number of learning notes per page
    page_size_query_param = 'page_size'  # Allow overriding the default page size
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of learning notes
            'total_pages': self.page.paginator.num_pages,  # Total number of pages
            'current_page': self.page.number,  # Current page number
            # Next page number
            'next_page': self.page.next_page_number() if self.page.has_next() else None,
            # Previous page number
            'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
            'results': data  # Paginated learning notes
        })

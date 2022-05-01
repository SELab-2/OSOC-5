
class PaginationMixin(object):
    """
    Pagination mixin which implements methods used to paginate non-generic Views.
    """
    @property
    def paginator(self):
        """
        Get the paginator associated with the view (or None).
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return one page (or None).
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style Response object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

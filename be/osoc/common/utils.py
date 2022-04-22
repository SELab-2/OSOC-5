"""
Utility functions
"""
from django.utils.http import urlencode
from rest_framework.reverse import reverse


def strip_and_lower_email(email):
    return email.strip().lower()

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    """
    https://gist.github.com/benbacardi/227f924ec1d9bedd242b
    Custom reverse to handle query strings.
    Usage:
        reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

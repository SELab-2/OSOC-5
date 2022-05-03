"""
Utilities.
"""
from django.utils import timezone
from django.utils.http import urlencode
from rest_framework.reverse import reverse


def assert_or_raise(check, mesg, error=ValueError):
    """
    If check fails, raise error with message.
    """
    if not check:
        raise error(mesg)

def get_nested(dictionary, default, *keys):
    """
    Get a dictionary but nested; returning the default at the first missing key.
    """
    val = dictionary
    for key in keys:
        val = val.get(key, default)
        if val == default:
            return default
    return val

def strip_and_lower_email(email):
    """
    Strip email and transform it to lowercase.
    """
    return email.strip().lower()

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, query_kwargs=None):
    """
    https://gist.github.com/benbacardi/227f924ec1d9bedd242b
    Custom reverse to handle query strings.
    Usage:
        reverse_querystring("student-list", query_kwargs=({"on_project": "true"}))
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs)
    if query_kwargs:
        return f"{base_url}?{urlencode(query_kwargs)}"
    return base_url

def string_to_datetime_tz(string):
    """
    convert a string to a timezone aware datetime object
    the string must be in one of the following formats:
    - "%Y-%m-%dT%H:%M:%S"
    - "%Y-%m-%d"
    """
    try:
        return timezone.make_aware(timezone.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return timezone.make_aware(timezone.datetime.strptime(string, "%Y-%m-%d"))

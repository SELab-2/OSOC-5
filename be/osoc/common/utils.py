"""
Utilities.
"""
import csv
from io import BytesIO, StringIO
from zipfile import ZIP_DEFLATED, ZipFile
from django.http import FileResponse, HttpResponse
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

def export_to_csv(queryset, filename, serializer):
    """
    export a queryset to a csv StringIO object
    """
    csv_data = StringIO()
    writer = csv.writer(csv_data)

    # write header
    writer.writerow(serializer.Meta.fields)
    # write objects
    for item in queryset:
        writer.writerow(serializer(item).data.values())

    csv_data.name = filename
    csv_data.seek(0)
    return csv_data

def create_zipfile_response(filename, files):
    """
    create a zipfile that contains given csv files
    returns a HTTP File Reponse with zip file attachment
    """
    zipped_file = BytesIO()
    with ZipFile(zipped_file, 'w', ZIP_DEFLATED) as zipped:
        for file in files:
            zipped.writestr(f'{file.name}.csv', file.read())
    zipped_file.seek(0)
    return FileResponse(zipped_file, content_type='application/zip',
        headers={'Content-Disposition': f'attachment; filename="{filename}.zip"'})

def create_csv_response(file):
    """
    create a csv file
    returns a HTTP File Response with the csv as an attachment
    """
    return HttpResponse(file, content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{file.name}.csv"'})

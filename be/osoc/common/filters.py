"""
Filters used in views.py
"""
from rest_framework import filters

from .models import Project, Student

class OnProjectFilter(filters.BaseFilterBackend):
    """
    filters students that are assigned/suggested to a project
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('on_project') is not None:
            suggested_students = Student.objects.none()
            for project in Project.objects.all():
                suggested_students |= project.suggested_students.all()
            subquery = suggested_students.distinct()
            return queryset.filter(id__in=subquery.values('id'))
        return queryset

class SuggestedByUserFilter(filters.BaseFilterBackend):
    """
    filters students that have a suggestion made by the current user
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('suggested_by_user') is not None:
            return queryset.filter(suggestions__id=request.user.id)
        return queryset
"""
Filters used in views.py
"""

from django.forms import ValidationError
from rest_framework import filters
from .models import Project, Student, Suggestion

true_strings = ['true', '1', 'yes', 't', 'y']
false_strings = ['false', '0', 'no', 'f', 'n']

class StudentOnProjectFilter(filters.BaseFilterBackend):
    """
    filters students that are assigned/suggested to a project
    query parameter 'on_project' should be included in the url
    """
    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('on_project')
        if param is not None:
            suggested_students = Student.objects.none()
            for project in Project.objects.all():
                suggested_students |= project.suggested_students.all()  # union

            # subquery is needed because filtering is not possible on a union of queries for some reason
            subquery = suggested_students.distinct()
            if param.lower() in true_strings:
                return queryset.filter(id__in=subquery.values('id'))
            elif param.lower() in false_strings:
                return queryset.exclude(id__in=subquery.values('id'))
        return queryset


class StudentSuggestedByUserFilter(filters.BaseFilterBackend):
    """
    filters students that have a suggestion made by the current user
    query parameter 'suggested_by_user' should be included in the url
    """
    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('suggested_by_user')
        if param is not None:
            if param.lower() in true_strings:
                return queryset.filter(suggestions__id=request.user.id)
            elif param.lower() in false_strings:
                return queryset.exclude(suggestions__id=request.user.id)
        return queryset


class StudentFinalDecisionFilter(filters.BaseFilterBackend):
    """
    filters students based on final decision
    query parameter 'suggestion' should be one of ['yes', 'no', 'maybe', 'none'] or ['0', '1', '2', '3']
    """
    param2enum = {'yes': Suggestion.Suggestion.YES, 
                  'no': Suggestion.Suggestion.NO, 
                  'maybe': Suggestion.Suggestion.MAYBE,
                  '0': Suggestion.Suggestion.YES, 
                  '1': Suggestion.Suggestion.NO, 
                  '2': Suggestion.Suggestion.MAYBE}

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('suggestion')
        if param is not None:
            if param.lower() in self.param2enum.keys():
                return queryset.filter(final_decision__suggestion=self.param2enum[param])
            if param.lower() in ['none', '3']:
                return queryset.filter(final_decision=None)
        return queryset


class EmailDateTimeFilter(filters.BaseFilterBackend):
    """
    filters emails based on their send date and time
    query parameter should be one of: ['?date=', '?before=', '?after=']
    """
    def filter_queryset(self, request, queryset, view):
        try:
            if (date := request.query_params.get('date')) is not None:
                return queryset.filter(time__date=date)
            if (before := request.query_params.get('before')) is not None:
                queryset = queryset.filter(time__lt=before)
            if (after := request.query_params.get('after')) is not None:
                queryset = queryset.filter(time__gt=after)
        except ValidationError:
            # return default queryset when a validationerror is raised
            pass
        return queryset
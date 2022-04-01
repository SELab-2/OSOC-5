"""
Filters used in views.py
"""
from rest_framework import filters
from .models import Project, Student, Suggestion

class OnProjectFilter(filters.BaseFilterBackend):
    """
    filters students that are assigned/suggested to a project
    query parameter 'on_project' should be included in the url
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('on_project') is not None:
            suggested_students = Student.objects.none()
            for project in Project.objects.all():
                suggested_students |= project.suggested_students.all()  # union

            # subquery is needed because filtering is not possible on a union of queries for some reason
            subquery = suggested_students.distinct()
            return queryset.filter(id__in=subquery.values('id'))
        return queryset

class SuggestedByUserFilter(filters.BaseFilterBackend):
    """
    filters students that have a suggestion made by the current user
    query parameter 'suggested_by_user' should be included in the url
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('suggested_by_user') is not None:
            return queryset.filter(suggestions__id=request.user.id)
        return queryset

class FinalDecisionFilter(filters.BaseFilterBackend):
    """
    filters students based on final decision
    query parameter 'suggestion' should be one of ['yes', 'no', 'maybe', 'none']
    """
    param2enum = {'yes': Suggestion.Suggestion.YES, 
                  'no': Suggestion.Suggestion.NO, 
                  'maybe': Suggestion.Suggestion.MAYBE}

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('suggestion')
        if param is not None:
            if param in ['yes', 'no', 'maybe']:
                return queryset.filter(final_decision__suggestion=self.param2enum[param])
            if param == 'none':
                return queryset.filter(final_decision=None)
        return queryset

"""
Filters used in views.py
"""
from rest_framework import filters
from .models import Project, Student, Suggestion

class StudentOnProjectFilter(filters.BaseFilterBackend):
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


class StudentSuggestedByUserFilter(filters.BaseFilterBackend):
    """
    filters students that have a suggestion made by the current user
    query parameter 'suggested_by_user' should be included in the url
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('suggested_by_user') is not None:
            return queryset.filter(suggestions__id=request.user.id)
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
            if param in self.param2enum.keys():
                return queryset.filter(final_decision__suggestion=self.param2enum[param])
            if param in ['none', '3']:
                return queryset.filter(final_decision=None)
        return queryset


class EmailDateTimeFilter(filters.BaseFilterBackend):
    """
    filters emails based on their send date and time
    query parameter should be one of: ['?date=', '?before=', '?after=']
    """
    def filter_queryset(self, request, queryset, view):
        if (date := request.query_params.get('date')) is not None:
            return queryset.filter(time__date=date)
        if (before := request.query_params.get('before')) is not None:
            queryset = queryset.filter(time__lt=before)
        if (after := request.query_params.get('after')) is not None:
            queryset = queryset.filter(time__gt=after)
        return queryset
"""
Register database models to Django admin panel.
"""
from django.contrib import admin

from .models import Coach, Project, Skill, Student, Suggestion

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    StudentAdmin; Just display first and last name on the change list page of the admin.
    """
    list_display = ('first_name', 'last_name',)

admin.site.register(Coach)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Suggestion)

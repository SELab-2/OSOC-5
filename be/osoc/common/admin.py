from django.contrib import admin

from .models import Coach, Project, Skill, Student, Suggestion


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)


admin.site.register(Coach)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Suggestion)

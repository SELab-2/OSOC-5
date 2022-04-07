"""
Register database models to Django admin panel.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach, Project, ProjectSuggestion, RequiredSkills, Skill, Student, Suggestion
from .forms import UserAdminChangeForm, UserAdminCreationForm

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    StudentAdmin; Just display first and last name on the change list page of the admin.
    """
    list_display = ('first_name', 'last_name',)

class CustomUserAdmin(UserAdmin):
    exclude = ('username',)
    ordering = ('email',)
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_active', 'last_email_sent')}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password','first_name','last_name')}
        ),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )

admin.site.register(Coach, CustomUserAdmin)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Suggestion)
admin.site.register(RequiredSkills)
admin.site.register(ProjectSuggestion)

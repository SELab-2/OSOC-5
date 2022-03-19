from django.contrib import admin

from .models import Coach, GithubUser, Project, Skill, Student, Suggestion
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Coach


@admin.register(Coach)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Coach
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (('Personal info'), {'fields': ('first_name', 'last_name')})
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    list_display = ('coach', 'login')

admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Suggestion)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

@admin.register(models.FieldValidationDate)
class DateAdmin(admin.ModelAdmin):
    list_display = 'field', 'date'


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):
    list_display = 'user', 'action', 'date'
    list_filter = 'user', 'date'


@admin.register(models.SmallInteger)
class SmallIntegerAdmin(admin.ModelAdmin):
    list_display = 'name', 'value'


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = 'name', 'captain', 'is_full', 'confirmed'
    fieldsets = (
        (None, {'fields': ('id', 'name', 'github_link', 'users',
                           'is_full', 'confirmed')}),
        ('Project info', {'fields': ('project_name', 'project_description',
                                     'technologies')}),
        ('Additional info', {'fields': ('ready', 'is_confirmed',
                                        'date_joined')}),
    )
    readonly_fields = 'is_confirmed', 'id', 'date_joined'
    list_filter = 'is_full', 'confirmed'
    ordering = 'date_joined',
    filter_horizontal = 'users', 'technologies'

    def captain(self, obj):
        return models.User.objects.get(id=obj.captain)

    captain.short_description = 'captain'


admin.site.register(models.Technology)


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'avatar',
                                      'form', 'phone', 'discord_id')}),
        ('Additional info', {
            'fields': ('tshirt_size', 'food_preferences', 'is_online',
                       'alergies', 'technologies', 'is_captain'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'email', 'name', 'form', 'phone', 'tshirt_size',
                    'discord_id', 'is_active', 'has_team')
    list_filter = ('is_active', 'is_staff', 'tshirt_size', 'form')
    ordering = 'id',
    readonly_fields = 'id',

    def name(self, obj):
        return obj.get_full_name()

    name.short_description = 'name'

    def has_team(self, obj):
        return bool(obj.team_set.count())

    has_team.is_boolean = True
    has_team.short_description = 'has_team'


class RegisteredUser(models.User):
    class Meta:
        proxy = True


@admin.register(RegisteredUser)
class RegisteredUserAdmin(UserAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        ids = set()
        for user in queryset:
            if user.has_team:
                ids.add(user.id)
        return queryset.filter(id__in=ids)

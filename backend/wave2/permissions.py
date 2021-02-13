from datetime import date

from rest_framework import permissions

from wave2.models import FieldValidationDate


class UserPermissions(permissions.BasePermission):
    """
    allowed methods:

    unregistered user - get, post
    registered user - get, put*, delete*
    """
    def has_permission(self, request, view):
        return True  # AllowAny

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == 'leave_team' and team_not_editable():
            return False

        if request.user == obj:
            return True

        return False


class TeamPermissions(permissions.BasePermission):
    """
    allowed methods:

    user: - get
    registered user: - ..., post
    captain: - ..., put*, delete*
    """
    def has_permission(self, request, view):
        if (view.action == 'change_captain' or
            request.method in permissions.SAFE_METHODS):
            return True

        if request.method == 'DELETE' and team_not_editable():
            return False
            
        if request.method == 'POST' and request.user.team_set.count():
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == 'change_captain' and team_not_editable():
            return False

        if (request.user.is_captain and request.user.team_set.first() == obj
            or request.method in permissions.SAFE_METHODS):
            return True

        return False


def team_not_editable():
    return (
        FieldValidationDate.objects.get(field='team_editable').date <
        date.today()
    )

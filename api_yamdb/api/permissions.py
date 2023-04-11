from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin or request.user.is_superuser
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return request.user.is_admin


class NotUserRoleOrIsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser


class IsModeratorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdminOrSuperuser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return request.user.is_superuser
        if request.user.is_authenticated:
            return request.user.is_admin


class IsAuthorOrModer(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_moderator)
                )
        )


class AuthorOrHasRoleOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )

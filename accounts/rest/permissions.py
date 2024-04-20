from rest_framework import permissions


class SuperAdminPermission(permissions.BasePermission):
    message = 'You are not allowed'

    def has_permission(self, request, view):
        if request.user.is_super_admin:
            return True
        return False


class AdminPermission(permissions.BasePermission):
    message = 'You are not allowed'

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        return False


class CustomerPermission(permissions.BasePermission):
    message = 'You are not allowed'

    def has_permission(self, request, view):
        if request.user.is_customer:
            return True
        return False


class ShopAdminPermission(permissions.BasePermission):
    message = 'You are not allowed'

    def has_permission(self, request, view):
        if request.user.is_shop_admin:
            return True
        return False



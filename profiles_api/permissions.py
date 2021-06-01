from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
	"""
	Takes a user and a group name, and returns 'True' if the user is in that group.
	"""
	try:
		return Group.objects.get(name=group_name).users_set.filter(id=user.id).exists()
	except Group.DoesNotExist:
		return None


def _has_group_permission(user, required_groups):
	return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsAuthenticatedUser(permissions.BasePermission):

	def __init__(self, required_groups=None):
		self.required_groups = required_groups

	def has_permission(self, request, view):
		has_group_permission = _has_group_permission(request.user, self.required_groups)
		return request.user and has_group_permission

	def has_object_permission(self, request, view, obj):
		has_group_permission = _has_group_permission(request.user, self.required_groups)
		return request.user and has_group_permission


class IsAdmin(IsAuthenticatedUser):
	def __init__(self):
		super(IsAdmin, self).__init__(required_groups=['admin'])


class IsAdminOrManager(IsAuthenticatedUser):
	def __init__(self):
		super(IsAdminOrManager, self).__init__(required_groups=['admin', 'manager'])


class IsAdminOrManagerOrUser(IsAuthenticatedUser):
	def __init__(self):
		super(IsAdminOrManagerOrUser, self).__init__(required_groups=['admin', 'manager', 'user'])

#
# class IsAdmin(permissions.BasePermission):
# 	# group_name for super admin
# 	required_groups = ['admin']
#
# 	def has_permission(self, request, view):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission
#
# 	def has_object_permission(self, request, view, obj):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission
#
#
# class IsAdminOrManager(permissions.BasePermission):
# 	required_groups = ['admin', 'manager']
#
# 	def has_permission(self, request, view):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission
#
# 	def has_object_permission(self, request, view, obj):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission
#
#
# class IsAdminOrManagerOrUser(permissions.BasePermission):
# 	required_groups = ['admin', 'manager', 'user']
#
# 	def has_permission(self, request, view):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission
#
# 	def has_object_permission(self, request, view, obj):
# 		has_group_permission = _has_group_permission(request.user, self.required_groups)
# 		return request.user and has_group_permission

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions


ERROR_MESSAGE = 'You must be the owner of this object.'

class IsOwnerOrReadOnly(BasePermission):
	message = ERROR_MESSAGE
	my_safe_method = ['GET']

	def has_permission(self, request, view):
		if request.method in self.my_safe_method:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		elif obj.writer != request.user:
			raise exceptions.PermissionDenied(detail=ERROR_MESSAGE)
		return True


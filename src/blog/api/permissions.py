from rest_framework.permissions import BasePermission
from rest_framework import exceptions


ERROR_MESSAGE = 'You must be the owner of this object.'

class IsOwnerOrReadOnly(BasePermission):
	message = ERROR_MESSAGE
	def has_object_permission(self, request, view, obj):
		if obj.writer != request.user:
			raise exceptions.PermissionDenied(detail=ERROR_MESSAGE)
		return True


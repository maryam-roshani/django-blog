from rest_framework.pagination import (
		LimitOffsetPagination,
		PageNumberPagination
	)


class PostLimitOffsetPagination(LimitOffsetPagination):
	max_limit = 10
	default_limit = 1


class PostPageNumberPagination(PageNumberPagination):
	page_size = 1
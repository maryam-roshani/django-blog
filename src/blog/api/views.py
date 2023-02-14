from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView, 
	RetrieveAPIView,
	UpdateAPIView,
	)

from blog.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer

	def perform_create(self, serializer):
		serializer.save(writer=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	# lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'


class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer


class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer


from rest_framework.serializers import ModelSerializer
from blog.models import Post


class PostListSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'topic',
			'title',
			'text',
		]


class PostDetailSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'topic',
			'title',
			'text',
			'slug',
		]

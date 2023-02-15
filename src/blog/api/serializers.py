from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from blog.models import Post


class PostListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='blog-api:detail',
		)
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'topic',
			'title',
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


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			# 'id',
			'topic',
			'title',
			'text',
			# 'slug',
		]

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	text = models.TextField(null=True, blank=True)
	picture = models.ImageField(blank=True, upload_to='images')
	date_created = models.DateTimeField(auto_now=True)
	date_updated = models.DateTimeField(auto_now_add=True)
	writer = models.ForeignKey(User, on_delete=models.CASCADE)
	slug = models.SlugField()

	def __str__(self):
		return self.title


class Comment(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	body = models.TextField()
	date_created = models.DateTimeField(auto_now=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.body[:20]
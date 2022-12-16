from django import forms
from .models import Comment, User, Post
# from django.contrib.auth.forms import UserCreationForm



# class MyUserCreationForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ['name', 'username', 'email', 'password1', 'password2']
			

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['avatar', 'name', 'username', 'email', 'bio']


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['topic', 'title', 'text', 'picture']

	def clean(self):
		data = self.cleaned_data
		title = data.get("title")
		qs = Post.objects.filter(title__icontains=title)
		if qs.exists():
			self.add_error("title", f"\"{title}\" is already in use. Please pick another title.")
		return data


from django.shortcuts import render
from .models import Post
from .forms import CommentForm

# Create your views here.
def home(request):
	posts = Post.objects.all()
	tost = Post.objects.get(pk=1)
	context = {'posts': posts, 'tost': tost}
	return render(request, 'home.html', context)

def post_detail(request, pk):
	post = Post.objects.get(slug=pk)
	comments = post.comments.set_all()
	new_comment = None

	if request.method == 'POST':
		form = CommentForm(request.post)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.commenter = request.user
			new_comment.save()
	else :
		form = CommentForm()
	context = {'post':post, 'comments':comments, 'form':form}
	return render(request, 'blog/blog_detail.html', context)



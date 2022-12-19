from django.shortcuts import render, redirect
from .models import Post, Comment, User, Message, MessageLike, CommentLike
from .forms import CommentForm, PostForm, UserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def home(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''
	posts = Post.objects.all()
	mosts = Post.objects.filter(
		Q(title__icontains=q)|
		Q(topic__icontains=q)|
		Q(text__icontains=q))
	tost = {}
	if posts :
		tost = posts.latest('id')
		if q :
			if mosts:
				tost = {}
				posts = mosts
			else:
				tost = {}
				messages.error(request, 'nothing is found')

	context = {'posts': posts, 'tost': tost}
	return render(request, 'home.html', context)


@login_required(login_url='accounts/login')
def post_detail(request, slug):
	post = Post.objects.get(slug=slug)
	post_messages = post.messages.all()

	for message in post_messages :
		bike = MessageLike.objects.filter(
		Q(user = request.user) & 
		Q(message = message)
		)
		message.like = bool(bike)

	if request.method == 'POST':
		if request.user.is_authenticated:
			message = Message.objects.create(
				sender=request.user,
				post = post,
				body=request.POST.get('body'))
			return redirect('blog:detail', slug=post.slug)
		else:
			messages.error(request, 'you are not allowed to send message')
	
	context = {'post':post, 'post_messages':post_messages}
	return render(request, 'blog/blog_detail.html', context)


@login_required(login_url='accounts/login')
def reply_create_view(request, pk):
	message = Message.objects.get(id=pk)
	post = message.post
	form = CommentForm(initial={'body':'@'+ message.sender.username})
	if request.method == "POST" :
		comment = Comment.objects.create(
			commenter=request.user,
			user = message.sender,
			post = post,
			message = message,
			body=request.POST.get('body'))
		message.replied = True
		message.save()
		return redirect('blog:detail', slug=post.slug)
	context = {'form' : form }
	return render(request, 'blog/commentCreate.html', context )


def show_reply_view(request, pk):
	message = Message.objects.get(id=pk)
	owner = message.sender
	post = message.post
	comments = Comment.objects.filter(message=message)
	for comment in comments :
		bike = CommentLike.objects.filter(
		Q(user = request.user) & 
		Q(comment = comment)
		)
		comment.like = bool(bike)
	context = {'comments' : comments }
	return render(request, 'blog/show_replies.html', context )



@login_required(login_url='accounts/login')
def comment_reply_create_view(request, pk):
	comment_1 = Comment.objects.get(id=pk)
	message = comment_1.message
	post = message.post
	user = comment_1.commenter
	form = CommentForm(initial={'body':'@'+ user.username})
	if request.method == "POST" :
		comment = Comment.objects.create(
			commenter=request.user,
			user = user,
			post = post,
			message = message,
			body=request.POST.get('body'))
		return redirect('blog:show-reply', pk=message.id)
	context = {'form' : form }
	return render(request, 'blog/commentCreate.html', context )



@login_required(login_url='login')
def comment_create_view(request, pk):
	form = CommentForm()
	message = Message.objects.get(id=pk)
	room = message.room
	if request.method == "POST" :
		comment = Comment.objects.create(
			owner=request.user,
			message=message,
			body=request.POST.get('body'))
		participants = room.participants.add(request.user)
		return redirect('rooms:room', pk=room.id)
	context = {'form' : form }
	return render(request, 'rooms/roomCreate_old.html', context )



@login_required
def post_create_view(request):
	form = PostForm()
	if request.method == "POST" :
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post_object = form.save(commit=False)
			post_object.writer = request.user
			post_object.save()
			return redirect(post_object.get_absolute_url())
	context = {
		"form": form
	}
	return render(request, "blog/create_blog.html", context=context)


@login_required(login_url='accounts/login')
def message_like(request, pk):
	message = Message.objects.get(id=pk)
	post = message.post
	like = MessageLike.objects.filter(
	Q(user = request.user) & 
    Q(message = message))

	if not like:
		message_like = MessageLike.objects.create(
			user = request.user,
			message = message)
	 #    message.like = True
		# message.save() 
	else:
		MessageLike.objects.filter(
			Q(user = request.user) & 
			Q(message = message)).delete()
		# message.like = False
  #   	message.save()		
	return redirect('blog:detail', slug=post.slug)

	
	


@login_required(login_url='accounts/login')
def comment_like(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	like = CommentLike.objects.filter(
	Q(user = request.user) & 
    Q(comment = comment)
    ) 
	if not like:
		comment_like = CommentLike.objects.create(
			user = request.user,
			comment = comment)
		# comment.like = True
  #   	comment.save() 
	else:
		CommentLike.objects.filter(
			Q(user = request.user) & 
			Q(comment = comment)).delete()
		# comment.like = False
  #   	comment.save()		
	return redirect('blog:show-reply', pk=message.id)



login_required(login_url='accounts/login')
def message_edit(request, pk):
	message = Message.objects.get(id=pk)
	post = message.post
	form = MessageForm(instance=message)
	if request.user == message.sender :
		if request.method == "POST" :
			form = MessageForm(request.POST, instance=message)
			obj = form.save()
			return redirect('blog:detail', slug=post.slug)
		context = {'form' : form }
		return render(request, 'blog/commentEdit.html', context )
	else :
		return redirect('blog:detail', slug=post.slug)


login_required(login_url='accounts/login')
def comment_edit(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	form = CommentForm(instance=comment)
	if request.user == comment.commenter :
		if request.method == "POST" :
			form = CommentForm(request.POST, instance=comment)
			obj = form.save()
			return redirect('blog:show-reply', pk=message.id)
		context = {'form' : form }
		return render(request, 'blog/commentEdit.html', context )
	else :
		return redirect('blog:show-reply', pk=message.id)



@login_required(login_url='accounts/login')
def comment_delete(request, pk):
	comment = Comment.objects.get(id=pk)
	message = comment.message
	context = {'obj' : comment }
	if request.user == comment.commenter :
		if request.method == 'POST':
			comment.delete()
			return redirect('blog:show-reply', pk=message.id)
		return render(request, 'blog/commentDelete.html', context )
	else :
		return redirect('blog:show-reply', pk=message.id)


@login_required(login_url='accounts/login')
def message_delete(request, pk):
	message = Message.objects.get(id=pk)
	post = message.post
	context = {'obj' : message }
	if request.user == message.sender :
		if request.method == 'POST':
			message.delete()
			return redirect('blog:detail', slug=post.slug)
		return render(request, 'blog/commentDelete.html', context )
	else :
		return redirect('blog:detail', slug=post.slug)



def userprofile(request,  pk):
	user = User.objects.get(id=pk)
	posts = user.post_set.all()
	context = {'user':user, 'posts':posts}
	return render(request, 'blog/profile.html', context)



@login_required(login_url='login')
def editUser(request):
	user = request.user
	form = UserForm(instance=user)
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('blog:user-profile', pk=user.id)

	context = {'form':form}
	return render(request, 'account/edit_user.html', context)



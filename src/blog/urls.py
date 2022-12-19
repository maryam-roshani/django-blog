from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.post_create_view, name='create'),
    path('<str:slug>', views.post_detail, name='detail'),
    path('show-reply/<str:pk>', views.show_reply_view, name='show-reply'),
    path('comment-create/<str:pk>', views.comment_create_view, name='create-comment'),
    path('reply-create/<str:pk>', views.reply_create_view, name='create-reply'),
    path('comment-reply-create/<str:pk>', views.comment_reply_create_view, name='create-comment-reply'),
	path('comment-edit/<str:pk>', views.comment_edit, name='comment-edit'),
    path('message-edit/<str:pk>', views.message_edit, name='message-edit'),
    path('comment-delete/<str:pk>', views.comment_delete, name='comment-delete'),
    path('message-delete/<str:pk>', views.message_delete, name='message-delete'),
    path('message-like/<str:pk>', views.message_like, name='message-like'),
    path('comment-like/<str:pk>', views.comment_like, name='comment-like'),
    path('profile/<str:pk>', views.userprofile, name='user-profile'),
    path('edit-user/', views.editUser, name='edit-user'),
]
								
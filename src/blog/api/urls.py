from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='home'),
    # path('create', views.post_create_view, name='create'),
    # path('<str:slug>', views.post_detail, name='detail'),
    # path('show-reply/<str:pk>', views.show_reply_view, name='show-reply'),
    # path('comment-create/<str:pk>', views.comment_create_view, name='create-comment'), 
]

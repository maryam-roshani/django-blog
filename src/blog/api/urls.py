from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='home'),
    path('/create', views.PostCreateAPIView.as_view(), name='create'),
    path('/<int:pk>/', views.PostDetailAPIView.as_view(), name='detail'),
    path('/<int:pk>/edit', views.PostUpdateAPIView.as_view(), name='update'),
    path('/<int:pk>/delete', views.PostDeleteAPIView.as_view(), name='delete'),
    # path('show-reply/<str:pk>', views.show_reply_view, name='show-reply'),
    # path('comment-create/<str:pk>', views.comment_create_view, name='create-comment'), 
]

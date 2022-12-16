from django.contrib import admin
from .models import Post, Comment, User, Message, MessageLike, CommentLike


# Register your models here.
class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	search_fields = ['title', 'topic']
	raw_id_fields = ['writer']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(MessageLike)
admin.site.register(CommentLike)


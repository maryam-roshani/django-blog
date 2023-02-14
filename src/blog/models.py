from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
import uuid
from django.urls import reverse
from .utils import slugify_instance_title
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')

        user = self.model(
                email=self.normalize_email(email),
                username=username
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
                email=self.normalize_email(email),
                username=username,
                password=password,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email Address', unique=True)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True)
    avatar = models.FileField(null=True, default="avatar.svg", validators=[FileExtensionValidator(['png', 'svg', 'jpg'])])
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class PostQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(topic__icontains=query)
        return self.filter(lookups) 

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Post(models.Model):
    topic = models.CharField(max_length=100, null=True, blank=True) 
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    picture = models.ImageField(blank=True, null=True, upload_to="media")
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.title + str(self.id)

    objects = PostManager()

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    

def post_pre_save(sender, instance, *args, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(post_pre_save, sender=Post)


def post_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(post_post_save, sender=Post)



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    body = models.TextField()  
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)
    

    def __str__(self):
        return self.body[:20]


class MessageLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    
    
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='previous')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    body = models.TextField()  
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.body[:20]


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

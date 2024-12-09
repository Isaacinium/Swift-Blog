from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid

class User(AbstractUser):
    username = ShortUUIDField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        email_username, provider = self.email.split('@')

        if self.full_name is None or self.full_name == '':
            self.full_name = email_username
        if self.username is None or self.username == '':
            self.username = email_username
        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    about = models.TextField(max_length=500, blank=True, null=True)
    author = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if self.full_name is None or self.full_name == '':
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_superuser_profile(sender, instance, **kwargs):
        instance.profile.save()
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_superuser_profile, sender=User)

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.png', upload_to='category_images', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
            super(Category, self).save(*args, **kwargs)

    def post_count(self):
        return Post.objects.filter(category=self).count()

class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(default='dp.png', upload_to='post_pics')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_user')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        get_latest_by = 'date_posted'

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]
            super(Post, self).save(*args, **kwargs)
    def comments(self):
        return Comment.objects.filter(post=self)


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    reply = models.TextField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Comment'

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Bookmark'

class Notification(models.Model):
    NOTI_TYPE = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('bookmark', 'Bookmark'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)

    def __str__(self):
        if self.post:
            return f"{self.post.title} - {self.type}"
        else:
            return "Notification"





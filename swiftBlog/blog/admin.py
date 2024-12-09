from django.contrib import admin
from blog import models as blog_models

admin.site.register(blog_models.User)
admin.site.register(blog_models.Profile)
admin.site.register(blog_models.Post)
admin.site.register(blog_models.Comment)
admin.site.register(blog_models.Category)
admin.site.register(blog_models.Bookmark)
admin.site.register(blog_models.Notification)




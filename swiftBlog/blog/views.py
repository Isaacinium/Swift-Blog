from allauth.account.views import email
from decouple import undefined
from django.shortcuts import render

from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
#Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
import json
import random

from unicodedata import category

from blog import serializers as blog_serializer
from blog import models as blog_models



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = blog_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = blog_serializer.RegisterSerializer
    queryset = blog_models.User.objects.all()
    permission_classes = (AllowAny,)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = blog_serializer.ProfileSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = blog_models.User.objects.get(id=user_id)
        profile = blog_models.Profile.objects.get(user = user)
        return profile

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = blog_serializer.CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return blog_models.Category.objects.all()

class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = blog_serializer.PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = blog_models.Category.objects.get(slug=category_slug)
        return blog_models.Post.objects.filter(category=category, status='draft')




class PostListAPIView(generics.ListAPIView):
    serializer_class = blog_serializer.PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return blog_models.Post.objects.filter(status='draft')

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = blog_serializer.PostSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        slug = self.kwargs['slug']
        post = blog_models.Post.objects.get(slug=slug, status='draft')
        post.views+=1
        post.save()
        return post

class LikePostAPIView(APIView):
    permission_classes=[AllowAny,]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The user who liked the post'),
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The id of the post'),
            },
        ),
    )

    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = blog_models.User.objects.get(id=user_id)
        post = blog_models.Post.objects.get(id=post_id)

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Post Disliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)

            blog_models.Notification.objects.create(
                user= post.user,
                post= post,
                type = 'like',
            )
            return Response({'message': 'Post Liked'}, status=status.HTTP_201_CREATED)

class PostCommentAPIView(APIView):
    permission_classes = [AllowAny, ]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The id of the post'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name of the user'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email of the user'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='The comment'),
            },
        ),
    )

    def post(self, request):
        post_id = request.data['post_id']
        name = request.data['name']
        email = request.data['email']
        comment = request.data['comment']

        post = blog_models.Post.objects.get(id=post_id)

        blog_models.Comment.objects.create(
            name=name,
            email=email,
            comment=comment,
            post=post,
        )

        blog_models.Notification.objects.create(
            user=post.user,
            post=post,
            type='comment',
        )
        return Response({'message': 'Comment Sent'}, status=status.HTTP_201_CREATED)

class BookmarkPostAPIView(APIView):
    permission_classes = [AllowAny, ]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The id of the post'),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The user who bookmarked the post'),
            }
        )
    )
    def post(self, request):
        post_id = request.data['post_id']
        user_id = request.data['user_id']

        user = blog_models.User.objects.get(id=user_id)
        post = blog_models.Post.objects.get(id=post_id)
        bookmark = blog_models.Bookmark.objects.filter(post=post, user=user).first()
        if bookmark:
            bookmark.delete()
            Response({'message': 'Bookmark Deleted'}, status=status.HTTP_200_OK)
        else:
            blog_models.Bookmark.objects.create(
                post=post,
                user=user,
            )

            blog_models.Notification.objects.create(
                user=post.user,
                post=post,
                type='Bookmark',
            )
            return Response({'message': 'Post Bookmarked'}, status=status.HTTP_201_CREATED)

class DashboardStatsAPIView(generics.ListAPIView):
    serializer_class = blog_serializer.AuthorSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = blog_models.User.objects.get(id=user_id)

        views = blog_models.Post.objects.filter(user=user).aggregate(views=Sum('views'))['views']
        posts = blog_models.Post.objects.filter(user=user).count()
        likes = blog_models.Post.objects.filter(user=user).aggregate(total_likes=Sum('likes'))['total_likes']
        bookmarks = blog_models.Bookmark.objects.filter(user=user).count()
        return [{
                'views': views,
                'likes': likes,
                'posts': posts,
                'bookmarks': bookmarks,
            }]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DashboardPostsListApiView(generics.ListAPIView):
    serializer_class = blog_serializer.PostSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = blog_models.User.objects.get(id=user_id)
        return blog_models.Post.objects.filter(user=user).order_by('-id')

class DashboardCommentsListApiView(generics.ListAPIView):
    serializer_class = blog_serializer.CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return blog_models.Comment.objects.all()

class DashboardNotificationListApiView(generics.ListAPIView):
    serializer_class = blog_serializer.NotificationSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = blog_models.User.objects.get(id=user_id)
        return blog_models.Notification.objects.all(seen=False, user=user)

class DashboardMarkNotificationAsSeenApiView(APIView):

    def post(self, request):
        notification_id = request.data['notification_id']
        notification = blog_models.Notification.objects.get(id=notification_id)
        notification.seen = True
        notification.save()
        return Response({'message': 'Notification Seen'}, status=status.HTTP_200_OK)

class DashboardReplyCommentApiView(APIView):
    def post(self, request):
        comment_id = request.data['comment_id']
        reply = request.data['reply']
        comment = blog_models.Comment.objects.get(id=comment_id)
        comment.reply = reply
        comment.save()
        return Response({'message': 'Comment Replied'}, status=status.HTTP_201_CREATED)

class DashboardPostCreateApiView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = blog_serializer.PostSerializer
    def post(self, request):
        print(request.data)

        user_id = request.data['user_id']
        title = request.data['title']
        image = request.data['image']
        description = request.data['description']
        tags = request.data['tags']
        category_id = request.data['category_id']
        post_status = request.data['post_status']

        user = blog_models.User.objects.get(id=user_id)
        category = blog_models.Category.objects.get(id=category_id)

        blog_models.Post.objects.create(
            user=user,
            title=title,
            image=image,
            description=description,
            tags=tags,
            category=category,
            status=post_status
        )
        return Response({'message': 'Post Created'}, status=status.HTTP_201_CREATED)

class DashboardPostEditApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = blog_serializer.PostSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']

        return blog_models.Post.objects.get(id=user_id)

    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()

        title = request.data['title']
        image = request.data['image']
        description = request.data['description']
        tags = request.data['tags']
        category_id = request.data['category_id']
        post_status = request.data['post_status']
        category = blog_models.Category.objects.get(id=category_id)

        post_instance.title = title

        if image != "undefined":
            post_instance.image = image
            post_instance.description = description
            post_instance.tags = tags
            post_instance.category = category
            post_instance.status = post_status
            post_instance.save()
            return Response({'message': 'Post Updated'}, status=status.HTTP_200_OK)


















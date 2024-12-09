from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from blog import views as blog_views

urlpatterns = [
    path('user/token/', blog_views.MyTokenObtainPairView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', blog_views.RegisterView.as_view(), name='register'),
    path('user/profile/<user_id>', blog_views.ProfileView.as_view(), name='profile'),

    path('post/category/list/', blog_views.CategoryListAPIView.as_view(), name='category-list'),
    path('post/category/posts/<category_slug>/', blog_views.PostCategoryListAPIView.as_view(), name='post-category-list'),
    path('post/lists/', blog_views.PostListAPIView.as_view(), name='post-list'),
    path('post/detail/<slug>/', blog_views.PostDetailAPIView.as_view(), name='post-detail'),
    path('post/like-post/', blog_views.LikePostAPIView.as_view(), name='like-post'),
    path('post/comment-post/', blog_views.PostCommentAPIView.as_view(), name='comment-post'),
    path('post/bookmark-post/', blog_views.BookmarkPostAPIView.as_view(), name='bookmark-post'),
    path('author/dashboard/stats/<user_id>/', blog_views.DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('author/dashboard/comment-list/<user_id>/', blog_views.DashboardCommentsListApiView.as_view(), name='dashboard-comments-list'),
    path('author/dashboard/notification-list/<user_id>/', blog_views.DashboardNotificationListApiView.as_view(), name='dashboard-notifications-list'),
    path('author/dashboard/notification-mark-as-seen/<user_id>/', blog_views.DashboardMarkNotificationAsSeenApiView.as_view(), name='dashboard-mark-notification-as-seen'),
    path('author/dashboard/reply-comment/<user_id>/', blog_views.DashboardReplyCommentApiView.as_view(), name='dashboard-reply-comment'),
    path('author/dashboard/post-create/', blog_views.DashboardPostCreateApiView.as_view(), name='dashboard-post-create'),
    path('author/dashboard/post-detail/<user_id>/<post_id>/', blog_views.DashboardPostEditApiView.as_view(), name='dashboard-post-detail'),

]

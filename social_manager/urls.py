from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('notifications', Notifications.as_view(), name='notifications'),
    path('edit-profile', EditProfile.as_view(), name='edit-profile'),
    path('profile/<str:pk>', Profile.as_view(), name='profile'),
    path('saved-posts/<str:pk>', GetSavedPostdView.as_view(), name='saved-posts'),
    path('follow/<str:user_to>', follow, name='follow'),
    path('write-post', WritePost.as_view(), name='write-post'),
    path('post/<str:id>/<str:slug>', GetPost.as_view(), name='post'),
    path('profile-search', ProfileSearch.as_view(), name='profile-search'),
    path('like-post/<str:post_id>', LikePostView.as_view(), name='like-post'),
    path('delete-post/<str:post_id>', postDeleteView, name='delete-post'),
    path('save-post/<str:post_id>', SavePostView.as_view(), name='save-post'),
    path('profilePostItems', ProfilePostItems.as_view(), name='profilePostItems'),
    path('edit-write-post/<str:pk>', EditWritePost.as_view(), name='edit-write-post'),

    #comments system urls start
    path('like-post-comment/<str:comment_id>', LikePostCommentView.as_view(), name='like-post-comment'),
    path('post/comments/<int:post_pk>/', PostCommentsDetailView.as_view(), name='post-comments-detail'),
    path('post/comment/delete/<int:pk>/', commentDeleteView, name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    #comments system urls end
]

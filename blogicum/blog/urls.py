from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.IndexListView.as_view(),
         name='index'
         ),
    path('posts/create/',
         views.CreatePost.as_view(),
         name='create_post'
         ),
    path('posts/edit/<int:post_pk>',
         views.EditPost.as_view(),
         name='edit_post'
         ),
    path('posts/<int:post_pk>/',
         views.PostDetail.as_view(),
         name='post_detail'
         ),
    path('posts/delete/<int:post_pk>',
         views.DeletePost.as_view(),
         name='delete_post'
         ),
    path('category/<slug:category_slug>/',
         views.CategoryPage.as_view(),
         name='category_posts'
         ),
    path('profile/edit/',
         views.UserProfileEdit.as_view(),
         name='edit_profile'
         ),
    path('profile/<slug:username>/',
         views.UserProfileDetail.as_view(),
         name='profile'
         ),
    path('posts/<int:post_pk>/comment/<int:comment_pk>',
         views.AddComment.as_view(),
         name='add_comment'
         ),
    path('posts/<int:post_pk>/comment/edit_comment/<int:comment_pk>/',
         views.EditComment.as_view(),
         name='edit_comment'
         ),
    path('posts/<int:post_pk>/comment/delete_comment/<int:comment_pk>/',
         views.DeleteComment.as_view(),
         name='delete_comment'
         ),
]

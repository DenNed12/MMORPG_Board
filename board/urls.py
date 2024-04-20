from django.urls import path,include
from .views import PostList,PostDetail,index, CreatePost, EditPost,DeletePost #UserPostList,AddReply
#from django.views.generic import TemplateView

app_name = 'board'
urlpatterns = [
    path('', index),
    path('board/', PostList.as_view()),
    path('board/<int:pk>',PostDetail.as_view(),name='post'),
    path('board/add/', CreatePost.as_view(), name ='create_post'),
    path('board/<int:pk>/update/', EditPost.as_view(),name ='edit_post'),
    path('board/<int:pk>/delete/', DeletePost.as_view(), name ='delete_post'),]
    # path('user_posts/', UserPostList.as_view(), name='user_posts')
    # path('replies/', reply_list, name='replies_to_user'),

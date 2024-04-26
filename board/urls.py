from django.urls import path,include
from .views import PostList,PostDetail,index, CreatePost, EditPost,DeletePost, AddReply,Replies #UserPostList,AddReply
#from django.views.generic import TemplateView

app_name = 'board'
urlpatterns = [
    path('', index),
    path('board/', PostList.as_view()),
    path('board/<int:pk>',PostDetail.as_view(),name='post'),
    path('board/add/', CreatePost.as_view(), name ='create_post'),
    path('board/<int:pk>/update/', EditPost.as_view(),name ='edit_post'),
    path('board/<int:pk>/delete/', DeletePost.as_view(), name ='delete_post'),
    path('board/<int:pk>/add_reply/', AddReply.as_view(), name ='add_repl'),
    path('board/replies/', Replies.as_view(), name='replies_to_user'),]

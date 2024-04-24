from django.urls import path
from .views import RegisterView,ConfirmUser,LoginView
app_name="users"
urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('confirm_user/<str:username>/', ConfirmUser.as_view(), name='confirm_user'),
    #path('profile/')
]
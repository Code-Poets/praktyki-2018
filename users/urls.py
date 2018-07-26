from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:pk>/stats/', views.UserStats.as_view(), name='user_stats'),
    path('<int:pk>/leave/', views.DeleteUserView.as_view(), name='delete_user'),
]

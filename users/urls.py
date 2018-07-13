from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('join/', views.JoinIn.as_view(), name='join'),
    path('create/', views.Create.as_view(), name='create'),
]

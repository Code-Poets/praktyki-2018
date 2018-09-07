from django.urls import path
from .views import view_sign_up
from .views import view_user_stats
from .views import view_delete_user
from .views import view_change_password
from .views import view_custom_user_update

urlpatterns = [
    path('signup/', view_sign_up.SignUp.as_view(), name='signup'),
    path('<int:pk>/stats/', view_user_stats.UserStats.as_view(), name='user_stats'),
    path('account/<int:pk>/leave/', view_delete_user.DeleteUserView.as_view(), name='delete_user'),
    path('account/password', view_change_password.change_password, name='change_password'),
    path('account', view_custom_user_update.CustomUser_update, name='edit_profile'),
]

# users/urls/auth_urls.py

from django.urls import path
from views.auth_views import create_user, get_users, retrieve_user, update_user, delete_user, login, refresh_token, signup

urlpatterns = [
    path("create_user/", create_user, name="create_user"),
    path("get_users/", get_users, name="get_users"),
    path("retrieve_user/<int:pk>/", retrieve_user, name="retrieve_user"),
    path("update_user/<int:pk>/", update_user, name="update_user"),
    path("delete_user/<int:pk>/", delete_user, name="delete_user"),
    path('login/', login, name='login'),
    path('refresh/', refresh_token, name='refresh_token'),
    path('signup/', signup, name='signup'),
]

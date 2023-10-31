"""
URL configuration for ERP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_user/", views.create_user, name="create_user"),
    path("get_users/", views.get_users, name="get_users"),
    path("retrieve_user/<int:pk>/", views.retrieve_user, name="retrieve_user"),
    path("update_user/<int:pk>/", views.update_user, name="update_user"),
    path("delete_user/<int:pk>/", views.delete_user, name="delete_user"),
]

"""
URL configuration for bloggingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from blogs.views import (
    user_detail,
    user_list,
    CreateUserView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register-user"),
    path("api/user/<int:pk>/", user_detail, name="user"),
    path("api/users/", user_list, name="user-list"),
    path("api/blogs/", include("blogs.urls")),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("api-auth/", include("rest_framework.urls")),
]

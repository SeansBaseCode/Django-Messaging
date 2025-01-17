"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from app.views import *

urlpatterns = [
    path("", sign_in, name="login"),
    path("login/", sign_in, name="login"),
    path("signup", sign_up, name="signup"),
    path("login/signup", sign_up, name="signup"),
    path("messages", message_board, name="messages"),
    path("delete_message/<int:message_id>", delete, name="delete" ),
    path("delete_all", delete_all_messages, name="delete_all"),
    path("access", admin_access, name="access"),
    path("admin/", admin.site.urls),
]

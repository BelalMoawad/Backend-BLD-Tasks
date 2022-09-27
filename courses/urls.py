"""courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import imp
from django.contrib import admin
from django.urls import path, include
from courses import views


urlpatterns = [
    path('', include('workcourses.urls')),
    path('admin/', admin.site.urls),
    path('courses/', views.CourseView.as_view()),
    path("courses/<str:id>", views.SingleCourseView.as_view()),
    path('users/', views.UserView.as_view()),
    path("users/<str:id>", views.SingleUserView.as_view()),
    path("query/", views.UserQueriesView.as_view()),
]
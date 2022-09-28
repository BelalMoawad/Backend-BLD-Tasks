from django.urls import path
from users import views 

urlpatterns = [
    path('', views.UserView.as_view()),
    path("<str:id>", views.SingleUserView.as_view()),
    path("query/", views.UserQueriesView.as_view()),
]
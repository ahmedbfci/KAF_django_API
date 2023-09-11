from django.urls import path

from . import views
from .views import (
    UserListApiView,
    UserSearchLikeApiView,
    UserSearchExactlyApiView,
    uploadApiView
    #TodoDetailApiView
)

urlpatterns = [
    path('list/', UserListApiView.as_view()),
    path('search/like/', UserSearchLikeApiView.as_view()),
    path('search/exactly/', UserSearchExactlyApiView.as_view()),
    path('uplod/', uploadApiView.as_view()),
    #path('api/<str:user_name>/', TodoDetailApiView.as_view()),
    #path("", views.index, name="index"),
]
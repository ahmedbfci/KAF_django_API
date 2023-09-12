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
    path('upload/', uploadApiView.as_view())
]

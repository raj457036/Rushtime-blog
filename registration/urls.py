from django.urls import path,include
from .views import UserDetail, ProfileView, PhotosList, UpdateProfileView, BookmarkView

app_name = 'registration'

urlpatterns = [
    path('',ProfileView.as_view(),name='myprofile'),
    path('<int:pk>/',UserDetail.as_view(),name='userprofile'),
    path('<int:pk>/update',UpdateProfileView.as_view(),name='updateprofile'),
    path('post/',include('post.urls')),
    path('photos/',PhotosList.as_view(), name='myphotos'),
    path('bookmark/', BookmarkView.as_view(), name='bookmark'),
]
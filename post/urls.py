from django.urls import path
from .views import PostDetailView, PostCreateView, PostLike, PostDeleteView

app_name="post"

urlpatterns = [
    path('<int:pk>',PostDetailView.as_view(), name='detail'),
    path('new', PostCreateView.as_view(), name='new'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='delete'),
    path('api/like/',PostLike, name='postlike')
]
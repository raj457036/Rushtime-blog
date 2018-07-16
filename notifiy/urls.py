from django.urls import path
from .views import NoticeList

app_name='notifiy'

urlpatterns = [
    path('',NoticeList.as_view(), name='notifications')
]
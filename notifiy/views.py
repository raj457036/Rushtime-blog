from django.shortcuts import render
from django.views.generic import ListView
from .models import Notice

# Create your views here.

class NoticeList(ListView):
    model = Notice
    template_name = 'notifiy/notice.html'

    def get_queryset(self, *args, **kwargs):
        query = Notice.objects.filter(user=self.request.user).order_by('-date_time')
        return query

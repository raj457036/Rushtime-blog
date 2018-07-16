from django.views.generic import TemplateView
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class HomeView(LoginRequiredMixin, TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        following_list = list(self.request.user.userextend.get_following()) + [self.request.user,]
        p = Post.objects.filter(user__in=following_list).order_by('-created_on')
        ctx['post_list'] = p
        return ctx
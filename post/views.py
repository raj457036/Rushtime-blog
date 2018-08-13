from django.shortcuts import redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models
from registration.models import Images, UserExtend
from django.db.models import Q,F
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from .forms import PostCreateForm
from notifiy.models import Notice
from django.http import JsonResponse
# Create your views here.
Post_Topics_List = {'0': 'PERSONAL', '1': 'FUTURE', '2': 'CULTURE', '3': 'TECH', '4': 'ENTREPRENEURSHIP', '5': 'SELF', '6': 'POLITICS', '7': 'DESIGN', '8': 'SCIENCE', '9': 'POPULAR'}
class PostDetailView(LoginRequiredMixin, DetailView):
    model = models.Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        g = self.request.GET.get('read', False)
        sl = self.object.user.userextend.protected
        ctx = super().get_context_data(**kwargs)
        ctx['topics'] = [Post_Topics_List[t] for t in self.object.user.post_set.values_list('post_topic', flat=True).distinct()]
        if g:
            n = Notice.objects.get(pk=g)
            n.viewed = True
            n.save()
        if self.object.user == self.request.user:
            ctx['lock'] = False # all allowed
            ctx['me'] = True
        else:
            ctx['me'] = False
            if sl == '3':
                ctx['lock'] = False # all allowed
            elif sl == '2':
                if self.object.user in self.request.user.userextend.get_following():
                    ctx['lock'] = False # all allowed
                else:
                    ctx['lock'] = True # no allowed
            else:
                ctx['lock'] = True # no allowed
                ctx['superlock'] = True
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    form_class = PostCreateForm
    template_name = 'post/post_create.html'
    success_url = '/'
    initial = {}

    def get_context_data(self, **kwargs):
        self.user = self.request.user
        self.initial = {
            'visibility':self.request.user.userextend.Post_Type}
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def PostLike(request):
    p = models.Post.objects.get(id=request.GET.get('post_id'))
    liker, created = p.likers.get_or_create(users_id=request.user.pk) 
    
    if not created:
        liker.delete()
        p.upvote = F('upvote') - 1
    else :
        p.upvote = F('upvote') + 1
    
    p.save()
    p.refresh_from_db()
    return JsonResponse(data={'status':created,'likes':int(p.upvote)})


class PostUpdateView(UpdateView):
    model = models.Post
    # fields = ['title','sub_title','head_img','content','draft','visibility']
    form_class = PostCreateForm
    template_name = 'post/post_update.html'
    success_url = '/'
    initial = {}

    def get_context_data(self, **kwargs):
        self.initial = {'visibility':self.request.user.userextend.Post_Type}
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    template_name = 'post/delete_post.html'
    model = models.Post
    success_url= '/user/'
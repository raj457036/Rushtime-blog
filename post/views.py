from django.shortcuts import redirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models
from registration.models import Images, UserExtend
from django.db.models import Q
from django.views.generic import DetailView, CreateView, DeleteView
from notifiy.models import Notice
from django.http import JsonResponse
# Create your views here.

class PostDetailView(LoginRequiredMixin, DetailView):
    model = models.Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        g = self.request.GET.get('read', False)
        sl = self.object.user.userextend.protected
        ctx = super().get_context_data(**kwargs)
        print(sl)
        if g:
            n = Notice.objects.get(pk=g)
            n.viewed = True
            n.save()
        if self.request.user == self.object.user:
            ctx['lock'] = False # all allowed
            ctx['me'] = True
        else:
            ctx['me'] = False
            if sl == '3':
                ctx['lock'] = False # all allowed
            elif sl == '2':
                if self.request.user in self.object.user.userextend.get_followers():
                    ctx['lock'] = False # all allowed
                else:
                    ctx['lock'] = True # no allowed
            else:
                ctx['lock'] = True # no allowed

        return ctx

@login_required
def PostComment(request):
    if request.method == "POST":
        if len(request.POST['comment'].strip(" ")) > 0:
            p = models.Post.objects.get(pk=request.POST['post'])
            models.Comment(who=request.user, post=p, 
            content=request.POST['comment']).save()
        return redirect(resolve_url('registration:post:detail',pk=request.POST['post'])+"#comment")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    fields = ['title','sub_title','head_img','content','draft']
    template_name = 'post/post_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def PostLike(request):

    p = models.Post.objects.get(id=request.GET.get('post_id'))
    liker, created = p.likers.get_or_create(users_id=request.user.pk) 
    
    if not created:
        liker.delete()
    
    print(created, liker)
    return JsonResponse(data={'status':created})


class PostDeleteView(DeleteView):
    template_name = 'post/delete_post.html'
    model = models.Post
    success_url= '/user/'

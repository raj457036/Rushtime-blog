from django.views.generic import TemplateView
from django.http import JsonResponse
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from registration.models import Follower, Bookmarks
from itertools import zip_longest

class HomeView(LoginRequiredMixin, TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        following_list = list(self.request.user.userextend.get_following()) + [self.request.user,]
        p = Post.objects.filter(user__in=following_list).order_by('-created_on')
        ctx['post_list'] = p
        return ctx


@login_required
def search_result_sync(request):
    data = request.GET.get('data', None)
    people_objects = []
    post_objects = []

    peoples = User.objects.filter(Q(username__icontains = data) | Q(first_name__icontains = data) | Q(last_name__icontains = data))
    posts = Post.objects.filter(Q(title__icontains = data) | Q(sub_title__icontains = data))

    for i, j in zip_longest(peoples, posts):
        if i is not None:
            people_objects.append({
            'id':i.pk,
            'name':i.get_full_name(), 
            'username':i.username, 
            'profile_pic':i.userextend.get_profile_pics().first().img.url if i.userextend.get_profile_pics().first() != None else '/static/registration/imgs/user.png',
            })

        if j is not None:
            post_objects.append({
            'id':j.pk,
            'title':j.title, 
            'subtitle':j.sub_title, 
            'img':j.head_img.url,
            })

    if not peoples:
        people_objects = False
    if not posts:
        post_objects = False

    ctx = {'peoples':people_objects, 'posts':post_objects}
    return JsonResponse(ctx)

    
@login_required
def follow_user(request):
    if request.method == 'POST':
        u = User.objects.get(pk=request.POST['user_id'])
        f = Follower.objects.get(current_user = request.user)
        if u in request.user.userextend.get_following():
            f.remove_follow(request.user, u)
            return JsonResponse({'status':False})
        else:
            f.add_follow(request.user, u)
            return JsonResponse({'status':True})
    else:
        return JsonResponse({'status': None})


@login_required
def bookmark(request):
    obj, created = Bookmarks.objects.get_or_create(user=request.user, o_id=request.GET.get('post_id'))

    if created:
        return JsonResponse({'status':True})
    else:
        obj.delete()    
        return JsonResponse({'status':False})
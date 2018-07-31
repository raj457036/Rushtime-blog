from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from post.models import Post, reply, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from registration.models import Bookmarks
from itertools import zip_longest
from django.views.decorators.csrf import csrf_exempt

class HomeView(LoginRequiredMixin, TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        following_list = list(self.request.user.userextend.get_following()) + [self.request.user,]
        p = Post.objects.filter(
            Q(user__in=following_list) &
            ~Q(visibility='3') &
            Q(draft=False)
        ).order_by('-created_on')
    
        ctx['post_list'] = p
        return ctx

class TrendingPosts(LoginRequiredMixin, TemplateView):
    template_name = 'blog/trending.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['topics'] = "FUTURE,CULTURE,TECH,ENTREPRENEURSHIP,SELF,POLITICS,DESIGN,SCIENCE,POPULAR,MORE".split(',')
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
            'profile_pic':i.userextend.get_profile_pics().first().img.url if i.userextend.get_profile_pics().first() != None else i.userextend.get_avatar_url(stat=True),
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
        if u in request.user.userextend.following.all():
            request.user.userextend.following.remove(u)
            return JsonResponse({'status':False})
        else:
            request.user.userextend.following.add(u)
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

@login_required
def draft(request):
    p = Post.objects.get(pk=request.POST['post_id'])
    p.draft = not p.draft
    p.save()
    if p.draft:
        return JsonResponse({'status':True})
    else:
        return JsonResponse({'status':False})


def user_details(request):
    user = User.objects.get(username=request.GET['username'])
    ctx = {}
    ctx['name'] = user.get_full_name()
    ctx['profile_pic'] = user.userextend.get_profile_pics().first().img.url if len(user.userextend.get_profile_pics()) > 0 else user.userextend.get_avatar_url(stat=True)
    ctx['joined'] = user.date_joined.date()
    ctx['about'] = user.userextend.aboutMe
    ctx['top-posts'] = [(post.pk,post.title) for post in user.post_set.all().order_by('upvote')[:3]]
    ctx['followers'] = len(user.userextend.get_followers())
    return JsonResponse(ctx)

@login_required
@csrf_exempt
def comment_reply(request):
    if request.method == "POST":
        r = request.POST.get('reply','').strip(' ')
        if len(r) > 0:
            com = Comment.objects.get(pk=int(request.POST['comment_id']))
            print(com)
            r = reply(who=request.user, comment=com, content=r)
            r.save()
            return render_to_response('post/reply.html', context={'reply':r,'post':r.comment.post,})
    return JsonResponse({'status':False})


@login_required
@csrf_exempt
def post_comment(request):
    if request.method == "POST":
        c = request.POST.get('comment','').strip(" ")
        if len(c) > 0:
            p = Post.objects.get(pk=int(request.POST['post']))
            c = Comment(who=request.user, post=p, content=c)
            c.save()
        return render_to_response('post/comment.html', context={'comment':c, 'post':c.post,})

@login_required
@csrf_exempt
def comment_remove(request):
    if request.method == "POST":
        c = request.POST.get('id')
        c = get_object_or_404(Comment, pk=c)

        # if requested user is owner of comment or the owner of post

        if request.user == c.who or request.user == c.post.user:
            c.delete()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})


@login_required
@csrf_exempt
def reply_remove(request):
    if request.method == "POST":
        r = request.POST.get('id')
        r = get_object_or_404(reply, pk=r)

        # if requested user is owner of reply or the owner of post

        if request.user == r.who or request.user == r.comment.post.user:
            r.delete()
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
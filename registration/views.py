from django.shortcuts import render,redirect,reverse
from post.models import Post
from .models import Images, UserExtend, Bookmarks
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, authenticate, views as auth_view, mixins, models
from django.views.generic import DetailView, TemplateView, ListView, UpdateView
from django.db.models import Q
# Create your views here.

def signup(request):

    def sepName(name):
        sp = name.split(' ')
        fname = sp[0]
        lname = ' '.join(sp[1:]) if len(sp) > 1 else ''
        return (fname,lname)

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)

            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.first_name,user.last_name = sepName(form.cleaned_data.get('name'))
                user.userextend.gender = form.cleaned_data.get('gender')
                user.userextend.date_of_birth = form.cleaned_data.get('date_of_birth')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = SignupForm()
        
        return render(request,'registration/signup.html',{'form':form})
    else:
        return redirect('')

class RegLogin(auth_view.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().dispatch(*args, **kwargs)

class RegLogout(mixins.LoginRequiredMixin, auth_view.LogoutView):
    login_url = '/login/'
    redirect_field_name = 'direct'

class UserDetail(mixins.LoginRequiredMixin, DetailView):
    model = models.User
    template_name = 'registration/userDetail.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post_list'] = Post.objects.filter(user__pk=self.kwargs['pk'])
        return ctx

class ProfileView(mixins.LoginRequiredMixin, ListView):
    model = Post
    template_name = 'registration/profileDetail.html'
    context_object_name = 'post_list'

    def get_queryset(self, *args, **kwargs):
        query = Post.objects.filter(user=self.request.user)
        return query
        

class PhotosList(mixins.LoginRequiredMixin, ListView):
    template_name = "registration/Photos.html"
    context_object_name = 'img_list'
    model = models.User

    def get_queryset(self, *args, **kwargs):
        if  self.request.GET.get('pk',False):
            query = Images.objects.filter(user__pk =  UserExtend.objects.get(user__pk = self.request.GET.get('pk')).pk)
        else:
            query = Images.objects.filter(user = self.request.user.userextend)

        return query

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = models.User.objects.get(pk=self.request.GET['pk']) if self.request.GET.get('pk',False) else self.request.user
        return ctx


class UpdateProfileView(mixins.LoginRequiredMixin, UpdateView):
    template_name = 'registration/update_profile.html'
    model = UserExtend
    fields = '__all__'

class BookmarkView(mixins.LoginRequiredMixin, ListView):
    template_name = 'registration/bookmarks.html'
    model = Bookmarks
    context_object_name = 'bookmarks'
    
    def get_queryset(self):
        o_ids = self.request.user.userextend.get_bookmarks()
        query = Post.objects.filter(pk__in = o_ids)
        return query
    
from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title','sub_title','head_img','content','draft']

    def form_valid(self, form):
        print(form)
        return super().form_valid(form)
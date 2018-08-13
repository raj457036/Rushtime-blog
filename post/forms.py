from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title','sub_title','head_img','content','draft','visibility','post_tags','post_topic']
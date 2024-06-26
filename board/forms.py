from .models import Post,Reply
from django import forms


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','text','cat']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
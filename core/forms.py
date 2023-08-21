from django import forms
from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment_text']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['nickname', 'description', 'link_fb', 'whatsapp', 'telegram', 'photo']


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['name', 'photo']
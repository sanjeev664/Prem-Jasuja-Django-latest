from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(ModelForm):
	class Meta:
		model=UserPosts
		fields = '__all__'


class CommentForm(ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

    class Meta:
        model = PostComments
        fields = ['comment']

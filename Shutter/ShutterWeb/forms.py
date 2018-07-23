from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    # content=forms.CharField(label='comment_content',max_length=500)
    class Meta:
        model= Topiccomment
        fields = ['content', ]



class TopicForm(forms.ModelForm):
    class Meta:
        model= Topic
        fields = ['title', 'content']

    # register related

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ("username", "email")


class photoForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Photo
        fields = ['category', 'photo_name', 'photographer_name', 'photographer_remark', 'image']

class photocommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ['content']

class messageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'gender', 'address', 'email']

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model= NewsComment
        fields = ['content', 'author']
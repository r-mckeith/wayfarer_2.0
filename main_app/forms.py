from django import forms
from .models import Post, Profile, City, Comment

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'body']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['first_name', 'last_name', 'current_city']

class CityForm(forms.ModelForm):
  class Meta:
    model = City
    fields = ['name', 'photo_url']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']

class ReplyForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']


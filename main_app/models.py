from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .check_time import check_time
from django.utils import timezone
import math

# Create your models here.
class City(models.Model):
  name = models.CharField(max_length=100, unique=True)
  photo_url = models.CharField(max_length=500)
  slug = models.SlugField(max_length=50, blank=True)

  def save(self):
    if not self.id: 
      self.slug = slugify(self.name)
    super(City, self).save()


  def __str__(self):
    return self.name

class Post(models.Model):
  title = models.CharField(max_length=200)
  body = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  # check_time = check_time
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.title}, {self.city}'  

  def posted(self):
    return check_time(self)

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  content = models.TextField()
  reply = models.ForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, related_name='replies')
  is_parent = models.BooleanField(null=True)

  def __str__(self):
    return f'{self.user}\'s comment'  

  def posted(self):
    return check_time(self)

  def ordered(self):
    return self.order_by('-created_at')

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  current_city = models.CharField(max_length=50)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  photo_url = models.CharField(max_length=200, default="https://s3-us-west-1.amazonaws.com/wayfarer-pp/d80df8.png")

  def __str__(self):
    return f'{self.first_name} {self.last_name} is from {self.current_city} @{self.photo_url}'
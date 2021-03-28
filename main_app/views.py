from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, City, Profile, Comment
from .forms import PostForm, ProfileForm, CityForm, CommentForm, ReplyForm
from django.http import HttpResponse
import uuid
import boto3

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required   
def profile_login(request):
  request.session["steps"] = 0
  return redirect('profile', user_id=request.user.id)

@login_required
def profile(request, user_id):
  # track if modal has been shown
  request.session["steps"] -= 1 
  if request.session["steps"] <= 0:
    request.session["modeltoopen"] = ''
  posts = Post.objects.filter(user_id=user_id).order_by('-created_at')
  comments = Comment.objects.filter(reply_id=None)
  profile = Profile.objects.get(user_id=user_id)
  profile_form = ProfileForm(instance=profile)
  post_form = PostForm()
  comment_form = CommentForm()
  city_form = CityForm()
  return render(request, 'profile.html', { 
    'posts': posts,
    'profile': profile, 
    'profile_form': profile_form,
    'post_form': post_form,
    'comment_form': comment_form,
    'city_form': city_form,
    'comments': comments
    })

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'wayfarer-pp'
@login_required
def add_photo(request, user_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          profile = Profile.objects.get(user_id=request.user.id)
          profile.photo_url = url
          if user_id == request.user.id:
            profile.save()
      except:
          print('An error occurred uploading file to S3')  
  return redirect('profile_login')

@login_required
def profile_edit(request):
  profile = Profile.objects.get(user=request.user)
  profile_form = ProfileForm(request.POST or None, instance=profile)
  if request.POST and profile_form.is_valid():
    profile_form.save()
  return redirect('profile_login')

@login_required
def post_new(request):
  post_form = PostForm(request.POST or None)
  if request.POST and post_form.is_valid():
    new_post = post_form.save(commit=False)
    new_post.user = request.user
    new_post.city_id = request.POST['cityId']
    new_post.save()
  return redirect('city_show', city_id=new_post.city_id)

@login_required
def post_edit(request, post_id):
  post = Post.objects.get(id=post_id)
  post_form = PostForm(request.POST or None, instance=post)
  if request.user == post.user:
    if request.POST and post_form.is_valid():
      post_form.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def post_delete(request, post_id):
  post = Post.objects.get(id=post_id)
  if request.user == post.user:
    Post.objects.get(id=post_id).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def comment_new(request):
  comment_form = CommentForm(request.POST or None)
  if request.POST and comment_form.is_valid():
    new_comment = comment_form.save(commit=False)
    new_comment.user = request.user
    new_comment.post_id = request.POST['postId']
    new_comment.save()
    request.session["modeltoopen"] = new_comment.post_id
    request.session["steps"] = 2
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def reply_new(request):
  reply_form = ReplyForm(request.POST or None)
  if request.POST and reply_form.is_valid():
    reply = reply_form.save(commit=False)
    reply.user = request.user
    # reply.post_id = request.POST['postId']
    reply.reply_id = request.POST['replyId']
    reply.save()
    request.session["modeltoopen"] = Comment.objects.get(id=reply.reply_id).post_id
    request.session["steps"] = 2
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def city_new(request):
  city_form = CityForm(request.POST or None)
  if request.POST and city_form.is_valid():
    new_city = city_form.save()
  return redirect('city_show', city_id=new_city.id)


def city_show(request, city_id):
  # track if modal has been shown
  try: 
    request.session["steps"] -= 1
  except KeyError:
    request.session["steps"] = 0
    
  if request.session["steps"] <= 0:
    request.session["modeltoopen"] = ''
    
  post_form = PostForm(request.POST or None)
  city = City.objects.get(id=city_id)
  city_form = CityForm()
  posts = Post.objects.filter(city_id=city_id).order_by('-created_at')
  comments = Comment.objects.filter(reply_id=None)
  return render(request, 'cities/show.html', { 
    'city': city,
    'post_form': post_form,
    'posts': posts,
    'city_form': city_form,
    'comments': comments
    })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      profile = Profile(first_name = request.POST['first_name'], last_name = request.POST['last_name'], current_city = request.POST['current_city'], user = request.user )
      profile.save()
      return redirect('profile_login')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

    
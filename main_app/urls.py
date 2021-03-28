from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('profile/', views.profile_login, name="profile_login"),
  path('profile/<int:user_id>/add_photo/', views.add_photo, name="add_photo"),
  path('profile/<int:user_id>/', views.profile, name="profile"),
  path('profile/edit/', views.profile_edit, name="profile_edit"),
  path('posts/new/', views.post_new, name="post_new"),
  path('comments/new/', views.comment_new, name="comment_new"),
  path('reply/new/', views.reply_new, name="reply_new"),
  path('posts/<int:post_id>/edit/', views.post_edit, name="post_edit"),
  path('posts/<int:post_id>/delete/', views.post_delete, name="post_delete"),
  path('cities/new', views.city_new, name='city_new'),
  path('cities/<int:city_id>/', views.city_show, name='city_show'),
  path('accounts/signup/', views.signup, name='signup'),
] 
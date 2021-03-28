from django.db import models
from django.utils import timezone
import math

def check_time(self):
  now = timezone.now()
  created_at = models.DateTimeField(auto_now_add=True)
  difference = now - self.created_at
  within_a_minute = difference.days == 0 and difference.seconds >= 0 and difference.seconds <= 60
  under_an_hour = difference.days == 0 and difference.seconds >= 60 and difference.seconds < 3600
  under_a_day = difference.days == 0 and difference.seconds >= 3600 and difference.seconds < 86400
  under_a_month = difference.days >= 1 and difference.days < 30
  under_a_year = difference.days >= 30 and difference.days < 365
  
  if within_a_minute:
    return 'just now'
  elif under_an_hour:
    minutes = math.floor(difference.seconds/60)
    if minutes == 1:
      return ' 1 minute ago'
    else:
      return str(minutes) + ' minutes ago'
  elif under_a_day:
    hours = math.floor(difference.seconds/3600)
    if hours == 1:
      return ' 1 hour ago'
    else: 
      return str(hours) + ' hours ago'
  elif under_a_month:
    days = difference.days
    if days == 1:
      return ' 1 day ago'
    else: 
      return str(days) + ' days ago'
  elif under_a_year:
    months = math.floor(difference.days/30)
    if months == 1:
      return str(months) + ' month ago'
    else:
      return str(months) + ' months ago'
  else:
    years = math.floor(difference.days/365)
    if years == 1:
      return ' 1 year ago'
    else:
      return str(years) + ' years ago'


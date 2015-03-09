from django.conf.urls import patterns, include, url
from notice import views

urlpatterns = patterns('',
    # Examples:
    url(r'^(\d+)/', views.messagebox,name='messagebox'),
    url(r'^advice/', views.notice_advice,name='notice_advice'),
    url(r'^success/', views.notice_success,name='notice_success'),
    url(r'^fail/', views.notice_fail,name='notice_fail'),
)

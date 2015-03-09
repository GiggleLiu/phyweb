from django.conf.urls import patterns, include, url
from essay import views
from django.contrib import admin
admin.autodiscover()

handler404 = 'lala.views.page_not_found'
handler500 = 'lala.views.page_error'
urlpatterns = patterns('',
    # Examples:
    url(r'^(\d+)/$', views.topic_list, name='topic_list'),
    url(r'^update/(\d+)$', views.topic_update, name='topic_update'),
    url(r'^delete/(\d+)$', views.topic_delete, name='topic_delete'),
    url(r'^new/$', views.topic_new, name='topic_new'),
    url(r'^essay/list/(\d+)/(\d+)/$', views.essay_list, name='essay_list'),
    url(r'^essay/detail/(\d+)/$', views.essay_detail, name='essay_detail'),
    url(r'^essay/new/(\d+)/(\w+)/', views.essay_new,name='essay_new'),
    url(r'^essay/update/(\d+)/', views.essay_update,name='essay_update'),
    url(r'^essay/delete/(\d+)/', views.essay_delete,name='essay_delete'),
    url(r'^essay/edit/(\d+)/', views.essay_edit,name='essay_edit'),
    url(r'^user_blog/(\d+)/(\d+)/', views.user_blog,name='user_blog'),
    url(r'^fail_submit/', views.fail_submit,name='fail_submit'),

    #url('', include('django_socketio.urls')),
    #url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': '/media'}),
)
